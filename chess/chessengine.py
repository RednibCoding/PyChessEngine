
# ChessEngine is a simple chess engine with an ai included

# ChessEngine uses the "python-chess" v0.30.1 library from "Niklas Fiekas"
# (https://github.com/niklasf/python-chess)
# "python-chess" is bundled into ChessEngine, so no need to install "python-chess" seperately via pip
import chess

from typing import List

class ChessEngine:
	def __init__(self):
		self.__board = chess.Board()

		"""
		piece-square tables used from
		https://www.chessprogramming.org/Simplified_Evaluation_Function
		"""
		self.__pawntable = [
		0,  0,  0,  0,  0,  0,  0,  0,
		5, 10, 10,-20,-20, 10, 10,  5,
		5, -5,-10,  0,  0,-10, -5,  5,
		0,  0,  0, 20, 20,  0,  0,  0,
		5,  5, 10, 25, 25, 10,  5,  5,
		10, 10, 20, 30, 30, 20, 10, 10,
		50, 50, 50, 50, 50, 50, 50, 50,
		0,  0,  0,  0,  0,  0,  0,  0]

		self.__knightstable = [
		-50,-40,-30,-30,-30,-30,-40,-50,
		-40,-20,  0,  5,  5,  0,-20,-40,
		-30,  5, 10, 15, 15, 10,  5,-30,
		-30,  0, 15, 20, 20, 15,  0,-30,
		-30,  5, 15, 20, 20, 15,  5,-30,
		-30,  0, 10, 15, 15, 10,  0,-30,
		-40,-20,  0,  0,  0,  0,-20,-40,
		-50,-40,-30,-30,-30,-30,-40,-50]

		self.__bishopstable = [
		-20,-10,-10,-10,-10,-10,-10,-20,
		-10,  5,  0,  0,  0,  0,  5,-10,
		-10, 10, 10, 10, 10, 10, 10,-10,
		-10,  0, 10, 10, 10, 10,  0,-10,
		-10,  5,  5, 10, 10,  5,  5,-10,
		-10,  0,  5, 10, 10,  5,  0,-10,
		-10,  0,  0,  0,  0,  0,  0,-10,
		-20,-10,-10,-10,-10,-10,-10,-20]

		self.__rookstable = [
		0,  0,  0,  5,  5,  0,  0,  0,
		-5,  0,  0,  0,  0,  0,  0, -5,
		-5,  0,  0,  0,  0,  0,  0, -5,
		-5,  0,  0,  0,  0,  0,  0, -5,
		-5,  0,  0,  0,  0,  0,  0, -5,
		-5,  0,  0,  0,  0,  0,  0, -5,
		5, 10, 10, 10, 10, 10, 10,  5,
		0,  0,  0,  0,  0,  0,  0,  0]

		self.__queenstable = [
		-20,-10,-10, -5, -5,-10,-10,-20,
		-10,  0,  0,  0,  0,  0,  0,-10,
		-10,  5,  5,  5,  5,  5,  0,-10,
		0,  0,  5,  5,  5,  5,  0, -5,
		-5,  0,  5,  5,  5,  5,  0, -5,
		-10,  0,  5,  5,  5,  5,  0,-10,
		-10,  0,  0,  0,  0,  0,  0,-10,
		-20,-10,-10, -5, -5,-10,-10,-20]

		self.__kingstable = [
		20, 30, 10,  0,  0, 10, 30, 20,
		20, 20,  0,  0,  0,  0, 20, 20,
		-10,-20,-20,-20,-20,-20,-20,-10,
		-20,-30,-30,-40,-40,-30,-30,-20,
		-30,-40,-40,-50,-50,-40,-40,-30,
		-30,-40,-40,-50,-50,-40,-40,-30,
		-30,-40,-40,-50,-50,-40,-40,-30,
		-30,-40,-40,-50,-50,-40,-40,-30]

	def __evaluateBoard(self):
		if self.__board.is_checkmate():
			if self.__board.turn:
				return -9999
			else:
				return 9999
		if self.__board.is_stalemate():
			return 0
		if self.__board.is_insufficient_material():
			return 0
		
		wp = len(self.__board.pieces(chess.PAWN, chess.WHITE))
		bp = len(self.__board.pieces(chess.PAWN, chess.BLACK))
		wn = len(self.__board.pieces(chess.KNIGHT, chess.WHITE))
		bn = len(self.__board.pieces(chess.KNIGHT, chess.BLACK))
		wb = len(self.__board.pieces(chess.BISHOP, chess.WHITE))
		bb = len(self.__board.pieces(chess.BISHOP, chess.BLACK))
		wr = len(self.__board.pieces(chess.ROOK, chess.WHITE))
		br = len(self.__board.pieces(chess.ROOK, chess.BLACK))
		wq = len(self.__board.pieces(chess.QUEEN, chess.WHITE))
		bq = len(self.__board.pieces(chess.QUEEN, chess.BLACK))
		
		material = 100*(wp-bp)+320*(wn-bn)+330*(wb-bb)+500*(wr-br)+900*(wq-bq)
		
		pawnsq = sum([self.__pawntable[i] for i in self.__board.pieces(chess.PAWN, chess.WHITE)])
		pawnsq= pawnsq + sum([-self.__pawntable[chess.square_mirror(i)] 
										for i in self.__board.pieces(chess.PAWN, chess.BLACK)])
		knightsq = sum([self.__knightstable[i] for i in self.__board.pieces(chess.KNIGHT, chess.WHITE)])
		knightsq = knightsq + sum([-self.__knightstable[chess.square_mirror(i)] 
										for i in self.__board.pieces(chess.KNIGHT, chess.BLACK)])
		bishopsq= sum([self.__bishopstable[i] for i in self.__board.pieces(chess.BISHOP, chess.WHITE)])
		bishopsq= bishopsq + sum([-self.__bishopstable[chess.square_mirror(i)] 
										for i in self.__board.pieces(chess.BISHOP, chess.BLACK)])
		rooksq = sum([self.__rookstable[i] for i in self.__board.pieces(chess.ROOK, chess.WHITE)]) 
		rooksq = rooksq + sum([-self.__rookstable[chess.square_mirror(i)] 
										for i in self.__board.pieces(chess.ROOK, chess.BLACK)])
		queensq = sum([self.__queenstable[i] for i in self.__board.pieces(chess.QUEEN, chess.WHITE)]) 
		queensq = queensq + sum([-self.__queenstable[chess.square_mirror(i)] 
										for i in self.__board.pieces(chess.QUEEN, chess.BLACK)])
		kingsq = sum([self.__kingstable[i] for i in self.__board.pieces(chess.KING, chess.WHITE)]) 
		kingsq = kingsq + sum([-self.__kingstable[chess.square_mirror(i)] 
										for i in self.__board.pieces(chess.KING, chess.BLACK)])
		
		eval = material + pawnsq + knightsq + bishopsq+ rooksq+ queensq + kingsq
		if self.__board.turn:
			return eval
		else:
			return -eval
	
	def __alphabeta(self, alpha, beta, depthleft):
		bestscore = -9999
		if(depthleft == 0):
			return self.__quiesce(alpha, beta)
		for move in self.__board.legal_moves:
			self.__board.push(move)   
			score = -self.__alphabeta(-beta, -alpha, depthleft - 1)
			self.__board.pop()
			if(score >= beta):
				return score
			if(score > bestscore):
				bestscore = score
			if(score > alpha):
				alpha = score   
		return bestscore

	def __quiesce(self, alpha, beta):
		stand_pat = self.__evaluateBoard()
		if(stand_pat >= beta):
			return beta
		if(alpha < stand_pat):
			alpha = stand_pat

		for move in self.__board.legal_moves:
			if self.__board.is_capture(move):
				self.__board.push(move)        
				score = -self.__quiesce(-beta, -alpha)
				self.__board.pop()

				if(score >= beta):
					return beta
				if(score > alpha):
					alpha = score  
		return alpha

	def __selectmove(self, depth):
		bestMove = chess.Move.null()
		bestValue = -99999
		alpha = -100000
		beta = 100000
		for move in self.__board.legal_moves:
			self.__board.push(move)
			boardValue = -self.__alphabeta(-beta, -alpha, depth-1)
			if boardValue > bestValue:
				bestValue = boardValue
				bestMove = move
			if(boardValue > alpha):
				alpha = boardValue
			self.__board.pop()
		return bestMove

	def __isLegalMove(self, move)->bool:
		"""
		Checks if the given move is a legal move
		"move" must be in UCI notation and of type "chess.Move" ( e.g.: chess.Move.from_uci("e2e4") )
		"""
		return move in self.__board.legal_moves


