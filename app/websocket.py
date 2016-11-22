from run import app

socketio=SocketIO(app)

@socketio.on('connect',namespace='/')
def handler_connect():
	emit('response', {'data': 'connection established!'})

@socketio.on('prepare')
def handler_prepare(message):
	if (len(chess.username)==0):
		if message['data']:
			chess.username.append(message['data'])
			emit('response', {'data': chess.username[0]+' is prepared.'},broadcast=True)
	elif (len(chess.username)==1):
		if message['data'] and message['data']!=chess.username[0]:
			chess.username.append(message['data'])
			emit('response', {'data': chess.username[1]+' is prepared.'},broadcast=True)
			msgStart=json.dumps({'start':1,'player1':chess.username[0],'player2':chess.username[1]})
			msgRight=json.dumps({'right':chess.username[0],'image':'../static/gomoku/black.png'})
			emit('start', {'data': msgStart},broadcast=True)
			emit('right', {'data': msgRight},broadcast=True)
	else:
		if (len(chess.username)>1 and len(chess.username)<10):
			if message['data']:
				chess.username.append(message['data'])
			emit('response', {'data': 'this room is full.'})

@socketio.on('chess')
def handler_chess(message):#{'user':'jack','image':'../static/gomoku/black.png','x':6,'y':5}
	obj=json.loads(message['data'])
	if obj['user']==chess.username[chess.variable] and chess.chessBar[obj['x']][obj['y']]==0:
		emit('coordinate', {'data': message['data']},broadcast=True)
		chess.chessBar[obj['x']][obj['y']]=chess.variable+1
		dot=[obj['x'],obj['y']]
		if chess.judgeWin(chess.variable+1,dot):
			msgResult=json.dumps({'result': chess.username[chess.variable]})
			print(msgResult)
			emit('result',{'data': msgResult},broadcast=True)
		else:
			chess.variable=chess.clock(chess.variable)
			if chess.variable:
				image='../static/gomoku/white.png'
			else:
				image='../static/gomoku/black.png'
			msgRight=json.dumps({'right': chess.username[chess.variable],'image':image})
			emit('right', {'data': msgRight},broadcast=True)

@socketio.on('message')
def handler_message(message):
	try:
		obj=json.loads(message['data'])#{"user":"jackson","msg":"hello,everyone"}
		print(obj['user']+':'+obj['msg'])
	except ValueError as e:
		print('It is not a chat.')
	finally:
		emit('response',{'data':message['data']},broadcast=True)

@socketio.on('clear')
def handler_clear(message):
	obj=json.loads(message['data'])
	if(obj['user'] in chess.username):
		emit('clear',broadcast=True)
		chess.clear()

@socketio.on('restart')
def handler_restart(message):
	if(message['data']==chess.username[0]):
		chess.loser=chess.username[0]
	elif(message['data']==chess.username[1]):
		chess.loser=chess.username[1]
	print('chess.loser: '+chess.loser)
	emit('restartConfirm',{'data':chess.loser},broadcast=True)

@socketio.on('restartConfirm')
def handler_restartConfirm(message):
	obj=json.loads(message['data'])
	if(obj['user'] in chess.username and obj['user']!=chess.loser):
		emit('restartConfirm',{'data':message['data']},broadcast=True)
		if (obj['confirm']==1):
			print('game will be clear.')
			chess.clear()

@socketio.on('getUser')
def handler_getUser():
	obj=json.dumps(chess.username)
	emit('response',{'data':obj})

@socketio.on('getVariable')
def handler_getVariable():
	emit('response',{'data':chess.variable})