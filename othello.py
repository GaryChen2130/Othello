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
		weights = [[4,-3,2,2,2,2,-3,4],
					[-3,-4,-1,-1,-1,-1,-4,-3],
					[2,-1,1,0,0,1,-1,2],
					[2,-1,0,1,1,0,-1,2],
					[2,-1,0,1,1,0,-1,2],
					[2,-1,1,0,0,1,-1,2],
					[-3,-4,-1,-1,-1,-1,-4,-3],
					[4,-3,2,2,2,2,-3,4]]
		return weights


	def GameLoop(self,player):

		mover = 0
		Pass = 0
		while(True):
			if not mover:
				print('black\'s turn')
			else:
				print('white\'s turn')

			legal_positions = self.FindLegalPos(mover)
			print(legal_positions)
			self.PrintBoard()

			if len(legal_positions) > 0:
				Pass = 0
				if mover == player:
					op = input('Select Position:')
					while (int(op[0]),int(op[2])) not in legal_positions:
						op = input('Select Position:')

					#self.board[int(op[0])][int(op[2])] = self.stone[mover]
					self.MakeMove(mover,(int(op[0]),int(op[2])))
					self.empty_pos.remove((int(op[0]),int(op[2])))

				else:
					print('Oppnent Select Position')
					pos = self.SearchPos(legal_positions)
					print(pos)
					#self.board[pos[0]][pos[1]] = self.stone[mover]
					self.MakeMove(mover,pos)
					self.empty_pos.remove(pos)
			else:
				Pass += 1

			mover = mover^1
			self.RestoreBoard()
			self.PrintBoard()

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


	def FindLegalPos(self,mover):
		legal_positions = []
		directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
		for pos in self.empty_pos:
			for direction in directions:
				flag = False
				neighbor = (pos[0] + direction[0],pos[1] + direction[1])
				while (neighbor[0] >= 0) and (neighbor[0] <= 7) and (neighbor[1] >= 0) and (neighbor[1] <= 7) and (self.board[neighbor[0]][neighbor[1]] == self.stone[mover^1]):
					neighbor = (neighbor[0] + direction[0],neighbor[1] + direction[1])
					flag = True

				if (neighbor[0] >= 0) and (neighbor[0] <= 7) and (neighbor[1] >= 0) and (neighbor[1] <= 7) and flag and (self.board[neighbor[0]][neighbor[1]] == self.stone[mover]):
					self.board[pos[0]][pos[1]] = 'X'
					legal_positions.append(pos)
					break

		return legal_positions


	def MakeMove(self,mover,pos):
		directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
		flip_positions = []
		for direction in directions:
			propose_positions = []
			neighbor = (pos[0] + direction[0],pos[1] + direction[1])
			while (neighbor[0] >= 0) and (neighbor[0] <= 7) and (neighbor[1] >= 0) and (neighbor[1] <= 7) and (self.board[neighbor[0]][neighbor[1]] == self.stone[mover^1]):
				propose_positions.append(neighbor)
				neighbor = (neighbor[0] + direction[0],neighbor[1] + direction[1])

			if (neighbor[0] >= 0) and (neighbor[0] <= 7) and (neighbor[1] >= 0) and (neighbor[1] <= 7) and (self.board[neighbor[0]][neighbor[1]] == self.stone[mover]):
				flip_positions += propose_positions

		for flip_position in flip_positions:
			self.board[flip_position[0]][flip_position[1]] = self.stone[mover]
		self.board[pos[0]][pos[1]] = self.stone[mover]

		return


	def SearchPos(self,legal_positions):
		Max = -99999
		Max_pos = None
		for pos in legal_positions:
			if self.weights[pos[0]][pos[1]] > Max:
				Max = self.weights[pos[0]][pos[1]]
				Max_pos = pos
		return Max_pos


	def RestoreBoard(self):
		for i in range(8):
			for j in range(8):
				if self.board[i][j] == 'X':
					self.board[i][j] = ' '
		return


	def PrintBoard(self):
		for row in self.board:
			print(row)
		print('-------------------------------------------\n')
		return


if __name__ == '__main__':
	player = eval(input('Select Player: (0 for black, 1 for white)'))
	game = Game()
	game.PrintBoard()
	game.GameLoop(player)
