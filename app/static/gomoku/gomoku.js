//游戏逻辑
//创建一个五子棋对象，并初始化
var chess=new Object();
//初始化本地用户
chess.user=prompt('What is your name?');
$('#player1').html('<p>玩家：'+chess.user+'</p>');
function initial(){
	//棋子的序号，描述落子的先后顺序
	chess.code=1;
	//你的对手
	chess.opponent=''
	//对应image监听器
	chess.image='';
	//对应start监听器
	chess.start=0;
	//对应right监听器
	chess.right='';
	//对应coordinate监听器
	chess.coordinate=[];
	//对应result监听器
	chess.result='';
	//对应restart监听器
	chess.loser='';
	//清除场上的棋子
	list=$('span');
	log('Now,it is a new game.');
	for(var i=0;i<list.length;i++){
		list[i].parentNode.style.backgroundImage='';
		list[i].parentNode.innerHTML='';
	}
}
initial();
//获取元素坐标的函数
function getCoordinate(obj){
	var chessBar=document.querySelectorAll('.chess-line');
	var parentElement=obj.parentElement;
	var i=0,j=0;
	for (i = 0; obj; i++) {
		obj=obj.previousElementSibling;
	}
	for (j = 0; parentElement; j++) {
		parentElement=parentElement.previousElementSibling;
	}
	return [i-1,j-1];
}
//通过坐标获取元素的函数
function getCell(coordinate){
	var x=-1,y=-1;
	x=coordinate[0];
	y=coordinate[1];
	var chessBar=document.querySelectorAll('.chess-line');
	var obj=chessBar[y].childNodes[2*x+1];
	return obj;
}
//log生成函数
function log(msg) {
	document.getElementById('log').innerHTML='<p>'+msg+'</p>'+document.getElementById('log').innerHTML;
}
//准备消息
function prepare(){
	socket.emit('prepare',{data: chess.user});//jack
}
//发送落子消息
function play(obj){
	if(chess.start&&chess.right===chess.user){
		var coordinate=getCoordinate(obj);
		var chessJson=new Object();
		chessJson.user=chess.user;
		chessJson.image=chess.image;
		chessJson.x=coordinate[0];
		chessJson.y=coordinate[1];
		var chessData=JSON.stringify(chessJson);
		socket.emit('chess',{data: chessData});//{'user':'jack','image':'../static/gomoku/black.png','x':6,'y':5}
	}
}
//聊天模块
//注册键盘事件
document.onkeydown = function(e) {
	//捕捉回车事件
	var ev = (typeof event!= 'undefined') ? window.event : e;
	if(ev.keyCode == 13) {
		send();
	}
}
function send() {
	if(!document.getElementById('text').value){
		alert('please enter something.');
		return false;
	}
	var msg='';
	msg=document.getElementById('text').value;
	var message=new Object();
	message.user=chess.user;
	message.msg=msg;
	var msgSend=JSON.stringify(message);
	socket.emit('message', {data: msgSend});
	document.getElementById('text').value='';
};
//请求重来
function restart(){
	if (chess.start===1) {
		var varification=confirm('你希望认输并开始下一局吗？如果你的对手不同意则不会生效。')
		if(varification){
			chess.loser=chess.user;
			var message=new Object();
			message.loser=chess.loser;
			var msgRestart=JSON.stringify(message);
			socket.emit('restart',{data: msgRestart});//{'loser':'jack'}
			console.log(chess.user);
		}
	}
	if(chess.start===0){
		var message=new Object();
		message.user=chess.user;
		var msgClear=JSON.stringify(message);
		socket.emit('clear', {data: msgClear});
	}
}

function gameHelp(){
	$("#gameHelp").slideToggle();
}
function getUser(){
	socket.emit('getUser');
}
function getVariable(){
	socket.emit('getVariable');
}