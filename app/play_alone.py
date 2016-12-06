#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
sys.path.append('..')
import json
from flask import Flask, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from app.views import mode
from app.chess import Chess


app=Flask(__name__)
app.register_blueprint(mode, url_prefix='')
app.config['DEBUG']=True
app.config['SECRET_KEY']='secret'
socketio=SocketIO(app)

chessBar=[[0 for col in range(15)]for row in range(15)]
rank=[[0 for col in range(15)]for row in range(15)]
gomoku=Chess(0,[],'','',chessBar,rank)


@socketio.on('connect')
def handler_connect():
	emit('response', {'data': 'connection established!'})

@socketio.on('prepare')
def handler_prepare(message):
	print('Someone is prepared')
	if(gomoku.username==[]):
		obj=json.loads(message['data'])
		gomoku.username.append('computer')
		gomoku.username.append(obj['user'])
		print(gomoku.username[1])
		msgStart=json.dumps({'start':1})
		emit('start',{'data':msgStart},broadcast=True)
		msgPlay=json.dumps({'user':'computer','image':'../static/gomoku/black.png','x':7,'y':7})
		gomoku.chessBar[7][7]=1
		gomoku.variable=gomoku.clock(gomoku.variable)
		print(msgPlay)
		emit('coordinate',{'data':msgPlay},broadcast=True)

@socketio.on('chess') #{'user':'jack','image':'../static/gomoku/black.png','x':6,'y':5}
def handler_play(message):
	if(gomoku.variable==1):
		obj=json.loads(message['data'])
		print('obj:')
		print(obj)
		if (gomoku.chessBar[obj['x']][obj['y']]==0):
			gomoku.chessBar[obj['x']][obj['y']]=2
			emit('coordinate',{'data':message['data']},broadcast=True)
			gomoku.variable=gomoku.clock(gomoku.variable)
			print('coordinate')
		if gomoku.judgeWin(2,[obj['x'],obj['y']]):
			msgResult=json.dumps({'result':gomoku.username[1]})
			emit('result',{'data':msgResult},broadcast=True)
			print(msgResult)
		else:
			gomoku.rank=[[0 for col in range(15)]for row in range(15)]
			dots=gomoku.findDot(1)
			print(dots)
			for dot in dots:
				for i in range(0,4):
					gomoku.dotRank(i,1,dot)
			dots=gomoku.findDot(2)
			print(dots)
			for dot in dots:
				for i in range(0,4):
					gomoku.dotRank(i,2,dot)
			dot=gomoku.topScore()
			gomoku.chessBar[dot[0]][dot[1]]=1
			msgPlay=json.dumps({'user':'computer','image':'../static/gomoku/black.png','x':dot[0],'y':dot[1]})
			emit('coordinate',{'data':msgPlay},broadcast=True)
			gomoku.variable=gomoku.clock(gomoku.variable)
			if gomoku.judgeWin(1,dot):
				msgResult=json.dumps({'result':gomoku.username[0]})
				emit('result',{'data':msgResult},broadcast=True)
				print(msgResult)

@socketio.on('clear')
def handler_clear(message):
	obj=json.loads(message['data'])
	print(obj)
	if(obj['user'] in gomoku.username):
		emit('clear',broadcast=True)
		gomoku.clear()
#key error
@socketio.on('restart')
def handler_restart(message):
	obj=json.loads(message['data'])#{'loser':'jack'}
	if(obj['loser']==gomoku.username[1]):
		gomoku.loser=gomoku.username[1]
		gomoku.winner=gomoku.username[0]
	if(obj['loser']==gomoku.username[0]):
		gomoku.loser=gomoku.username[0]
		gomoku.winner=gomoku.username[1]
	print('gomoku.loser: '+gomoku.loser)
	msgResult=json.dumps({'result':gomoku.winner})
	emit('result',{'data': msgResult}, broadcast=True)#{'result':'jack'}
	emit('clear',broadcast=True)
	gomoku.clear()

@socketio.on('message')
def handler_message(message):
	try:
		obj=json.loads(message['data'])#{"user":"jackson","msg":"hello,everyone"}
		print(obj['user']+':'+obj['msg'])
	except ValueError as e:
		print('It is not a chat.')
	finally:
		emit('response',{'data':message['data']},broadcast=True)


if __name__ == '__main__':
	socketio.run(app,host='0.0.0.0',port=5000)