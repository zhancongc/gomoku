//建立websocket通讯客户端
var namespace='/';
var socket=io.connect(location.protocol+'//'+document.domain+':'+location.port+namespace);
//监听日志
socket.on('response',function(message){
	try{
		var chessJson=JSON.parse(message['data']);
		if(chessJson.msg)
			log(chessJson.user+': '+chessJson.msg);
		return false;
	}
	catch(e){
		log(message['data']);
		return false;
	}
});
//监听棋子颜色
socket.on('image',function(message){
	var chessJson=JSON.parse(message['data']);
	chess.image=chessJson.image;
});
//监听游戏开始
socket.on('start',function(message){
	var chessJson=JSON.parse(message['data']);
	chess.start=chessJson.start
	log('Game start.');
	chess.opponent=((chessJson.player1===chess.user)?chessJson.player2:chessJson.player1);
});
//监听棋权
socket.on('right',function(message){
	var chessJson=JSON.parse(message['data']);
	chess.right=chessJson.right;
	chess.image=chessJson.image;
	log('It is '+chess.right+'\'s turn.');
});
//监听落子信息
socket.on('coordinate',function(message){
	var chessJson=JSON.parse(message['data']);
	chess.image=chessJson.image;
	chess.coordinate=[chessJson.x,chessJson.y];
	log(chess.coordinate);
	getCell(chess.coordinate).style.backgroundImage='url('+chessJson.image+')';
	getCell(chess.coordinate).innerHTML='<span class="code">'+chess.code.toString()+'</span>'
	getCell(chess.coordinate).children[0].style.color=(chess.code%2===1?'white':'grey');
	chess.code+=1;
});
//监听胜负信息
socket.on('result',function(message){
	var chessJson=JSON.parse(message['data']);//{'result':'lucy'}
	chess.result=chessJson.result;
	log('Winner is '+chess.result);
	chess.start=0;
	if(chess.result===chess.user){
		alert('恭喜你，你赢了！');
	}
	else if (chess.result==='dogfall') {
		alert('很可惜是平局，再来一局如何？');
	}
	else {
		alert(chess.result+'赢了。')
	}
});
//监听初始化
socket.on('clear',function chessClear(){
	initial();
});
//监听重来的消息
socket.on('restart',function(message){
	var chessJson=JSON.parse(message['data']);//{'loser':'jack'}
	console.log('loser: '+chessJson['loser']);
	console.log('opponent: '+chess.opponent);
	if (chessJson['loser']===chess.opponent) {
		var varification=confirm(chess.opponent+'希望结束这一局，开始下一局游戏，你接受吗？');
		var message=new Object();
		message.user=chess.user;
		if (varification) {
			message.confirm=1;
		}
		else{
			message.confirm=0;
		}
		var msgRestart=JSON.stringify(message);
		console.log(msgRestart);
		socket.emit('restartConfirm',{data: msgRestart});//{'user':'lucy','confirm':1}
	}
});