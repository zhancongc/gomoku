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
	print('someone was prepared.')
	if (len(gomoku.username)==0):
		if message['data']:
			gomoku.username.append(message['data'])
			emit('response', {'data': gomoku.username[0]+' is prepared.'},broadcast=True)
	elif (len(gomoku.username)==1):
		if message['data'] and message['data']!=gomoku.username[0]:
			gomoku.username.append(message['data'])
			emit('response', {'data': gomoku.username[1]+' is prepared.'},broadcast=True)
			msgStart=json.dumps({'start':1,'player1':gomoku.username[0],'player2':gomoku.username[1]})
			msgRight=json.dumps({'right':gomoku.username[0],'image':'../static/gomoku/black.png'})
			emit('start', {'data': msgStart},broadcast=True)
			emit('right', {'data': msgRight},broadcast=True)
	else:
		if (len(gomoku.username)>1 and len(gomoku.username)<10):
			if message['data']:
				gomoku.username.append(message['data'])
			emit('response', {'data': 'this room is full.'})

@socketio.on('chess')
def handler_chess(message):#{'user':'jack','image':'../static/gomoku/black.png','x':6,'y':5}
	obj=json.loads(message['data'])
	if obj['user']==gomoku.username[gomoku.variable] and gomoku.chessBar[obj['x']][obj['y']]==0:
		emit('coordinate', {'data': message['data']},broadcast=True)
		gomoku.chessBar[obj['x']][obj['y']]=gomoku.variable+1
		dot=[obj['x'],obj['y']]
		if gomoku.judgeWin(gomoku.variable+1,dot):
			gomoku.winner=gomoku.username[gomoku.variable]
			msgResult=json.dumps({'result': gomoku.winner})
			print(msgResult)
			emit('result',{'data': msgResult},broadcast=True)
		else:
			gomoku.variable=gomoku.clock(gomoku.variable)
			if gomoku.variable:
				image='../static/gomoku/white.png'
			else:
				image='../static/gomoku/black.png'
			msgRight=json.dumps({'right': gomoku.username[gomoku.variable],'image':image})
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
	if(obj['user'] in gomoku.username):
		emit('clear',broadcast=True)
		gomoku.clear()

@socketio.on('restart')
def handler_restart(message):
	obj=json.loads(message['data'])#{'loser':'jack'}
	if(obj['loser']==gomoku.username[0]):
		gomoku.loser=gomoku.username[0]
	elif(obj['loser']==gomoku.username[1]):
		gomoku.loser=gomoku.username[1]
	print('gomoku.loser: '+gomoku.loser)
	emit('restart',{'data': message['data']}, broadcast=True)#{'loser':'jack'}

@socketio.on('restartConfirm')
def handler_restartConfirm(message):
	obj=json.loads(message['data'])#{'user':'lucy','confirm':1}
	if(obj['user'] in gomoku.username and obj['user']!=gomoku.loser and obj['confirm']==1):
		gomoku.winner=obj['user']
		msgResult=json.dumps({'result': gomoku.winner})
		print(msgResult)
		emit('result',{'data': msgResult}, broadcast=True)#{'result':'lucy'}
		emit('clear',broadcast=True)
		print('game will be clear.')
		gomoku.clear()

@socketio.on('getUser')
def handler_getUser():
	obj=json.dumps(gomoku.username)
	emit('response',{'data':obj})

@socketio.on('getVariable')
def handler_getVariable():
	emit('response',{'data':gomoku.variable})

if __name__ == '__main__':
	socketio.run(app,host='0.0.0.0',port=5000)
