#!/usr/bin/python
# -*- coding: UTF-8 -*-
class chess(object):
	variable=0
	username=[]
	winner=''
	loser=''
	chessBar=[[0 for col in range(15)]for row in range(15)]

	def clear():
		chess.variable=0
		chess.username=[]
		chess.loser=''
		chess.chessBar=[[0 for col in range(15)]for row in range(15)]

	def clock(key):
		if key==0:
			return(1)
		if key==1:
			return(0)
		else:
			raise ValueError

	def judgeWin(varification,coordinate):
		judge=[]
		for i in range(4):
			judge.append(chess.fiveConnection(i,varification,coordinate))
		print(judge)
		for x in judge:
			if x:
				return(1)
		return(0)

	def fiveConnection(type,varification,coordinate):
		count=0
		if type==0:
			x=coordinate[0]
			y=coordinate[1]
			while True:
				if (x<15 and chess.chessBar[x][y]==varification):
					count+=1
					x+=1
				else:
					break
			x=coordinate[0]
			y=coordinate[1]
			while True:
				if (x>=0 and chess.chessBar[x][y]==varification):
					count+=1
					x-=1
				else:
					break
		elif type==1:
			x=coordinate[0]
			y=coordinate[1]
			while True:
				if (x<15 and y<15 and chess.chessBar[x][y]==varification):
					count+=1
					x+=1
					y+=1
				else:
					break
			x=coordinate[0]
			y=coordinate[1]
			while True:
				if (x>=0 and y>=0 and chess.chessBar[x][y]==varification):
					count+=1
					x-=1
					y-=1
				else:
					break
		elif type==2:
			x=coordinate[0]
			y=coordinate[1]
			while True:
				if (y<15 and chess.chessBar[x][y]==varification):
					count+=1
					y+=1
				else:
					break
			x=coordinate[0]
			y=coordinate[1]
			while True:
				if (y>=0 and chess.chessBar[x][y]==varification):
					count+=1
					y-=1
				else:
					break
		elif type==3:
			x=coordinate[0]
			y=coordinate[1]
			while True:
				if (x>=0 and y<15 and chess.chessBar[x][y]==varification):
					count+=1
					x-=1
					y+=1
				else:
					break
			x=coordinate[0]
			y=coordinate[1]
			while True:
				if (x<15 and y>=0 and chess.chessBar[x][y]==varification):
					count+=1
					x+=1
					y-=1
				else:
					break
		print(count)
		if count>5:
			return(1)
		else:
			return(0)

	def logRecord(message):
		log=open('../log/gomoku.log','a+')
		log.write(message)
		log.close()
