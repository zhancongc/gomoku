#import json, unittest,sys
#sys.path.append('../')
#from config import *
from gomoku import chess
from websocket import app, socketio


if __name__=='__main__':
	socketio.run(app,host='0.0.0.0',port=5000)