import random

DEPTH = 2
MIN_SCORE = -100000
MAX_SCORE = 100000
DRAW = 0

pieceScores = {'p' : 100, 'N' : 300, 'B' : 320, 'R' : 500, 'Q' : 900, 'K' : 0}

def getRandomMoves(possibleMoves):
    if len(possibleMoves) > 0:
        return possibleMoves[random.randint(0, len(possibleMoves) - 1)]
    
