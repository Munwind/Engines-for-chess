import pygame as p
import chessAI
import chessMoves
import time

BOARD_SIZE = 560
DIMENTION = 8 # 8*8 CHESS BOARD
CELL_SIZE = BOARD_SIZE // DIMENTION
MAX_FPS = 12
IMAGES = {}
DISPLACEMENT = 0


p.display.set_caption("CHESS")
def loadImages():
	pieces = ['bp', 'bR', 'bN', 'bB', 'bQ', 'bK', 'wp', 'wR', 'wN', 'wB', 'wQ', 'wK']
	for piece in pieces:
        # Make sure you have a correct path to the images folder
		IMAGES[piece] = p.transform.scale(p.image.load("Engines-for-chess/images/" + piece + ".png"), (CELL_SIZE, CELL_SIZE ) )  


def main():
    p.init()
    screen = p.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    clock = p.time.Clock()
    gs = chessMoves.GameState()
    loadImages()
    
    animationCheck = False
    moveMade = False
    running = True
    sqSelected = ()
    playerClicks = []
    possibleMoves = gs.getPossibleMoves()
    
    isMate = False
    humanPlayWhite = False
    humanPlayBlack = False
    
    while running:
        humanToPlay = (gs.whiteToMove and humanPlayWhite) or (not gs.whiteToMove and humanPlayBlack)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not isMate and humanToPlay:
                    location = p.mouse.get_pos()  
                    col = location[0] // CELL_SIZE
                    row = location[1] // CELL_SIZE
                    if sqSelected == (row, col):  
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)  
                        if len(playerClicks) == 2:  
                            move = chessMoves.Move(playerClicks[0], playerClicks[1], gs.board)
                            for i in range(len(possibleMoves)):
                                if move == possibleMoves[i]:
                                    gs.makeMove(move)
                                    if gs.isDrawByRepetition():
                                        gs.draw = True
                                    moveMade = True
                                    animationCheck = True
                                    sqSelected = () 
                                    playerClicks = []
                                    
                            if not moveMade:
                                playerClicks = [sqSelected]
    
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.unMakeMove()
                    moveMade = True
                    isMate = False
                    animationCheck = False
                    
        if not isMate and not humanToPlay:
            startTime = time.time()
            AI_move = chessAI.getTheMove(gs, possibleMoves)
            endTime = time.time()
            executionTime = endTime - startTime
            print(f"It took {executionTime} to run")
            if AI_move == None:
                AI_move = chessAI.getRandomMoves(possibleMoves)
            gs.makeMove(AI_move)
            if gs.isDrawByRepetition():
                gs.draw = True
            moveMade = True    
            animationCheck = True

        if moveMade:
            if animationCheck:
                animationCheck = False
                animate(gs.moveLog[-1], screen, gs.board, clock)
            possibleMoves = gs.getPossibleMoves()
            moveMade = False
            
        drawGameState(screen, gs, possibleMoves, sqSelected)
        
        if gs.checkMate:
            isMate = True
            if gs.whiteToMove:
                draw_text(screen, "Black wins by checkmate")
            else:
                draw_text(screen, "White wins by checkmate")
            
        elif gs.staleMate:
            isMate = True
            draw_text(screen, "Draw by stalemate")
        
        elif gs.draw:
            isMate = True
            draw_text(screen, "Draw by repetitions")
            
        clock.tick(MAX_FPS)
        p.display.flip()

'''
responsible for all the graphics in the game
'''
                    
def drawGameState(screen, gs, possibleMoves, sqSelected):
    drawBoard(screen)
    displayLastMove(screen, gs)
    hightlightSquare(screen, gs, possibleMoves, sqSelected)
    hightlightChecks(screen, gs)
    drawPieces(screen, gs.board)


'''
draw the squares on the board
'''
def drawBoard(screen):
    global colors
    colors = [p.Color('white'), p.Color('gray')]
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(CELL_SIZE*c, CELL_SIZE*r , CELL_SIZE, CELL_SIZE))

'''
draw the pieces on the board using ChessEngine.GameState.board.
'''
def drawPieces(screen, board):
	for r in range(DIMENTION):
		for c in range(DIMENTION):
			piece = board[r][c]
			if piece != '--':
				screen.blit(IMAGES[piece], p.Rect(CELL_SIZE*c, CELL_SIZE*r , CELL_SIZE, CELL_SIZE))

def draw_text(screen ,string):
    font = p.font.SysFont('Helvitica', 50, True, False)
    textObject = font.render(string, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, BOARD_SIZE, BOARD_SIZE).move(BOARD_SIZE / 2 - textObject.get_width() / 2, BOARD_SIZE / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)

def animate(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framePerSquare = 8
    
    frameCount = (abs(dR) + abs(dC)) * framePerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame/frameCount, move.startCol + dC * frame / frameCount) 
        drawBoard(screen)
        drawPieces(screen, board)
        
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * CELL_SIZE, move.endRow * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        p.draw.rect(screen, color, endSquare)
        
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, BOARD_SIZE))
        p.display.flip()
        clock.tick(60)


def hightlightSquare(screen, gs, possibleMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if (gs.board[r][c][0] == 'w' and gs.whiteToMove) or (gs.board[r][c][0] == 'b' and not gs.whiteToMove):
            s = p.Surface((CELL_SIZE, CELL_SIZE))
            s.set_alpha(70)
            s.fill(p.Color('blue'))
            screen.blit(s, (c * CELL_SIZE, r * CELL_SIZE))
            s.fill(p.Color('green'))
            
            for move in possibleMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (CELL_SIZE * move.endCol, CELL_SIZE * move.endRow))
                    
def hightlightChecks(screen, gs):
    r, c = -1, -1
    if gs.whiteToMove:
        if gs.isAttacked(gs.whiteKingLocation[0], gs.whiteKingLocation[1]):
            r, c = gs.whiteKingLocation
    else:
        if gs.isAttacked(gs.blackKingLocation[0], gs.blackKingLocation[1]):
            r, c = gs.blackKingLocation
    
    if r != -1 and c != -1:
        s = p.Surface((CELL_SIZE, CELL_SIZE))
        s.fill(p.Color('red'))
        screen.blit(s, (c * CELL_SIZE, r * CELL_SIZE))

def displayLastMove(screen, gs):
    if len(gs.moveLog) != 0:
        startRow = gs.moveLog[-1].startRow
        startCol = gs.moveLog[-1].startCol
        endRow = gs.moveLog[-1].endRow
        endCol = gs.moveLog[-1].endCol
        
        s = p.Surface((CELL_SIZE, CELL_SIZE))
        s.fill(p.Color('light yellow'))
        screen.blit(s, (startCol * CELL_SIZE, startRow * CELL_SIZE))
        
        s.fill(p.Color('yellow'))
        screen.blit(s, (endCol * CELL_SIZE, endRow * CELL_SIZE))
        
if __name__ == '__main__':
	main()
