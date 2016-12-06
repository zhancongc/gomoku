#!/usr/bin/python
# -*- coding: UTF-8 -*-
class Chess(object):
	def __init__(self,variable,username,winner,loser,chessBar,rank):
		self.variable=variable
		self.username=username
		self.winner=winner
		self.loser=loser
		self.chessBar=chessBar
		self.rank=rank

	def clear(self):
		self.variable=0
		self.username=[]
		self.winner=''
		self.loser=''
		self.chessBar=[[0 for col in range(15)]for row in range(15)]
		self.rank=[[0 for col in range(15)]for row in range(15)]

	def clock(self,key):
		if key==0:
			return(1)
		if key==1:
			return(0)
		else:
			raise ValueError

	def judgeWin(self,varification,coordinate):#judgeWin(1,[4,5])
		judge=[]
		for i in range(4):# 0:0d,1:45d,2:90d,3:135d
			judge.append(self.fiveConnection(i,varification,coordinate))
		print(judge)
		for x in judge:
			if x:
				return(1)
		return(0)

	def fiveConnection(self,type,varification,coordinate):
		count=0
		if type==0:
			x=coordinate[0]
			y=coordinate[1]
			while True:
				if (x<15 and self.chessBar[x][y]==varification):
					count+=1
					x+=1
				else:
					break
			x=coordinate[0]
			y=coordinate[1]
			while True:
				if (x>=0 and self.chessBar[x][y]==varification):
					count+=1
					x-=1
				else:
					break
		elif type==1:
			x=coordinate[0]
			y=coordinate[1]
			while True:
				if (x<15 and y<15 and self.chessBar[x][y]==varification):
					count+=1
					x+=1
					y+=1
				else:
					break
			x=coordinate[0]
			y=coordinate[1]
			while True:
				if (x>=0 and y>=0 and self.chessBar[x][y]==varification):
					count+=1
					x-=1
					y-=1
				else:
					break
		elif type==2:
			x=coordinate[0]
			y=coordinate[1]
			while True:
				if (y<15 and self.chessBar[x][y]==varification):
					count+=1
					y+=1
				else:
					break
			x=coordinate[0]
			y=coordinate[1]
			while True:
				if (y>=0 and self.chessBar[x][y]==varification):
					count+=1
					y-=1
				else:
					break
		elif type==3:
			x=coordinate[0]
			y=coordinate[1]
			while True:
				if (x>=0 and y<15 and self.chessBar[x][y]==varification):
					count+=1
					x-=1
					y+=1
				else:
					break
			x=coordinate[0]
			y=coordinate[1]
			while True:
				if (x<15 and y>=0 and self.chessBar[x][y]==varification):
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

	def logRecord(self,message):
		log=open('../log/gomoku.log','a+')
		log.write(message)
		log.close()

	def Score(self,count,interference):
		if (count==2 and interference==1):
			score=1
		elif(count==2 and interference==0):
			score=10
		elif(count==3 and interference==1):
			score=10
		elif(count==3 and interference==0):
			score=100
		elif(count==4 and interference==1):
			score=100
		elif(count==4 and interference==0):
			score=1000
		elif(count==5 and interference==1):
			score=1000
		elif(count==5 and interference==0):
			score=10000
		elif(count==6 and interference==2):
			score=10000
		elif(count==6 and interference==1):
			score=10000
		elif(count==6 and interference==0):
			score=10000
		else:
			score=0
		return(score)

	def dotRank(self,type,varification,coordinate):# fiveConnection(0,1,[4,5])
		count=0 #连子个数
		interference=0 #挡路的棋子
		handler=[] #解决方案
		score=0 #得分
		if type==0:
			x,y=coordinate[0],coordinate[1]
			while True:
				if (x<15 and self.chessBar[x][y]==varification):
					count+=1
					x+=1
				else:
					if (x<15):
						if(self.chessBar[x][y]!=0):
							if (self.chessBar[x][y]!=varification):
								interference+=1
						else:
							handler.append(x)
							handler.append(y)
					break
			x,y=coordinate[0],coordinate[1]
			while True:
				if (x>=0 and self.chessBar[x][y]==varification):
					count+=1
					x-=1
				else:
					if (x>=0):
						if (self.chessBar[x][y]!=0):
							if (self.chessBar[x][y]!=varification):
								interference+=1
						else:
							handler.append(x)
							handler.append(y)
					break
		elif type==1:
			x,y=coordinate[0],coordinate[1]
			while True:
				if (x<15 and y<15 and self.chessBar[x][y]==varification):
					count+=1
					x,y=x+1,y+1
				else:
					if (x<15 and y<15):
						if (self.chessBar[x][y]!=0):
							if (self.chessBar[x][y]!=varification):
								interference+=1
						else:
							handler.append(x)
							handler.append(y)
					break
			x,y=coordinate[0],coordinate[1]
			while True:
				if (x>=0 and y>=0 and self.chessBar[x][y]==varification):
					count+=1
					x,y=x-1,y-1
				else:
					if (x>=0 and y>=0):
						if (self.chessBar[x][y]!=0):
							if (self.chessBar[x][y]!=varification):
								interference+=1
						else:
							handler.append(x)
							handler.append(y)
					break
		elif type==2:
			x,y=coordinate[0],coordinate[1]
			while True:
				if (y<15 and self.chessBar[x][y]==varification):
					count+=1
					y+=1
				else:
					if (y<15):
						if (self.chessBar[x][y]!=0):
							if (self.chessBar[x][y]!=varification):
								interference+=1
						else:
							handler.append(x)
							handler.append(y)
					break
			x,y=coordinate[0],coordinate[1]
			while True:
				if (y>=0 and self.chessBar[x][y]==varification):
					count+=1
					y-=1
				else:
					if (y>0):
						if(self.chessBar[x][y]!=0):
							if (self.chessBar[x][y]!=varification):
								interference+=1
						else:
							handler.append(x)
							handler.append(y)
					break
		elif type==3:
			x,y=coordinate[0],coordinate[1]
			while True:
				if (x>=0 and y<15 and self.chessBar[x][y]==varification):
					count+=1
					x,y=x-1,y+1
				else:
					if (x>=0 and y<15):
						if(self.chessBar[x][y]!=0):
							if (self.chessBar[x][y]!=varification):
								interference+=1
						else:
							handler.append(x)
							handler.append(y)
					break
			x,y=coordinate[0],coordinate[1]
			while True:
				if (x<15 and y>=0 and self.chessBar[x][y]==varification):
					count+=1
					x,y=x+1,y-1
				else:
					if (x<15 and y>=0):
						if(self.chessBar[x][y]!=0):
							if (self.chessBar[x][y]!=varification):
								interference+=1
						else:
							handler.append(x)
							handler.append(y)
					break
		print('count: %s' % count)
		print('interference: %s' % interference)
		print('handler: ',handler)
		score+=self.Score(count,interference)
		if varification==1:
			score/=(count-1)
		else:
			score/=(count+2)
		print(int(score))
		if(len(handler)==4):
			if (self.chessBar[handler[0]][handler[1]]==0):
				self.rank[handler[0]][handler[1]]+=int(score)
			if (self.chessBar[handler[2]][handler[3]]==0):
				self.rank[handler[2]][handler[3]]+=int(score)
		elif(len(handler)==2):
			if (self.chessBar[handler[0]][handler[1]]==0):
				self.rank[handler[0]][handler[1]]+=int(score)

	def findDot(self,varification):
		dots=[]
		for x in range(0,15):
			for y in range(0,15):
				if(self.chessBar[x][y]==varification):
					dots.append([x,y])
		return(dots)

	def topScore(self):
		tmp=0
		dot=[]
		for x in range(0,15):
			for y in range(0,15):
				if(self.chessBar[x][y]==0 and self.rank[x][y]>tmp):
					tmp=self.rank[x][y]
					dot=[x,y]
		return(dot)
