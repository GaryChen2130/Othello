import copy
import time

class Game:
	def __init__(self):
		self.stone = []
		self.empty_pos = []
		self.board = self.Init()
		self.weights = self.SetWeights()


	def Init(self):
		self.stone.append('@')
		self.stone.append('O')

		board = []
		for i in range(8):
			board.append([])
			for j in range(8):
				board[i].append(' ')
				self.empty_pos.append((i,j))

		board[3][3] = 'O'
		board[3][4] = '@'
		board[4][3] = '@'
		board[4][4] = 'O'

		self.empty_pos.remove((3,3))
		self.empty_pos.remove((3,4))
		self.empty_pos.remove((4,3))
		self.empty_pos.remove((4,4))

		return board


	def SetWeights(self):
		weights = [[120,-60,20,5,5,20,-60,120],
					[-60,-80,-5,-5,-5,-5,-80,-60],
					[20,-5,15,3,3,15,-5,20],
					[5,-5,3,3,3,3,-5,5],
					[5,-5,3,3,3,3,-5,5],
					[20,-5,15,3,3,15,-5,20],
					[-60,-80,-5,-5,-5,-5,-80,-60],
					[120,-60,20,5,5,20,-60,120]]
		return weights


	def GameLoop(self,player):

		mover = 0
		Pass = 0
		while(True):
			if not mover:
				print('black\'s turn')
			else:
				print('white\'s turn')

			legal_positions = self.FindLegalPos(self.board,mover)
			print(legal_positions)
			self.PrintBoard(self.board)

			if len(legal_positions) > 0:
				Pass = 0
				if mover == player:
					op = input('Select Position:')
					while (int(op[0]),int(op[2])) not in legal_positions:
						op = input('Select Position:')

					#self.board[int(op[0])][int(op[2])] = self.stone[mover]
					self.MakeMove(self.board,mover,(int(op[0]),int(op[2])))
					self.empty_pos.remove((int(op[0]),int(op[2])))

				else:
					start_time = time.time()
					print('Oppnent Select Position')
					pos = self.SearchPos(self.board,legal_positions,mover,4)
					print(pos)
					self.MakeMove(self.board,mover,pos)
					self.empty_pos.remove(pos)
					end_time = time.time()
					print("--- %s sec ---" % (end_time - start_time))
			else:
				Pass += 1

			mover = mover^1
			self.RestoreBoard(self.board)
			self.PrintBoard(self.board)

			if Pass == 2:
				self.EndGame()
				break


	def EndGame(self):
		black_num = 0
		white_num = 0
		for i in range(8):
			for j in range(8):
				if self.board[i][j] == '@':
					black_num += 1
				elif self.board[i][j] == 'O':
					white_num += 1

		print('Black Stones: ' + str(black_num))
		print('White Stones: ' + str(white_num))

		if black_num > white_num:
			print('black wins')
		elif white_num > black_num:
			print('white wins')
		else:
			print('draw')

		return


	def FindLegalPos(self,board,mover):
		legal_positions = []
		directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
		for pos in self.empty_pos:
			for direction in directions:
				flag = False
				neighbor = (pos[0] + direction[0],pos[1] + direction[1])
				while (neighbor[0] >= 0) and (neighbor[0] <= 7) and (neighbor[1] >= 0) and (neighbor[1] <= 7) and (board[neighbor[0]][neighbor[1]] == self.stone[mover^1]):
					neighbor = (neighbor[0] + direction[0],neighbor[1] + direction[1])
					flag = True

				if (neighbor[0] >= 0) and (neighbor[0] <= 7) and (neighbor[1] >= 0) and (neighbor[1] <= 7) and flag and (board[neighbor[0]][neighbor[1]] == self.stone[mover]):
					board[pos[0]][pos[1]] = 'X'
					legal_positions.append(pos)
					break

		return legal_positions


	def MakeMove(self,board,mover,pos):
		directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
		flip_positions = []
		for direction in directions:
			propose_positions = []
			neighbor = (pos[0] + direction[0],pos[1] + direction[1])
			while (neighbor[0] >= 0) and (neighbor[0] <= 7) and (neighbor[1] >= 0) and (neighbor[1] <= 7) and (board[neighbor[0]][neighbor[1]] == self.stone[mover^1]):
				propose_positions.append(neighbor)
				neighbor = (neighbor[0] + direction[0],neighbor[1] + direction[1])

			if (neighbor[0] >= 0) and (neighbor[0] <= 7) and (neighbor[1] >= 0) and (neighbor[1] <= 7) and (board[neighbor[0]][neighbor[1]] == self.stone[mover]):
				flip_positions += propose_positions

		#print(flip_positions)
		for flip_position in flip_positions:
			board[flip_position[0]][flip_position[1]] = self.stone[mover]
		board[pos[0]][pos[1]] = self.stone[mover]

		return


	def h(self,board,mover):
		val = 0
		for i in range(8):
			for j in range(8):
				if board[i][j] == ' ':
					continue
				elif board[i][j] == self.stone[mover]:
					val += self.weights[i][j]
				elif board[i][j] == self.stone[mover^1]:
					val -= self.weights[i][j]
		return val


	def MinMax(self,sim_board,mover,pos_cur,depth,Maximize):
		#print('depth: ' + str(depth) + ' mover: ' + str(mover))
		#print('Before Sim')
		#self.PrintBoard(sim_board)
		self.MakeMove(sim_board,mover,pos_cur)
		#print('After Sim')
		self.RestoreBoard(sim_board)
		#self.PrintBoard(sim_board)

		legal_positions = self.FindLegalPos(sim_board,mover^1)
		if depth*len(legal_positions) == 0:
			#if depth == 4 or (pos_cur[0] == 1 and pos_cur[1] == 1): 
			#	print('MinMax in depth(' + str(depth) + '): ' + str(self.h(pos_cur)*Maximize))
			#	print(pos_cur)
			#return self.h(pos_cur)*Maximize
			return self.h(sim_board,mover)

		'''
		Max = -99999
		Max_pos = None
		for pos in legal_positions:
			val = self.MinMax(copy.deepcopy(sim_board),mover^1,pos,depth - 1,Maximize*-1)
			if val > Max:
				Max = val
				Max_pos = pos
		if depth == 4 or (Max_pos[0] == 1 and Max_pos[1] == 1):  
			print('MinMax in depth(' + str(depth) + '): ' + str(Max*Maximize))
			print(Max_pos)
		return Max*Maximize
		'''

		if Maximize > 0:
			best = -99999
			for pos in legal_positions:
				val = self.MinMax(copy.deepcopy(sim_board),mover^1,pos,depth - 1,Maximize*-1)
				if val > best:
					best = val
		else:
			best = 99999
			for pos in legal_positions:
				val = self.MinMax(copy.deepcopy(sim_board),mover^1,pos,depth - 1,Maximize*-1)
				if val < best:
					best = val
		return best


	def SearchPos(self,board,legal_positions,mover,depth):
		Max = -99999
		Max_pos = None
		for pos in legal_positions:
			val = self.MinMax(copy.deepcopy(board),mover,pos,depth,-1)
			if val > Max:
				Max = val
				Max_pos = pos
		return Max_pos


	def RestoreBoard(self,board):
		for i in range(8):
			for j in range(8):
				if board[i][j] == 'X':
					board[i][j] = ' '
		return


	def PrintBoard(self,board):
		for row in board:
			print(row)
		print('-------------------------------------------\n')
		return


if __name__ == '__main__':
	player = eval(input('Select Player: (0 for black, 1 for white)'))
	game = Game()
	game.PrintBoard(game.board)
	game.GameLoop(player)
