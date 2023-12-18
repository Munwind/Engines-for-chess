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
                  [ 20,  60,  10,   0,   0,  10,  60,  20]]

blackKingStart = [[ 20,  60,  10,   0,   0,  10,  60,  20],
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
               [-20, 10, 20, 10, 10, 20, 10,-20],
               [-20, 20, 30, 40, 40, 30, 20,-20],
               [-20, 20, 30, 40, 40, 30, 20,-20],
               [-20, 10, 20, 10, 10, 20, 10,-20],
               [-20, 10, 10, 10, 10, 10, 10,-20],
               [-40,-20,-20,-20,-20,-20,-20,-40]]

def getRandomMoves(possibleMoves):
    if len(possibleMoves) > 0:
        return possibleMoves[random.randint(0, len(possibleMoves) - 1)]

def getTheMove(gs, possibleMoves): # Get the AI move through this
    check = isEndGame(gs)
    if check < 0:
        return getBestMove(gs, possibleMoves)
    else:  # this is the end game
        print("This is endgame")
        return getMoveLateGame(gs, possibleMoves)


def getBestMove(gs, possibleMoves):
    best_move = None
    best_eval = MIN_SCORE
    
    if gs.numOfMoves < 2:
        return best_move
    possibleMoves = orderMoves(gs, possibleMoves)
    for move in possibleMoves:
        gs.makeMove(move)
        newMoves = orderMoves(gs, gs.getPossibleMoves())
        evalScore = -minimax(gs, newMoves, MIN_SCORE, -best_eval, DEPTH - 1)
        gs.unMakeMove()
        
        if evalScore > best_eval:
            best_eval = evalScore
            best_move = move
            if best_eval == MAX_SCORE:
                return best_move
    if best_move is None:
        print("No good moves")
    return best_move

def getMoveLateGame(gs, possibleMoves):
    best_move = None
    best_eval = MIN_SCORE
    
    possibleMoves = orderMoves(gs, possibleMoves)
    depth = 1
    while depth <= DEPTH:
        for move in possibleMoves:
            gs.makeMove(move)
            newMoves = orderMoves(gs, gs.getPossibleMoves())
            evalScore = -minimaxEndGame(gs, newMoves, MIN_SCORE, -best_eval, depth - 1)
            gs.unMakeMove()
            
            if evalScore == MAX_SCORE:
                return move
            
            if depth == 4:
                if evalScore > best_eval:
                    best_eval = evalScore
                    best_move = move
                    if best_eval == MAX_SCORE:
                        return best_move
        depth += 1
        
    return best_move

def minimax(gs, possibleMoves, alpha, beta, currentDepth):
    if currentDepth == 0:
        return quiesenceSearch(gs, alpha, beta)
    
    if gs.checkMate:
        return MIN_SCORE
    elif gs.staleMate or gs.isDrawByRepetition():
        return 0
    
    maxScore = MIN_SCORE
    
    for move in possibleMoves:
        gs.makeMove(move)
        nextMoves = gs.getPossibleMoves()
        nextMoves = orderMoves(gs, nextMoves)
        score = -minimax(gs, nextMoves, -beta, -alpha, currentDepth - 1)
        gs.unMakeMove()

        if score > maxScore:
            maxScore = score
        alpha = max(alpha, maxScore)
        if alpha >= beta:
            break
    
    return maxScore

def minimaxEndGame(gs, possibleMoves, alpha, beta, currentDepth):
    if currentDepth == 0:
        return evalForEndGame(gs)
    
    if gs.checkMate:
        return MIN_SCORE
    elif gs.staleMate or gs.isDrawByRepetition():
        return 0
    
    maxScore = MIN_SCORE
    
    for move in possibleMoves:
        gs.makeMove(move)
        nextMoves = gs.getPossibleMoves()
        score = -minimaxEndGame(gs, nextMoves, -beta, -alpha, currentDepth - 1)
        gs.unMakeMove()
        
        if score > maxScore:
            maxScore = score
        alpha = max(alpha, maxScore)
        if alpha >= beta:
            break
    
    return maxScore

def quiesenceSearch(gs, alpha, beta):
    evaluation = Evaluate(gs)
    if evaluation >= beta:
        return beta
    alpha = max(alpha, evaluation)
    
    temp_moves = gs.getPossibleMoves()
    moves = []
    
    for move in temp_moves:
        if move.pieceCaptured != '--':
            moves.append(move)
    
    moves = orderMoves(gs, moves)
    
    for move in moves:
        gs.makeMove(move)
        evaluation = -quiesenceSearch(gs, -beta, -alpha)
        gs.unMakeMove()
        
        if evaluation >= beta:
            return beta
        alpha = max(alpha, evaluation)
    
    return alpha

