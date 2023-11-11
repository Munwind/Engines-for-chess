import random

DEPTH = 4
MIN_SCORE = -100000
MAX_SCORE = 100000
DRAW = 0

pieceScores = {'p' : 100, 'N' : 300, 'B' : 320, 'R' : 500, 'Q' : 900, 'K' : 0}

# Points for pawn position
whitePawnStart = [[  0,  0,  0,  0,  0,  0,  0,  0],
                  [ 50, 50, 50, 50, 50, 50, 50, 50],
                  [ 10, 10, 20, 30, 30, 20, 10, 10],
                  [  5,  5, 10, 25, 25, 10,  5,  5],
                  [  0,  0,  0, 20, 20,  0,  0,  0],
                  [  5, -5,-10,  0,  0,-10, -5,  5],
                  [  5, 10, 10,-20,-20, 10, 10,  5],
                  [  0,  0,  0,  0,  0,  0,  0,  0]]

blackPawnStart = [[  0,  0,  0,  0,  0,  0,  0,  0],
                  [  5, 10, 10,-20,-20, 10, 10,  5],
                  [  5, -5,-10,  0,  0,-10, -5,  5],
                  [  0,  0,  0, 20, 20,  0,  0,  0],
                  [  5,  5, 10, 25, 25, 10,  5,  5],
                  [ 10, 10, 20, 30, 30, 20, 10, 10],
                  [ 50, 50, 50, 50, 50, 50, 50, 50],
                  [  0,  0,  0,  0,  0,  0,  0,  0]]

whitePawnEnd = [[  0,  0,  0,  0,  0,  0,  0,  0],
                [ 80, 80, 80, 80, 80, 80, 80, 80],
                [ 50, 50, 50, 50, 50, 50, 50, 50],
                [ 30, 30, 30, 30, 30, 30, 30, 30],
                [ 20, 20, 20, 20, 20, 20, 20, 20],
                [ 10, 10, 10, 10, 10, 10, 10, 10],
                [ 10, 10, 10, 10, 10, 10, 10, 10],
                [  0,  0,  0,  0,  0,  0,  0,  0]]

blackPawnEnd = [[  0,  0,  0,  0,  0,  0,  0,  0],
                [ 10, 10, 10, 10, 10, 10, 10, 10],
                [ 10, 10, 10, 10, 10, 10, 10, 10],
                [ 20, 20, 20, 20, 20, 20, 20, 20],
                [ 30, 30, 30, 30, 30, 30, 30, 30],
                [ 50, 50, 50, 50, 50, 50, 50, 50],
                [ 80, 80, 80, 80, 80, 80, 80, 80],
                [  0,  0,  0,  0,  0,  0,  0,  0]]

# Points for Kinght position
whiteKinghtScore = [[-50, -40, -30, -30, -30, -30, -40, -50],
                    [-40, -20,   0,   0,   0,   0, -20, -40],
                    [-30,   0,  10,  15,  15,  10,   0, -30],
                    [-30,   5,  15,  20,  20,  15,   5, -30],
                    [-30,   0,  15,  20,  20,  15,   0, -30],
                    [-30,   5,  10,  15,  15,  10,   5, -30],
                    [-40, -20,   0,   5,   5,   0, -20, -40],
                    [-50, -40, -30, -30, -30, -30, -40, -50]]

blackKinghtScore = [[-50, -40, -30, -30, -30, -30, -40, -50],
                    [-40, -20,   0,   5,   5,   0, -20, -40],
                    [-30,   5,  10,  15,  15,  10,   5, -30],
                    [-30,   0,  15,  20,  20,  15,   0, -30],
                    [-30,   5,  15,  20,  20,  15,   5, -30],
                    [-30,   0,  10,  15,  15,  10,   0, -30],
                    [-40, -20,   0,   0,   0,   0, -20, -40],
                    [-50, -40, -30, -30, -30, -30, -40, -50]]

