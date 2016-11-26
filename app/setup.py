import sys
sys.path.append('..')
import json
from flask import Flask, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from app.views import mode
from app.chess import chess

app=Flask(__name__)
app.register_blueprint(mode, url_prefix='')
app.config['DEBUG']=True
app.config['SECRET_KEY']='secret'
socketio=SocketIO(app)


@socketio.on('connect',namespace='/')
def handler_connect():
	emit('response', {'data': 'connection established!'})

@socketio.on('prepare')
def handler_prepare(message):
	print('someone was prepared.')
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
			chess.winner=chess.username[chess.variable]
			msgResult=json.dumps({'result': chess.winner})
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
	obj=json.loads(message['data'])#{'loser':'jack'}
	if(obj['loser']==chess.username[0]):
		chess.loser=chess.username[0]
	elif(obj['loser']==chess.username[1]):
		chess.loser=chess.username[1]
	print('chess.loser: '+chess.loser)
	emit('restart',{'data': message['data']}, broadcast=True)#{'loser':'jack'}

@socketio.on('restartConfirm')
def handler_restartConfirm(message):
	obj=json.loads(message['data'])#{'user':'lucy','confirm':1}
	if(obj['user'] in chess.username and obj['user']!=chess.loser and obj['confirm']==1):
		chess.winner=obj['user']
		msgResult=json.dumps({'result': chess.winner})
		print(msgResult)
		emit('result',{'data': msgResult}, broadcast=True)#{'result':'lucy'}
		emit('clear',broadcast=True)
		print('game will be clear.')
		chess.clear()

@socketio.on('getUser')
def handler_getUser():
	obj=json.dumps(chess.username)
	emit('response',{'data':obj})

@socketio.on('getVariable')
def handler_getVariable():
	emit('response',{'data':chess.variable})

if __name__ == '__main__':
	socketio.run(app,host='0.0.0.0',port=5000)
