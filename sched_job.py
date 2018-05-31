from flask import json
import sqlite3
import urllib.request
import sched
import time
from datetime import datetime


class EasySqlite:
    """
    sqlite数据库操作工具类

    database: 数据库文件地址，例如：db/mydb.db
    """
    _connection = None

    def __init__(self, database):
        # 连接数据库
        self._connection = sqlite3.connect(database)

    def _dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def execute(self, sql, args=[], result_dict=True, commit=True) -> list:
        """
        执行数据库操作的通用方法

        Args:
        sql: sql语句
        args: sql参数
        result_dict: 操作结果是否用dict格式返回
        commit: 是否提交事务

        Returns:
        list 列表，例如：
        [{'id': 1, 'name': '张三'}, {'id': 2, 'name': '李四'}]
        """
        if result_dict:
            self._connection.row_factory = self._dict_factory
        else:
            self._connection.row_factory = None
            # 获取游标
        _cursor = self._connection.cursor()
        # 执行SQL获取结果
        _cursor.execute(sql, args)
        if commit:
            self._connection.commit()
        data = _cursor.fetchall()
        _cursor.close()
        return data


def get_user_tx(address):
    user_erc_address = address
    data = {}
    data['module'] = 'account'
    data['action'] = 'txlist'
    data['address'] = user_erc_address
    data['startblock'] = 0
    data['endblock'] = 99999999
    data['sort'] = 'desc'
    data['apikey'] = '4JK3E2HVSV1AKJHD5I3TG1CQFHNCBUUWNJ'
    # UM1CWYYZFUAH2PHAE74DAF1WE97756N99X
    # 6ZBKAKHK4E12Y1N1EC4NGECY8HWP4KEEDT
    url_parame = urllib.parse.urlencode(data)
    url = "http://api.etherscan.io/api?"
    request_url = url + url_parame
    get_data = urllib.request.urlopen(request_url).read()
    json_result = json.loads(get_data)
    return json_result


def update_inviter_balance():
    db = EasySqlite('db/cst.db')
    ico_erc_address = '0xE95c7c81ed1De8E8d897695b0ca22DD4a010E865'
    invite_list = db.execute("select * from invite")
    if len(invite_list) > 0:
        for record in invite_list:
            owner = db.execute("select erc20_address from user where email = ?",[record['owner']])[0]['erc20_address']
            inviter = db.execute("select erc20_address from user where email = ?",[record['inviter']])[0]['erc20_address']
            tx_owner = get_user_tx(owner)
            tx_owner_json_result_list = tx_owner['result']
            if len(tx_owner_json_result_list) > 0:
                for tx in tx_owner_json_result_list:
                    eth_value = int(tx['value'])
                    eth_value = eth_value * 0.000000000000000001
                    tx_from = tx['from']
                    tx_to = tx['to']
                    if eth_value > 0 and tx_from.lower() == owner.lower() and tx_to.lower() in ico_erc_address.lower():
                        eth_reward = eth_value * 0.1
                        eth_reward = round(eth_reward, 6)
                        try:
                            db.execute('update invite set owner_transfer_balance = ? , inviter_reward = ? where owner = ? and inviter = ?', [eth_value, eth_reward, record['owner'], record['inviter']])
                        except Exception as e:
                            err = e


# 初始化sched模块的 scheduler 类
# 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
schedule = sched.scheduler(time.time, time.sleep)


# 被周期性调度触发的函数
def printTime(inc):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    update_inviter_balance()
    schedule.enter(inc, 0, printTime, (inc,))


# 默认参数60s
def main(inc=60):
    # enter四个参数分别为：间隔事件、优先级（用于同时间到达的两个事件同时执行时定序）、被调用触发的函数，
    # 给该触发函数的参数（tuple形式）
    schedule.enter(0, 0, printTime, (inc,))
    schedule.run()


# 10s 输出一次
main(60)