# Points for King position
whiteKingStart = [[-80, -70, -70, -70, -70, -70, -70, -80],
                  [-60, -60, -60, -60, -60, -60, -60, -60],
                  [-40, -50, -50, -60, -60, -50, -50, -40],
                  [-30, -40, -40, -50, -50, -40, -40, -30],
                  [-20, -30, -30, -40, -40, -30, -30, -20],
                  [-10, -20, -20, -20, -20, -20, -20, -10],
                  [ 20,  20,  -5,  -5,  -5,  -5,  20,  20],
                  [ 20,  30,  10,   0,   0,  10,  30,  20]]

blackKingStart = [[ 20,  30,  10,   0,   0,  10,  30,  20],
                  [ 20,  20,  -5,  -5,  -5,  -5,  20,  20],
                  [-10, -20, -20, -20, -20, -20, -20, -10],
                  [-20, -30, -30, -40, -40, -30, -30, -20],
                  [-30, -40, -40, -50, -50, -40, -40, -30],
                  [-40, -50, -50, -60, -60, -50, -50, -40],
                  [-60, -60, -60, -60, -60, -60, -60, -60],
                  [-80, -70, -70, -70, -70, -70, -70, -80]]

whiteKingEnd = [[-20, -10, -10, -10, -10, -10, -10, -20],
                [ -5,   0,   5,   5,   5,   5,   0,  -5],
                [-10,  -5,  20,  30,  30,  20,  -5, -10],
                [-15, -10,  35,  45,  45,  35, -10, -15],
                [-20, -15,  30,  40,  40,  30, -15, -20],
                [-25, -20,  20,  25,  25,  20, -20, -25],
                [-30, -25,   0,   0,   0,   0, -25, -30],
                [-50, -30, -30, -30, -30, -30, -30, -50]]

blackKingEnd = [[-50, -30, -30, -30, -30, -30, -30, -50],
                [-30, -25,   0,   0,   0,   0, -25, -30],
                [-25, -20,  20,  25,  25,  20, -20, -25],
                [-20, -15,  30,  40,  40,  30, -15, -20],
                [-15, -10,  35,  45,  45,  35, -10, -15],
                [-10,  -5,  20,  30,  30,  20,  -5, -10],
                [ -5,   0,   5,   5,   5,   5,   0,  -5],
                [-20, -10, -10, -10, -10, -10, -10, -20],]

# Points for Queen position
queenScore = [[-50,-30,-30,-10,-10,-30,-30,-50],
              [-30, 10, 10, 10, 10, 10, 10,-30],
              [-30, 10, 20, 20, 20, 20, 10,-30],
              [-10, 10, 20, 30, 30, 20, 10,-10],
              [-10, 10, 20, 30, 30, 20, 10,-10],
              [-30, 10, 20, 20, 20, 20, 10,-30],
              [-30, 10, 10, 10, 10, 10, 10,-30],
              [-50,-30,-30,-10,-10,-30,-30,-50]]

# Points for Rook position
whiteRookScore = [[ 10, 10, 10, 10, 10, 10, 10, 10],
                  [ 20, 50, 50, 50, 50, 50, 50, 20],
                  [-40,-20,-20,-20,-20,-20,-20,-20],
                  [-40,-20,-20,-20,-20,-20,-20,-20],
                  [-40,-20,-20,-20,-20,-20,-20,-20],
                  [-40,-20,-20,-20,-20,-20,-20,-20],
                  [-40,-20,-20,-20,-20,-20,-20,-20],
                  [-20,-20,  0, 20, 20,  0,-20,-20]]

blackRookScore = [[-20,-20,  0, 20, 20,  0,-20,-20],
                  [-40,-20,-20,-20,-20,-20,-20,-20],
                  [-40,-20,-20,-20,-20,-20,-20,-20],
                  [-40,-20,-20,-20,-20,-20,-20,-20],
                  [-40,-20,-20,-20,-20,-20,-20,-20],
                  [-40,-20,-20,-20,-20,-20,-20,-20],
                  [ 20, 50, 50, 50, 50, 50, 50, 20],
                  [ 10, 10, 10, 10, 10, 10, 10, 10]]

