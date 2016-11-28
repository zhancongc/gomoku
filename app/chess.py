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

	def judgeWin(varification,coordinate):#judgeWin(1,[4,5])
		judge=[]
		for i in range(4):# 0:0d,1:45d,2:90d,3:135d
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


	def statusCode(type,varification,coordinate):# fiveConnection(0,1,[4,5])
		count=0
		interference=0
		handler=[]
		score=0
		if type==0:
			x,y=coordinate[0],coordinate[1]
			while True:
				if (x<15 and chessBar[x][y]==varification):
					count+=1
					x+=1
				else:
					x+=1
					if (x<15):
						if(chessBar[x][y]!=0):
							if (chessBar[x][y]!=varification):
								interference+=1
						else:
							handler.append(x)
							handler.append(y)
					break
			x,y=coordinate[0],coordinate[1]
			while True:
				if (x>=0 and chess.chessBar[x][y]==varification):
					count+=1
					x-=1
				else:
					x-=1
					if (x>=0):
						if (chessBar[x][y]!=0):
							if (chessBar[x][y]!=varification):
								interference+=1
						else:
							handler.append(x)
							handler.append(y)
					break
		elif type==1:
			x,y=coordinate[0],coordinate[1]
			while True:
				if (x<15 and y<15 and chess.chessBar[x][y]==varification):
					count+=1
					x,y=x+1,y+1
				else:
					x,y=x+1,y+1
					if (x<15 and y<15):
						if (chessBar[x][y]!=0):
							if (chessBar[x][y]!=varification):
								interference+=1
						else:
							handler.append(x)
							handler.append(y)
					break
			x,y=coordinate[0],coordinate[1]
			while True:
				if (x>=0 and y>=0 and chess.chessBar[x][y]==varification):
					count+=1
					x,y=x-1,y-1
				else:
					x,y=x-1,y-1
					if (x>=0 and y>=0)
						if (chessBar[x][y]!=0):
							if (chessBar[x][y]!=varification):
								interference+=1
						else:
							handler.append(x)
							handler.append(y)
					break
		elif type==2:
			x,y=coordinate[0],coordinate[1]
			while True:
				if (y<15 and chess.chessBar[x][y]==varification):
					count+=1
					y+=1
				else:
					y+=1
					if (y<15):
						if (chess.chessBar[x][y]!=0):
							if (chessBar[x][y]!=varification):
								interference+=1
						else:
							handler.append(x)
							handler.append(y)
					break
			x,y=coordinate[0],coordinate[1]
			while True:
				if (y>=0 and chess.chessBar[x][y]==varification):
					count+=1
					y-=1
				else:
					y-=1
					if (y>0):
						if(chess.chessBar[x][y]!=0):
							if (chessBar[x][y]!=varification):
								interference+=1
						else:
							handler.append(x)
							handler.append(y)
					break
		elif type==3:
			x,y=coordinate[0],coordinate[1]
			while True:
				if (x>=0 and y<15 and chess.chessBar[x][y]==varification):
					count+=1
					x,y=x-1,y+1
				else:
					x,y=x-1,y+1
					if (x>=0 and y<15):
						if(chess.chessBar[x][y]!=0):
							if (chessBar[x][y]!=varification):
								interference+=1
						else:
							handler.append(x)
							handler.append(y)
					break
			x,y=coordinate[0],coordinate[1]
			while True:
				if (x<15 and y>=0 and chess.chessBar[x][y]==varification):
					count+=1
					x,y=x+1,y-1
				else:
					x,y=x+1,y-1
					if (x<15 and y>=0):
						if(chess.chessBar[x][y]!=0):
							if (chessBar[x][y]!=varification):
								interference+=1
						else:
							handler.append(x)
							handler.append(y)
					break
		print('count: '+count)
		print('interference: '+interference)
		if (count==2 and interference==1):
			score+=1
		elif(count==2 and interference==0):
			score+=10
		elif(count==3 and interference==1):
			score+=10
		elif(count==3 and interference==0):
			score+=100
		elif(count==4 and interference==1):
			score+=100
		elif(count==4 and interference==0):
			score+=1000
		elif(count==5 and interference==1):
			score+=1000
		elif(count==5 and interference==0):
			score+=10000
		elif(count==6 and interference==2):
			score+=10000
		elif(count==6 and interference==1):
			score+=10000
		elif(count==6 and interference==0):
			score+=10000
		else:
			score+=0
		return(score)

