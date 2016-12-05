import unittest
from chess import Chess

class TestChess(unittest.TestCase):
	def setUp(self):
		self.chessBar=[[0 for col in range(15)]for row in range(15)]
		self.rank=[[0 for col in range(15)]for row in range(15)]
		self.gomoku=Chess(0,[],'','',self.chessBar,self.rank)
	def tearDown(self):
		self.gomoku.clear()
	def test_dot_rank(self):
		for y in range(4,8):
			self.gomoku.chessBar[5][y]=1
			print(5,y)
		for x in range(4,9):
			self.gomoku.chessBar[x][5]=1
		self.gomoku.chessBar[5][8]=2
		self.gomoku.chessBar[5][3]=2
		for x in range(0,4):
			print(self.gomoku.dotRank(x,1,[5,5]))

if __name__ == '__main__':
	unittest.main()