################################################################
# Puplic methods for the user
################################################################

	def setBoardFromFen(self, fen:str)->None:
		"""
		Setup the board from the given 'fen'
		"""
		self.__board.set_board_fen(fen)

	def boardAsFen(self)->str:
		"""
		Returns the current board as fen string
		"""
		return self.__board.fen()

	def makeComputerMove(self, depth:int=3)->bool:
		"""
		Let the ai make a move.

		Returns True if the given move can be performed otherwise False

		'depth' is the amount of look ahead moves for each possible move.
		Be aware that higher values (4+) inceases the compute time tremendously
		"""
		if depth < 1: depth = 1
		if depth > 4: depth = 4
		mov = self.__selectmove(depth)
		if not self.__isLegalMove(mov): return False
		self.__board.push(mov)
		return True

	def makeHumanMove(self, move:str)->bool:
		"""
		Make a manual move according to the given 'move'.

		'move' must be in uci notation (eg.: e2e4)
		Returns True if the given move can be performed otherwise False
		"""
		if not self.isLegalMove(move): return False
		mov = chess.Move.from_uci(move)
		self.__board.push(mov)
		return True

	def undoMove(self)->None:
		"""
		Undo the last move and remove it from the history
		"""
		self.__board.pop()

	def peekBestNextMove(self, depth:int=3)->str:
		"""
		Returns the move that is considered to be the best
		without changing the board.
		Returned move is in UCI notation as string e.g.: "e2e4"

		'depth' is the amount of look ahead moves for each possible move.
		Be aware that higher values (4+) inceases the compute time tremendously
		"""
		if depth < 1: depth = 1
		if depth > 4: depth = 4
		return str(self.__selectmove(depth))

	def moveHistory(self)->List[str]:
		"""
		Returns a list of already made moves in UCI notation
		e.g.: ['e2e4', 'g8f6', 'b1c3']
		"""
		moves = [str(mov) for mov in self.__board.move_stack]
		return moves

	def lastMove(self)->str:
		"""
		Returns the last move made.
		Returned move is in UCI notation as string e.g.: "e2e4"
		"""
		last = self.__board.peek()
		return str(last)

	def isLegalMove(self, move:str)->bool:
		"""
		Checks if the given move is a legal move
		'move must be in UCI notation and of type string ("e2e4")
		"""
		return self.__isLegalMove(chess.Move.from_uci(move))

	def isCheckmate(self)->bool:
		"""
		Returns if the current side to move is in checkmate.
		"""
		return self.__board.is_checkmate()

	def isStalemate(self)->bool:
		"""
		Returns if the current side to move is in stalemate.
		"""
		return self.__board.is_stalemate()

	def isInsufficientMaterial(self)->bool:
		"""
		Returns if the current side to move has insufficient material.
		"""
		return self.__board.is_insufficient_material()

	def isGameOver(self):
		"""
		Checks if the game is over for the current side to move due to checkmate, stalemate, insufficient material,
		seventyfive-move rule, fivefold repetition , fifty-move rule or threefold repetition.
		"""
		return self.__board.is_game_over(claim_draw=True)

	def isInCheck(self)->bool:
		"""
		Returns if the current side to move is in check.
		"""
		return self.__board.is_check()

	def isIntoCheck(self, move:str)->bool:
		"""
		Checks if the given move would leave the king of the current side to move in check or put it into check.
		The move must be legal and in UCI notation e.g.: "e2e4".
		"""
		if not self.isLegalMove(move):
			print(f"Illegal move '{move}'!")
			return False
		return self.__board.is_into_check(chess.Move.from_uci(move))

	def turn(self)->bool:
		"""
		True: white's turn
		False: black's turn
		"""
		return self.__board.turn

	def reset(self)->None:
		"""
		Resets piece positions to the starting position and
		clears the move stack (moveHistory)
		"""
		self.__board.reset_board()

	def dumpBoard(self, newline=True)->None:
		"""
		Prints the board to the console.
		'newline' determines if a new line character should
		be appended at the end.
		"""
		nl = "\n" if newline else ""
		print(f"{self.__board}{nl}")
