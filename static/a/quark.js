(function($,win){
	
	
	var w,h,x,y;
	var gly = document.getElementById('gly');
	var context = gly.getContext("2d");
	var canvas = $(gly);
	
	$(window).resize(function() {
		w = $(window).outerWidth();
		h =$('.index-banner').height();
		setSize();
	}).resize();
	if (w>720) {
		$(document).mousemove(function(){
		
				x = event.clientX;
				y = event.clientY;
				kx = 0.5*(x/w-.5);
				ky = 0.5*(y/h-.5);
			
		});
	} else{
		x = w/2;
		y= h/2;
	}
	function setSize() {
		canvas.width(w).height(h).attr({
			'width': w,
			'height': h
		});
	}
	var roll = Math.random;
	var PI = Math.PI;
	var sin = Math.sin;
	var cos = Math.cos;
	var atan = Math.atan;
	var cosh = Math.cosh;
	
	console.log();
	
	
	var len = 5000,min=10,max=40,c=(max-min),zk=.001,zb=1,a=0,b=0;
	
	var list = new Array(len);
	
	var x=0,y=0,z=0,zx=0,rx=0,kx=0,ky=0,kk=0,ak=0;
	
	for (var i = 0;i<len;i++) {
		list[i]={a:roll()*2*PI,ay:roll()*2*PI,r:roll()*c+min,k:roll(),v:roll()*0.05};
		list[i].r=list[i].r*list[i].r;
	}
		
	function getVal(a,ay,r,k,v){
		y = sin(ay)*r;
		rx =cos(ay)*r
		z = sin(a+kx+ak)*rx;
		x = cos(a+kx+ak)*rx;
		//		zx = cos(a+kx)*z;
		zx = z;
	}
	
	var img01 = new Image();
	img01.src = 'images/bgg01.png';
	
	function draw(){
		ak+=0.001;
		context.globalAlpha=1;
		
		context.fillStyle='#110e22';

		context.fillRect(0,0,w,h);
		context.fillStyle='#6f5d91';
		
		
		context.drawImage(img01,-w/5,-h/5,w*1.4,h*1.2);
		
		
//		context.strokeStyle='#FFF';
		for (var i = 0 ; i < len ; i++) {
				getVal(list[i].a,list[i].ay,list[i].r,list[i].k,list[i].v);
				if (list[i].k>1) {
					list[i].k=1;
					list[i].v=-list[i].v;
				} else if (list[i].k<0){
					list[i].k=0;
					list[i].v=-list[i].v;
				}else{
					list[i].k+=list[i].v
				}
				zx = zx*zk+zb;
				
				kk = zx;
				
					if (Math.random()>.01) {
						context.globalAlpha=(kk+.05)*list[i].k;
					} else{
						context.globalAlpha=kk*list[i].k;
					}
				
				if (zx<0) {
					zx = 0.1
				}
				context.beginPath();
				context.arc(w*.5+x,h*.5+y,zx,0,PI*2);
				context.closePath();
				context.fill();
		}
		
		
	}
	
	
	
	setInterval(draw,1000/10);

})(jQuery,window)