# Points for Bishop position
bishopScore = [[-40,-20,-20,-20,-20,-20,-20,-40],
               [-20, 10, 10, 10, 10, 10, 10,-20],
               [-20, 10, 20, 30, 30, 20, 10,-20],
               [-20, 20, 30, 40, 40, 30, 20,-20],
               [-20, 20, 30, 40, 40, 30, 20,-20],
               [-20, 10, 20, 30, 30, 20, 10,-20],
               [-20, 10, 10, 10, 10, 10, 10,-20],
               [-40,-20,-20,-20,-20,-20,-20,-40]]

def getRandomMoves(possibleMoves):
    if len(possibleMoves) > 0:
        return possibleMoves[random.randint(0, len(possibleMoves) - 1)]

def findMove(gs, possibleMoves):
    global bestMove
    bestMove = None
    random.shuffle(possibleMoves)
    if gs.numOfMoves == 0 or gs.numOfMoves == 1:
        bestMove = getRandomMoves(possibleMoves)
    else:
        minimax(gs, possibleMoves, MIN_SCORE, MAX_SCORE, DEPTH)
    
    return bestMove
    
def minimax(gs, possibleMoves, alpha, beta, currentDepth):
    global bestMove
    
    if currentDepth == 0:
        return Evaluate(gs)

    maxScore = MIN_SCORE
    
    for move in possibleMoves:
        gs.makeMove(move)
        nextMoves = gs.getPossibleMoves()
        score = -minimax(gs, nextMoves, -beta, -alpha, currentDepth - 1)
        
        if score > maxScore:
            maxScore = score
            if currentDepth == DEPTH:
                bestMove = move
        gs.unMakeMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    
    return maxScore
    
def Evaluate(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return MIN_SCORE
        else:
            return MAX_SCORE
    if gs.staleMate:
        return DRAW
    
    score = 0
    for row in range(8):
        for col in range(8):
            square = gs.board[row][col]
            
            if square != '--':
                piecePositionScore = 0
                
                # Solve for the pawn
                if square == 'wp':
                    if gs.numOfMoves < 25:
                        piecePositionScore = whitePawnStart[row][col]
                    else:
                        piecePositionScore = whitePawnEnd[row][col]
                elif square == 'bp':
                    if gs.numOfMoves < 25:
                        piecePositionScore = blackPawnStart[row][col]
                    else:
                        piecePositionScore = blackPawnEnd[row][col]
                        
                # Solve for the king
                elif square == 'wK':
                    if gs.numOfMoves < 25:
                        piecePositionScore = whiteKingStart[row][col]
                    else:
                        piecePositionScore = whiteKingEnd[row][col]

                elif square == 'bK':
                    if gs.numOfMoves < 25:
                        piecePositionScore = blackKingStart[row][col]
                    else:
                        piecePositionScore = blackKingEnd[row][col]
                
                # Solve for the knight
                elif square == 'wN':
                    piecePositionScore = whiteKinghtScore[row][col]
                
                elif square == 'bN':
                    piecePositionScore = blackKinghtScore[row][col]
                    
                # Solve for the rook
                elif square == 'wR':
                    piecePositionScore = whiteRookScore[row][col]
                
                elif square == 'bR':
                    piecePositionScore = blackRookScore[row][col]
                
                # Solve for the queen
                elif square[1] == 'Q':
                    piecePositionScore = queenScore[row][col]
                
                # Solve for the bishop
                elif square[1] == 'B':
                    piecePositionScore = bishopScore[row][col]
                
                    
                if square[0] == 'w':
                    score += pieceScores[square[1]] + piecePositionScore
                elif square[0] == 'b':
                    score -= pieceScores[square[1]] + piecePositionScore
    if not gs.whiteToMove:
        score *= -1
        
    return score