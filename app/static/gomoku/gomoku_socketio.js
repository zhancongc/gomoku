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
	var chessJson=JSON.parse(message['data']);
	chess.result=chessJson.result;
	log('Winner is '+chess.result);
	chess.start=0;
	if(chess.result===chess.user){
		alert('Congratulations, you have won!');
	}
	else if (chess.result==='dogfall') {
		alert('Neither you win, nor lose.How about trying again?');
	}
	else {
		alert(chess.result+' has won.')
	}
});
//监听初始化
socket.on('clear',function chessClear(){
	initial();
	list=$('span');
	log('Now,it is a new game.');
	for(var i=0;i<list.length;i++){
		list[i].parentNode.style.backgroundImage='';
		list[i].parentNode.innerHTML='';
	}
});
//监听重来的消息
socket.on('restart',function(message){
	if (message['data']===chess.opponent) {
		var varification=confirm(chessJson.user+' was meaning to admit defeat or restart the game, do you agree with him or her?');
		if (varification) {
			var msgRestart={'user':chess.user,'confirm':1}.toString();
			socket.emit('restartConfirm',{data: msgRestart});
		}
		else{
			var msgRestart={'user':chess.user,'confirm':1}.toString();
			socket.emit('restartConfirm',{data: msgRestart});
		}
	}
});
//监听重来的确认消息
socket.on('restartConfirm',function(message){
	var chessJson=JSON.parse(message['data']);
	if (chessJson.confirm===1) {
		if (chessJson.user===chess.user) {
			alert('Congratulations, you have won!');
		}
		alert(chessJson.user+' has won!');
		initial();
	}
});