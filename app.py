from flask import Flask, render_template, request
import sqlite3,logging,random,string

app = Flask(__name__)

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename='log/error.log', level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


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


@app.route('/')
def index():
    invite_code = request.args.get('r')
    return render_template('a.html', invite_code=invite_code)


@app.route('/b/')
def b():
    return render_template('b.html')


def activation_code(id, length=10):
    prefix = hex(int(id))[2:] + 'L'
    length = length - len(prefix)
    chars = string.ascii_letters + string.digits
    return prefix + ''.join([random.choice(chars) for i in range(length)])


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        db = EasySqlite('db/cst.db')
        email = request.form.get('mail')
        erc20_address = request.form.get('eth')
        invite_code = request.form.get('invite_code')

        if invite_code is not None and invite_code != 'None':
            inviter = db.execute('select * from user where code = ?', [invite_code])
            invite_data = db.execute('select * from invite where inviter = ? and owner = ?',[inviter[0]['email'], email])
            if len(invite_data) == 0 and inviter[0]['email'] != email:
                db.execute('insert into invite(inviter,owner) values(?,?) ', [inviter[0]['email'], email])

        owner = db.execute('select * from user where email = ?', [email])
        if len(owner) > 0:
            invite_number = db.execute("select * from invite where inviter = ?", [email])
            invite_number = len(invite_number)
            invite_reward = db.execute("select sum(inviter_reward) as inviter_reward from invite where inviter = ?", [email])[0]['inviter_reward']
            if invite_reward != None:
                invite_reward = round(invite_reward, 6)
            else:
                invite_reward = 0
            token_info = {
                "r": owner[0]['code'],
                "balance": invite_reward,
                "erc20_address": owner[0]['erc20_address'],
                "invite_number": invite_number
            }
            return render_template('c.html', token_info=token_info)
        else:
            maxid = db.execute('select max(id) as id from user')
            maxid = int(maxid[0]['id']) + 1
            code = activation_code(maxid)
            try:
                db.execute('insert into user(id,erc20_address,email,code) values(?,?,?,?) ',[maxid, erc20_address, email, code])
            except Exception as e:
                logging.error(e)
            token_info = {
                "r": code,
                "balance": 0,
                "erc20_address": erc20_address,
                "invite_number": 0
            }
            return render_template('c.html', token_info=token_info)


if __name__ == '__main__':
    app.run()