# Order the moves to make alpha beta prunning more efficient
def orderMoves(gs, possibleMoves):
    orderedMoves = []
    captureMoves = []
    nonCaptureMoves = []
    
    for move in possibleMoves:
        if move.pieceCaptured != '--':  
            captureMoves.append(move)
        else:
            nonCaptureMoves.append(move)

    captureMoves.sort(key=lambda move : captureMoveValue(move))
    
    orderedMoves.extend(captureMoves)
    orderedMoves.extend(nonCaptureMoves)
    
    return orderedMoves
    
def captureMoveValue(move):
    return pieceScores[move.pieceMoved[1]] - pieceScores[move.pieceCaptured[1]]

def evalForEndGame(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return MIN_SCORE
        else:
            return MAX_SCORE
        
    if gs.staleMate or gs.isDrawByRepetition():
        point = getMaterial(gs.board)
        if point == 0:
            if gs.whiteToMove:
                return 0
            else:
                return 0
            
        if gs.whiteToMove:
            return point
        else:
            return point
        
    friendlyKingRow = 0
    friendlyKingCol = 0
    enemyKingRow = 0
    enemyKingCol = 0
    endGameWeight = isEndGame(gs) // 2
    
    # Store the position of white king and black king as friendlyKing and enemyKing
    if gs.whiteToMove:
        friendlyKingRow, friendlyKingCol = gs.whiteKingLocation
        enemyKingRow, enemyKingCol = gs.blackKingLocation
    else:
        friendlyKingRow, friendlyKingCol = gs.blackKingLocation
        enemyKingRow, enemyKingCol = gs.whiteKingLocation
    
    # Start to count the eval value
    eval = 0
    
    # Increase eval if the enemy king is in the corner of the board
    enemyKingDistanceToCentreRow = max(abs(enemyKingRow - 3), abs(enemyKingRow - 4))
    enemyKingDistanceToCentreCol = max(abs(enemyKingCol - 3), abs(enemyKingCol - 4)) 
    enemyKingDistanceToCentre = enemyKingDistanceToCentreRow + enemyKingDistanceToCentreCol
    
    eval += enemyKingDistanceToCentre * (endGameWeight // 30)
    
    # Increase eval if the friendlyKing is near the enemyKing
    kingDistanceRow = abs(friendlyKingRow - enemyKingRow)
    kingDistanceCol = abs(friendlyKingCol - enemyKingCol)
    totalKingDistance = kingDistanceRow + kingDistanceCol
    
    eval += (14 - totalKingDistance) * (endGameWeight // 30)
    
    score = scoreForEndGame(gs.board)
    
    if not gs.whiteToMove:
        score *= -1
    
    return eval + score
    

def isEndGame(gs): # return positive => ebd game happens , negative otherwise
    blackScore = 0
    whiteScore = 0
    
    for row in gs.board:
        for col in row:
            if col[0] == 'w':
                whiteScore += pieceScores[col[1]]
            elif col[0] == 'b':
                blackScore += pieceScores[col[1]]
    
    totalScore = whiteScore + blackScore
    return 2300 - totalScore

def Evaluate(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return MIN_SCORE
        else:
            return MAX_SCORE
        
    if gs.staleMate or gs.isDrawByRepetition():
        point = getMaterial(gs.board)
        if point == 0:
            if gs.whiteToMove:
                return -10
            else:
                return 10
            
        if gs.whiteToMove:
            return point
        else:
            return point
    
    score = 0
    for row in range(8):
        for col in range(8):
            square = gs.board[row][col]
            
            if square != '--':
                piecePositionScore = 0
                
                # Solve for the pawn
                if square == 'wp':
                    if gs.numOfMoves < 65:
                        piecePositionScore = whitePawnStart[row][col]
                    else:
                        piecePositionScore = whitePawnEnd[row][col]
                elif square == 'bp':
                    if gs.numOfMoves < 65:
                        piecePositionScore = blackPawnStart[row][col]
                    else:
                        piecePositionScore = blackPawnEnd[row][col]
                        
                # Solve for the king
                elif square == 'wK':
                    if gs.numOfMoves < 65:
                        piecePositionScore = whiteKingStart[row][col]
                    else:
                        piecePositionScore = whiteKingEnd[row][col]

                elif square == 'bK':
                    if gs.numOfMoves < 65:
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

def getMaterial(board):
    score = 0
    for row in board:
        for col in row:
            if col[0] == 'w':
                score += pieceScores[col[1]]
            elif col[0] == 'b':
                score -= pieceScores[col[1]]
    return score 

def scoreForEndGame(board):
    score = 0
    for row in range(8):
        for col in range(8):
            square = board[row][col]

            if square != '--':
                piecePositionScore = 0
                
                # Solve for the pawn
                if square == 'wp':
                    piecePositionScore = whitePawnEnd[row][col]
                elif square == 'bp':
                    piecePositionScore = blackPawnEnd[row][col]
                        
                # Solve for the king
                elif square == 'wK':
                    piecePositionScore = whiteKingEnd[row][col]

                elif square == 'bK':
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
    
    return score