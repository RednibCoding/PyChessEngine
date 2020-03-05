from chess.chessengine import ChessEngine

ce = ChessEngine()

ce.makeHumanMove(move="e2e4")
ce.dumpBoard()
ce.makeComputerMove(depth=3)
ce.dumpBoard()

history = ce.moveHistory()
print(history)
print(ce.peekBestNextMove(depth=3))
