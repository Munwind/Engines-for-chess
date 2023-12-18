class GameState():
	def __init__(self):
		self.board = [
			['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
			['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
			['--', '--', '--', '--', '--', '--', '--', '--'],
			['--', '--', '--', '--', '--', '--', '--', '--'],
			['--', '--', '--', '--', '--', '--', '--', '--'],
			['--', '--', '--', '--', '--', '--', '--', '--'],
			['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
	 		['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

		self.numOfMoves = 0
		self.whiteToMove = True
		self.moveLog = []

		# Work for castling
		self.whiteKingLocation = (7, 4)
		self.blackKingLocation = (0, 4)
		
		# Work for checking the valid moves part
		self.pieceToBePinned = []
		self.isCheckedBy = []
		self.inCheck = False
		self.addPin = False
  
		self.checkMate = False
		self.staleMate = False
		self.draw = False

		self.currentCastlingRight = CastleRights(True, True, True, True)
		self.castleRightLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]
		self.storePosition = []
  
	def makeMove(self, move):
		self.board[move.startRow][move.startCol] = '--'  # empty the start cell 
		self.board[move.endRow][move.endCol] = move.pieceMoved 	# keep the piece moved on the end cell
		self.moveLog.append(move) 	# record the move
  
		if move.pieceMoved == 'wK':
			self.whiteKingLocation = (move.endRow, move.endCol)
		elif move.pieceMoved == 'bK':
			self.blackKingLocation = (move.endRow, move.endCol)

		if self.board[move.endRow][move.endCol][1] == 'p':
			if move.endRow == 0 or move.endRow == 7:
				self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

		if move.pieceMoved[1] == 'K':
			if move.endCol - move.startCol == 2:
				self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
				self.board[move.endRow][move.endCol + 1] = '--'
			elif move.endCol - move.startCol == -2:
				self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
				self.board[move.endRow][move.endCol - 2] = '--'

		self.updateCastleRights(move)
		self.castleRightLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))

		position = self.calculatePosition()
		self.storePosition.append(position)

		self.numOfMoves += 1
		self.whiteToMove = not self.whiteToMove
	
	def unMakeMove(self):
		if len(self.moveLog) > 0:
			move = self.moveLog.pop()
			self.board[move.startRow][move.startCol] = move.pieceMoved
			self.board[move.endRow][move.endCol] = move.pieceCaptured
    
			self.whiteToMove = not self.whiteToMove
			if move.pieceMoved == 'wK':
				self.whiteKingLocation = (move.startRow, move.startCol)
			elif move.pieceMoved == 'bK':
				self.blackKingLocation = (move.startRow, move.startCol)
   
			self.castleRightLog.pop()
			newRights = self.castleRightLog[-1]
			self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)

			# Castle
			if move.pieceMoved[1] == 'K':
				if move.endCol - move.startCol == 2:
					self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
					self.board[move.endRow][move.endCol - 1] = '--'
				elif move.endCol - move.startCol == -2:
					self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
					self.board[move.endRow][move.endCol + 1] = '--'

			self.storePosition.pop()
			self.numOfMoves -= 1

	def updateCastleRights(self, move):
		if move.pieceMoved == 'wK':
			self.currentCastlingRight.wks = False
			self.currentCastlingRight.wqs = False
		elif move.pieceMoved == 'bK':
			self.currentCastlingRight.bks = False
			self.currentCastlingRight.bqs = False
		elif move.pieceMoved == 'wR':
			if move.startRow == 7:
				if move.startCol == 0:
					self.currentCastlingRight.wqs = False
				elif move.startCol == 7:
					self.currentCastlingRight.wks = False
		elif move.pieceMoved == 'bR':
			if move.startRow == 0:
				if move.startCol == 0:
					self.currentCastlingRight.bqs = False
				elif move.startCol == 7:
					self.currentCastlingRight.bks = False
     
     
	def isDrawByRepetition(self):
		lastPosition = self.storePosition[-1]
		count = self.storePosition.count(lastPosition)

		if count >= 3:
			return True
		return False

	def calculatePosition(self):
		position = ''
		for row in self.board:
			for square in row:
				if square == '--':
					position += '0'
				else:
					position += square
     
		return position

	def getPossibleMoves(self):
		check = False
		temp = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
		moves = []
		self.addPin = True
		self.pieceToBePinned = []
		self.isCheckedBy = []
		self.get_Pins_and_Checks()
		if not self.inCheck:
			check = False
		else:
			check = True
   
		kingRow, kingCol = self.whiteKingLocation if self.whiteToMove else self.blackKingLocation
		
		# Handling the case where the king is checked
		if self.inCheck:
			# Check => the king move or block with pieces
			if len(self.isCheckedBy) == 1:
				posRow, posCol = self.isCheckedBy[0][0], self.isCheckedBy[0][1]
				directionRow, directionCol = self.isCheckedBy[0][2], self.isCheckedBy[0][3]
				moves = self.generateAllMoves()
				
				blockSquare = []
				
				# Block or capture the piece
				if self.board[posRow][posCol][1] == 'N': # If the kinght check => capture
					blockSquare.append((posRow, posCol))
				else:  # Other pieces checking
					for i in range(1, 8):
						rr, cc = kingRow + directionRow * i, kingCol + directionCol * i
						if 0 <= rr < 8 and 0 <= cc < 8:
							blockSquare.append((rr, cc))
							if rr == posRow and cc == posCol:
								break
				
				for i in range(len(moves) - 1, -1, -1):
					if moves[i].pieceMoved[1] != 'K':
						if not (moves[i].endRow, moves[i].endCol) in blockSquare:
							moves.remove(moves[i])
			
			# Double-check situation => must move the king
			elif len(self.isCheckedBy) == 2:
				self.getKingMoves(kingRow, kingCol, moves)
					
		else:
			moves = self.generateAllMoves()
		
		if len(moves) == 0:
			self.get_Pins_and_Checks
			if check:
				self.checkMate = True
			else:
				self.staleMate = True

		else:
			self.checkMate = False
			self.staleMate = False

		self.currentCastlingRight = temp
   
		return moves

	def get_Pins_and_Checks(self):
		self.inCheck = False

		count = [[0] * 4 for _ in range(4)]
		directions = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))
  
		for i in range(8):
			possiblePins = ()
			for j in range(1, 8):
				
				color = 'w' if self.whiteToMove else 'b'
				r, c = self.whiteKingLocation if self.whiteToMove else self.blackKingLocation
				# The orthorgonal and diagonal
				rr, cc = r + directions[i][0] * j, c + directions[i][1] * j
				
				if 0 <= rr < 8 and 0 <= cc < 8:
					if self.board[rr][cc][0] == color and self.board[rr][cc][1] != 'K':
						if possiblePins == ():
							possiblePins = (rr, cc, directions[i][0], directions[i][1])
						else:
							break
					
					elif self.board[rr][cc][0] != color and self.board[rr][cc][0] != '-':
						pieceCanAttack = self.board[rr][cc][1]
						if pieceCanAttack == 'Q' or (0 <= i < 4 and pieceCanAttack == 'R') or (4 <= i < 8 and pieceCanAttack == 'B') or (j == 1 and color == 'w' and pieceCanAttack == 'p' and 6 <= i < 8) or (j == 1 and color == 'b' and pieceCanAttack == 'p' and 4 <= i < 6) or (j == 1 and pieceCanAttack == 'K'):
          
							if possiblePins == ():
								
								self.inCheck = True
								if self.addPin:
									if count[directions[i][0] + 1][directions[i][1] + 1] == 0:
										self.isCheckedBy.append((rr, cc, directions[i][0], directions[i][1]))
										count[directions[i][0] + 1][directions[i][1] + 1] = 1
							else:
								if not (possiblePins in self.pieceToBePinned) and self.addPin:
									self.pieceToBePinned.append(possiblePins)
								break
						else:
							break
				else:
					break
			
			# Special case for the kinghts
		moves = ((1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (2, -1), (-2, -1), (-2, 1))
		for k in range(8):
			newRow, newCol = r + moves[k][0], c + moves[k][1]
			if 0 <= newRow < 8 and 0 <= newCol < 8:
				if self.board[newRow][newCol][0] != color and self.board[newRow][newCol][1] == 'N':
					self.inCheck = True
					if self.addPin:
						self.isCheckedBy.append((newRow, newCol, moves[k][0], moves[k][1]))
					break
	
	'''
	If the square (r, c) is attacked return True, False otherwise
 	'''
	def isAttacked(self, r, c):
		directions = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))
		enemyColor = 'b' if self.whiteToMove else 'w'
		allyColor = 'w' if self.whiteToMove else 'b'
  
		for i in range(8):
			for j in range(1, 8):
				rr, cc = r + directions[i][0] * j, c + directions[i][1] * j
				if 0 <= rr < 8 and 0 <= cc < 8:
					if self.board[rr][cc][0] == allyColor:  # Same color
						break
					elif self.board[rr][cc][0] == enemyColor:
						pieceCanAttack = self.board[rr][cc][1]
						if pieceCanAttack == 'Q' or (0 <= i < 4 and pieceCanAttack == 'R') or (4 <= i < 8 and pieceCanAttack == 'B') or (j == 1 and allyColor == 'w' and pieceCanAttack == 'p' and 6 <= i < 8) or (j == 1 and allyColor == 'b' and pieceCanAttack == 'p' and 4 <= i < 6) or (j == 1 and pieceCanAttack == 'K'):
							return True
						break
   
		moves = ((1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (2, -1), (-2, -1), (-2, 1))
		for k in range(8):
			newRow, newCol = r + moves[k][0], c + moves[k][1]
			if 0 <= newRow < 8 and 0 <= newCol < 8:
				if self.board[newRow][newCol][0] == enemyColor and self.board[newRow][newCol][1] == 'N':
					return True

		return False
    
	def generateAllMoves(self):
		moves = []
  
		for i in range(8):
			for j in range(8):
				if (self.whiteToMove and self.board[i][j][0] == 'w') or (not self.whiteToMove and self.board[i][j][0] == 'b'):
					if self.board[i][j][1] == 'p':
						self.getPawnMoves(i, j, moves)
					elif self.board[i][j][1] == 'R':
						self.getRookMoves(i, j, moves)
					elif self.board[i][j][1] == 'N':
						self.getKnightMoves(i, j, moves)
					elif self.board[i][j][1] == 'B':
						self.getBishopMoves(i, j, moves)
					elif self.board[i][j][1] == 'Q':
						self.getRookMoves(i, j, moves)
						self.getBishopMoves(i, j, moves)
					elif self.board[i][j][1] == 'K':
						self.getKingMoves(i, j, moves)

		return moves

	def getPawnMoves(self, r, c, moves):
		isPinned = False
		pinDirection = ()

		for i in range(len(self.pieceToBePinned) - 1, -1, -1):	
			if self.pieceToBePinned[i][0] == r and self.pieceToBePinned[i][1] == c:
				isPinned = True
				pinDirection = (self.pieceToBePinned[i][2], self.pieceToBePinned[i][3])
				self.pieceToBePinned.remove(self.pieceToBePinned[i])
				break

		if self.whiteToMove:
			
			if self.board[r - 1][c] == '--':
				if not isPinned or pinDirection == (-1, 0) or pinDirection == (1, 0):
					moves.append(Move((r, c), (r - 1, c), self.board))
					if r == 6 and self.board[r - 2][c] == '--':
						moves.append(Move((r, c), (r - 2, c), self.board))
			if c > 0:
				if not isPinned or pinDirection == (-1, -1):
					if self.board[r - 1][c - 1][0] == 'b':	
						moves.append(Move((r, c), (r - 1, c - 1), self.board))
			if c < 7:
				if not isPinned or pinDirection == (-1, 1):
					if self.board[r - 1][c + 1][0] == 'b':	
						moves.append(Move((r, c), (r - 1, c + 1), self.board))
	
		else:
			if self.board[r + 1][c] == '--':
				if not isPinned or pinDirection == (-1, 0) or pinDirection == (1, 0):	
					moves.append(Move((r, c), (r + 1, c), self.board))
					if r == 1 and self.board[r + 2][c] == '--':
						moves.append(Move((r, c), (r + 2, c), self.board))
			if c > 0:
				if not isPinned or pinDirection == (1, -1):
					if self.board[r + 1][c - 1][0] == 'w':
						moves.append(Move((r, c), (r + 1, c - 1), self.board))
			if c < 7:
				if not isPinned or pinDirection == (1, 1):
					if self.board[r + 1][c + 1][0] == 'w':	
						moves.append(Move((r, c), (r + 1, c + 1), self.board))
	
	def getRookMoves(self, r, c, moves):
		directions = ((-1, 0), (1, 0), (0, 1), (0, -1))
		isPinned = False
		pinDirection = ()

		for i in range(len(self.pieceToBePinned) - 1, -1, -1):
			if self.pieceToBePinned[i][0] == r and self.pieceToBePinned[i][1] == c:
				isPinned = True
				pinDirection = (self.pieceToBePinned[i][2], self.pieceToBePinned[i][3])
				if self.board[r][c][1] != 'Q':
					self.pieceToBePinned.remove(self.pieceToBePinned[i])
				break
				
		for i in range(4):
			for j in range(1, 8):
				rr, cc = r + directions[i][0] * j, c + directions[i][1] * j
				
				if 0 <= rr < 8 and 0 <= cc < 8:
					if not isPinned or pinDirection == directions[i] or pinDirection == (-directions[i][0], -directions[i][1]):
						if self.board[rr][cc][0] == '-':
							moves.append(Move((r, c), (rr, cc), self.board))
						elif self.board[rr][cc][0] == self.board[r][c][0]:
							break
						elif self.board[rr][cc][0] != self.board[r][c][0]:
							moves.append(Move((r, c), (rr, cc),self.board))
							break
				else:
					break
	
	def getKnightMoves(self, r, c, moves):
		directions = ((1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (2, -1), (-2, -1), (-2, 1))
		isPinned = False
		pinDirection = ()

		for i in range(len(self.pieceToBePinned) -  1, -1, -1):
			if self.pieceToBePinned[i][0] == r and self.pieceToBePinned[i][1] == c:
				isPinned = True
				return

		for i in range(8):
			rr, cc = r + directions[i][0], c + directions[i][1]
			if 0 <= rr < 8 and 0 <= cc < 8:
				if self.board[rr][cc][0] == '-' or self.board[rr][cc][0] != self.board[r][c][0]:
					moves.append(Move((r, c), (rr, cc), self.board))
	
	def getBishopMoves(self, r, c, moves):
		directions = ((1, 1), (1, -1), (-1, 1), (-1, -1))
		isPinned = False
		pinDirection = ()
		
		for i in range(len(self.pieceToBePinned) - 1, -1, -1):
			if self.pieceToBePinned[i][0] == r and self.pieceToBePinned[i][1] == c:
				isPinned = True
				pinDirection = (self.pieceToBePinned[i][2], self.pieceToBePinned[i][3])
				self.pieceToBePinned.remove(self.pieceToBePinned[i])
				break
    
		for i in range(4):
			for j in range(1, 8):
				rr, cc = r + directions[i][0] * j, c + directions[i][1] * j

				if 0 <= rr < 8 and 0 <= cc < 8:
					if not isPinned or pinDirection == (directions[i][0], directions[i][1]) or pinDirection == (- directions[i][0], - directions[i][1]):
						if self.board[rr][cc][0] == '-':
							moves.append(Move((r, c), (rr, cc), self.board))
						elif self.board[rr][cc][0] == self.board[r][c][0]:
							break
						elif self.board[rr][cc][0] != self.board[r][c][0]:	
							moves.append(Move((r, c), (rr, cc), self.board))
							break
	
	def getKingMoves(self, r, c, moves):
		self.addPin = False
		directions = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (1, 1), (-1, 1), (-1, -1))
  
		for i in range(8):
			rr, cc = r + directions[i][0], c + directions[i][1]
			
			if 0 <= rr < 8 and 0 <= cc < 8:
				if self.board[rr][cc][0] == '-' or self.board[rr][cc][0] != self.board[r][c][0]:
					
					if self.whiteToMove:
						self.whiteKingLocation = (rr, cc)
					else:
						self.blackKingLocation = (rr, cc)

					self.get_Pins_and_Checks()
					if self.inCheck == False:
						moves.append(Move((r, c), (rr, cc), self.board))

					if self.whiteToMove:
						self.whiteKingLocation = (r, c)
					else:
						self.blackKingLocation = (r, c)

		if not self.isAttacked(r, c):
			self.getCastleMoves(r, c, moves)

	def getCastleMoves(self, r, c, moves):
		if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
			self.getKingsideCastleMoves(r, c, moves)
		if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
			self.getQueensideCastleMoves(r, c, moves)
	
	def getKingsideCastleMoves(self, r, c, moves):
		if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--':
			if not self.isAttacked(r, c + 1) and not self.isAttacked(r, c + 2):
				moves.append(Move((r, c), (r, c + 2), self.board))
	
	def getQueensideCastleMoves(self, r, c, moves):
		if self.board[r][c - 1]	== '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--':
			if not self.isAttacked(r, c - 1) and not self.isAttacked(r, c - 2):
				moves.append(Move((r, c), (r, c - 2), self.board))
  
class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
        

class Move():

	def __init__(self, startSq, endSq, board):
		self.startRow = startSq[0]
		self.startCol = startSq[1]
		self.endRow = endSq[0]
		self.endCol = endSq[1]
		self.pieceMoved = board[self.startRow][self.startCol] # can't be '--' 
		self.pieceCaptured = board[self.endRow][self.endCol]  # can be '--' -> no piece was captured 
		self.moveId = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
  
	def __eq__(self,other):
		return isinstance(other, Move) and self.moveId == other.moveId
