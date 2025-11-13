import math, copy, time
import random as random_module
from PIL import Image as PILImage
import pygame
import os
import sys

# Initialize pygame
pygame.init()

# Color constants
COLORS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'gray': (128, 128, 128),
    'lightgray': (211, 211, 211),
    'lightblue': (173, 216, 230),
    'lightgreen': (144, 238, 144),
    'yellow': (255, 255, 0),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'orange': (255, 165, 0),
    'chartreuse': (127, 255, 0),
}

def fixAlpha(path):
    """Convert PNG to true RGBA format for proper transparency."""
    try:
        img = PILImage.open(path)
        if img.mode != 'RGBA':
            if img.mode == 'P' and 'transparency' in img.info:
                img = img.convert("RGBA")
            elif img.mode in ['RGB', 'L']:
                img = img.convert("RGBA")
            else:
                img = img.convert("RGBA")
        img.save(path, format='PNG', optimize=False)
    except Exception as e:
        print(f"Error fixing alpha for {path}: {e}")

# Pygame helper functions to mimic cmu_graphics API
class Game:
    """Game class to hold all game state (replaces app object)."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Chess Game")
        self.clock = pygame.time.Clock()
        self.fonts = {}  # Cache fonts
        self.images = {}  # Cache loaded images
        
    def get_font(self, name='Arial', size=16, bold=False, italic=False):
        """Get or create a font."""
        key = (name, size, bold, italic)
        if key not in self.fonts:
            try:
                # pygame.font.match_font doesn't support italic, so we handle it separately
                font_name = pygame.font.match_font(name, bold=bold)
                font_obj = pygame.font.Font(font_name, size)
                if italic:
                    font_obj.set_italic(True)
                self.fonts[key] = font_obj
            except:
                font_obj = pygame.font.Font(None, size)
                if italic:
                    font_obj.set_italic(True)
                self.fonts[key] = font_obj
        return self.fonts[key]
    
    def load_image(self, path):
        """Load and cache an image."""
        if path not in self.images:
            try:
                # Convert to RGBA for transparency
                img = pygame.image.load(path).convert_alpha()
                self.images[path] = img
            except Exception as e:
                print(f"Error loading image {path}: {e}")
                return None
        return self.images[path]
    
    def draw_rect(self, x, y, width, height, fill=None, border=None, borderWidth=0):
        """Draw a rectangle."""
        if fill:
            color = COLORS.get(fill, fill) if isinstance(fill, str) else fill
            pygame.draw.rect(self.screen, color, (x, y, width, height))
        if border and borderWidth > 0:
            border_color = COLORS.get(border, border) if isinstance(border, str) else border
            pygame.draw.rect(self.screen, border_color, (x, y, width, height), borderWidth)
    
    def draw_circle(self, x, y, radius, fill=None, border=None, borderWidth=0):
        """Draw a circle."""
        if fill:
            color = COLORS.get(fill, fill) if isinstance(fill, str) else fill
            pygame.draw.circle(self.screen, color, (int(x), int(y)), int(radius))
        if border and borderWidth > 0:
            border_color = COLORS.get(border, border) if isinstance(border, str) else border
            pygame.draw.circle(self.screen, border_color, (int(x), int(y)), int(radius), borderWidth)
    
    def draw_line(self, x1, y1, x2, y2, fill=None, lineWidth=1):
        """Draw a line."""
        if fill:
            color = COLORS.get(fill, fill) if isinstance(fill, str) else fill
            pygame.draw.line(self.screen, color, (int(x1), int(y1)), (int(x2), int(y2)), lineWidth)
    
    def draw_label(self, text, x, y, font='Arial', size=16, bold=False, italic=False, fill='black', align='center'):
        """Draw text label."""
        font_obj = self.get_font(font, size, bold, italic)
        color = COLORS.get(fill, fill) if isinstance(fill, str) else fill
        text_surface = font_obj.render(str(text), True, color)
        text_rect = text_surface.get_rect()
        
        if align == 'center':
            text_rect.center = (x, y)
        elif align == 'left':
            text_rect.left = x
            text_rect.top = y
        elif align == 'right':
            text_rect.right = x
            text_rect.top = y
        
        self.screen.blit(text_surface, text_rect)
    
    def draw_image(self, path, x, y, width=None, height=None, align='center'):
        """Draw an image."""
        img = self.load_image(path)
        if img is None:
            return
        
        # Scale if needed
        if width or height:
            original_width, original_height = img.get_size()
            if width and height:
                img = pygame.transform.scale(img, (int(width), int(height)))
            elif width:
                scale = width / original_width
                img = pygame.transform.scale(img, (int(width), int(original_height * scale)))
            elif height:
                scale = height / original_height
                img = pygame.transform.scale(img, (int(original_width * scale), int(height)))
        
        img_rect = img.get_rect()
        if align == 'center':
            img_rect.center = (x, y)
        elif align == 'left-top':
            img_rect.left = x
            img_rect.top = y
        
        self.screen.blit(img, img_rect)

# Global app variable for wrapper functions
_app_instance = None

def set_app_instance(app_instance):
    """Set the global app instance for drawing functions."""
    global _app_instance
    _app_instance = app_instance

# Wrapper functions to maintain compatibility with existing code
def drawRect(x, y, width, height, fill=None, border=None, borderWidth=0):
    if _app_instance:
        _app_instance.draw_rect(x, y, width, height, fill, border, borderWidth)

def drawCircle(x, y, radius, fill=None, border=None, borderWidth=0):
    if _app_instance:
        _app_instance.draw_circle(x, y, radius, fill, border, borderWidth)

def drawLine(x1, y1, x2, y2, fill=None, lineWidth=1):
    if _app_instance:
        _app_instance.draw_line(x1, y1, x2, y2, fill, lineWidth)

def drawLabel(text, x, y, font='Arial', size=16, bold=False, italic=False, fill='black', align='center'):
    if _app_instance:
        _app_instance.draw_label(text, x, y, font, size, bold, italic, fill, align)

def drawImage(path, x, y, width=None, height=None, align='center'):
    if _app_instance:
        _app_instance.draw_image(path, x, y, width, height, align)

# AI Functions

def evaluatePosition(app):
    """Evaluate the current position. Positive favors white, negative favors black."""
    value = 0
    
    # Material values only (fast evaluation, no expensive checks)
    pieceValues = {pawn: 1, knight: 3, bishop: 3, rook: 5, queen: 9, king: 0}
    
    for piece in app.whitepieces:
        value += pieceValues[type(piece)]
    
    for piece in app.blackpieces:
        value -= pieceValues[type(piece)]
    
    return value

def getAllValidMoves(app, color):
    """Get all valid moves for a given color."""
    pieces = app.whitepieces if color == 'white' else app.blackpieces
    allMoves = []
    
    for i, piece in enumerate(pieces):
        possibleMoves = piece.moves(app.plist)
        # Set prevclick temporarily to use actualMoves function
        originalPrevclick = app.prevclick
        app.prevclick = [piece.row, piece.col]
        validMoves = actualMoves(app, possibleMoves)
        app.prevclick = originalPrevclick
        
        for move in validMoves:
            allMoves.append((piece, move))
    
    return allMoves

def makeMove(app, piece, move):
    """Make a move and return the captured piece (if any) for undo."""
    capturedPiece = app.plist[move[0]][move[1]]
    
    # Store original position
    originalRow, originalCol = piece.row, piece.col
    
    # Handle special moves (similar to mousePressed logic)
    if len(move) > 2:
        if move[2] == 'hit':
            if piece.color == 'white':
                app.whitetakenpieces.append(capturedPiece)
                app.blackpieces.remove(capturedPiece)
            else:
                app.blacktakenpieces.append(capturedPiece)
                app.whitepieces.remove(capturedPiece)
        # Handle castling, en passant, etc. (simplified for AI)
    
    # Move the piece
    app.plist[originalRow][originalCol] = None
    app.plist[move[0]][move[1]] = piece
    piece.row = move[0]
    piece.col = move[1]
    
    return capturedPiece, originalRow, originalCol

def undoAIMove(app, piece, move, capturedPiece, originalRow, originalCol):
    """Undo a move (used by AI for move evaluation)."""
    # Move piece back
    app.plist[move[0]][move[1]] = capturedPiece
    app.plist[originalRow][originalCol] = piece
    piece.row = originalRow
    piece.col = originalCol
    
    # Restore captured piece
    if capturedPiece is not None and len(move) > 2 and move[2] == 'hit':
        if piece.color == 'white':
            app.whitetakenpieces.remove(capturedPiece)
            app.blackpieces.append(capturedPiece)
        else:
            app.blacktakenpieces.remove(capturedPiece)
            app.whitepieces.append(capturedPiece)

def easyAI(app):
    """Easy AI: Basic capture preference with simple evaluation."""
    validMoves = getAllValidMoves(app, app.computerPlayer)
    if not validMoves:
        return None
    
    # Prefer captures, but not always - adds some evaluation
    captures = []
    for piece, move in validMoves:
        if len(move) > 2 and move[2] == 'hit':
            pieceValues = {pawn: 1, knight: 3, bishop: 3, rook: 5, queen: 9}
            captured = app.plist[move[0]][move[1]]
            if captured:
                captureValue = pieceValues.get(type(captured), 0)
                captures.append((captureValue, piece, move))
    
    # 70% chance to take a capture if available, otherwise random
    if captures and random_module.random() < 0.7:
        captures.sort(reverse=True, key=lambda x: x[0])
        return captures[0][1:]  # Return (piece, move)
    
    return random_module.choice(validMoves)

def mediumAI(app):
    """Medium AI: Minimax depth 1, evaluates top moves."""
    validMoves = getAllValidMoves(app, app.computerPlayer)
    if not validMoves:
        return None
    
    # Evaluate moves with depth 1 minimax
    bestMove = None
    bestValue = float('-inf') if app.computerPlayer == 'white' else float('inf')
    
    # Order moves: captures first for better pruning
    moveScores = []
    for piece, move in validMoves:
        score = 0
        if len(move) > 2 and move[2] == 'hit':
            pieceValues = {pawn: 1, knight: 3, bishop: 3, rook: 5, queen: 9}
            captured = app.plist[move[0]][move[1]]
            if captured:
                score = pieceValues.get(type(captured), 0) * 10
        moveScores.append((score, piece, move))
    moveScores.sort(reverse=True, key=lambda x: x[0])
    orderedMoves = [m[1:] for m in moveScores]
    
    # Evaluate top 20 moves (more than before for better play)
    movesToEvaluate = orderedMoves[:min(20, len(orderedMoves))]
    
    for piece, move in movesToEvaluate:
        captured, origRow, origCol = makeMove(app, piece, move)
        
        # Use minimax with depth 1
        value = minimax(app, 1, app.computerPlayer == 'black', float('-inf'), float('inf'))
        
        undoAIMove(app, piece, move, captured, origRow, origCol)
        
        if app.computerPlayer == 'white':
            if value > bestValue:
                bestValue = value
                bestMove = (piece, move)
        else:
            if value < bestValue:
                bestValue = value
                bestMove = (piece, move)
    
    return bestMove if bestMove else random_module.choice(validMoves)

def minimax(app, depth, isMaximizing, alpha, beta):
    """Minimax algorithm with alpha-beta pruning and move ordering."""
    if depth == 0:
        return evaluatePosition(app)
    
    color = 'white' if isMaximizing else 'black'
    validMoves = getAllValidMoves(app, color)
    
    if not validMoves:
        # Check if it's checkmate or stalemate
        king = app.whiteking if color == 'white' else app.blackking
        if inCheck(app, king.row, king.col, color):
            return -1000 if isMaximizing else 1000  # Checkmate
        else:
            return 0  # Stalemate
    
    # Order moves: captures first for better alpha-beta pruning
    moveScores = []
    for piece, move in validMoves:
        score = 0
        if len(move) > 2 and move[2] == 'hit':
            pieceValues = {pawn: 1, knight: 3, bishop: 3, rook: 5, queen: 9}
            captured = app.plist[move[0]][move[1]]
            if captured:
                score = pieceValues.get(type(captured), 0) * 10
        moveScores.append((score, piece, move))
    moveScores.sort(reverse=True, key=lambda x: x[0])
    orderedMoves = [m[1:] for m in moveScores]
    
    if isMaximizing:
        maxEval = float('-inf')
        for piece, move in orderedMoves:
            captured, origRow, origCol = makeMove(app, piece, move)
            eval = minimax(app, depth - 1, False, alpha, beta)
            undoAIMove(app, piece, move, captured, origRow, origCol)
            
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Alpha-beta pruning
        return maxEval
    else:
        minEval = float('inf')
        for piece, move in orderedMoves:
            captured, origRow, origCol = makeMove(app, piece, move)
            eval = minimax(app, depth - 1, True, alpha, beta)
            undoAIMove(app, piece, move, captured, origRow, origCol)
            
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha-beta pruning
        return minEval

def hardAI(app):
    """Hard AI: Minimax with depth 3, evaluates many moves."""
    validMoves = getAllValidMoves(app, app.computerPlayer)
    if not validMoves:
        return None
    
    # Order moves: captures first, then by piece value
    moveScores = []
    for piece, move in validMoves:
        score = 0
        if len(move) > 2 and move[2] == 'hit':
            pieceValues = {pawn: 1, knight: 3, bishop: 3, rook: 5, queen: 9}
            captured = app.plist[move[0]][move[1]]
            if captured:
                score = pieceValues.get(type(captured), 0) * 10
        # Add piece value for move ordering
        pieceValues = {pawn: 1, knight: 3, bishop: 3, rook: 5, queen: 9, king: 0}
        score += pieceValues.get(type(piece), 0)
        moveScores.append((score, piece, move))
    moveScores.sort(reverse=True, key=lambda x: x[0])
    orderedMoves = [m[1:] for m in moveScores]
    
    # Evaluate top 25 moves with depth 3 (much deeper search)
    movesToEvaluate = orderedMoves[:min(25, len(orderedMoves))]
    
    bestMove = None
    bestValue = float('-inf') if app.computerPlayer == 'white' else float('inf')
    
    for piece, move in movesToEvaluate:
        captured, origRow, origCol = makeMove(app, piece, move)
        
        # Use minimax with depth 3 (deeper search for stronger play)
        value = minimax(app, 3, app.computerPlayer == 'black', float('-inf'), float('inf'))
        
        undoAIMove(app, piece, move, captured, origRow, origCol)
        
        if app.computerPlayer == 'white':
            if value > bestValue:
                bestValue = value
                bestMove = (piece, move)
        else:
            if value < bestValue:
                bestValue = value
                bestMove = (piece, move)
    
    return bestMove if bestMove else orderedMoves[0]

def getComputerMove(app):
    """Get the computer's move based on difficulty."""
    if app.difficulty == 'easy':
        return easyAI(app)
    elif app.difficulty == 'medium':
        return mediumAI(app)
    elif app.difficulty == 'hard':
        return hardAI(app)
    return None

def gameDimensions():
    rows = 8
    cols = 8
    cellSize = 80  # Increased from 60
    margin = 100   # Increased from 60
    return (rows, cols, cellSize, margin)

def onAppStart(app):
    d = gameDimensions()
    #checks for checkmate, returns winner when over
    app.gameStarted = False
    app.gameOver = False
    app.winner = ''

    #AI and game mode variables
    app.gameMode = None  # None = menu, 'human' = human vs human, 'computer' = human vs computer
    app.computerPlayer = 'black'  # which color the computer plays
    app.difficulty = None  # 'easy', 'medium', 'hard'
    app.computerThinking = False
    
    #holds the previous click so each player can think and highlight moves
    app.prevclick = None
    app.firstclickwork = False
    #True is white's move, False is black's move
    app.numTurns = 0
    app.turn = True
    
    # Animation variables
    app.animatingPiece = None
    app.animationStartPos = None
    app.animationEndPos = None
    app.animationProgress = 0.0
    app.animationSpeed = 0.15  # How fast pieces move (0-1 per step)
    
    app.rows = d[0]
    app.cols = d[1]
    app.cellSize = d[2]
    app.margin = d[3]
    
    app.blackrook1 = rook('black', 0, 0)
    app.blackknight1 = knight('black', 0, 1)
    app.blackbishop1 = bishop('black', 0, 2)
    app.blackqueen = queen('black', 0, 3)
    app.blackking = king('black', 0, 4)
    app.blackbishop2 = bishop('black', 0, 5)
    app.blackknight2 = knight('black', 0, 6)
    app.blackrook2 = rook('black', 0, 7)
    app.whiterook1 = rook('white', 7, 0)
    app.whiteknight1 = knight('white', 7, 1)
    app.whitebishop1 = bishop('white', 7, 2)
    app.whitequeen = queen('white', 7, 3)
    app.whiteking = king('white', 7, 4)
    app.whitebishop2 = bishop('white', 7, 5)
    app.whiteknight2 = knight('white', 7, 6)
    app.whiterook2 = rook('white', 7, 7)
    app.blackpawn1 = pawn('black', 1, 0)
    app.blackpawn2 = pawn('black', 1, 1)
    app.blackpawn3 = pawn('black', 1, 2)
    app.blackpawn4 = pawn('black', 1, 3)
    app.blackpawn5 = pawn('black', 1, 4)
    app.blackpawn6 = pawn('black', 1, 5)
    app.blackpawn7 = pawn('black', 1, 6)
    app.blackpawn8 = pawn('black', 1, 7)
    app.whitepawn1 = pawn('white', 6, 0)
    app.whitepawn2 = pawn('white', 6, 1)
    app.whitepawn3 = pawn('white', 6, 2)
    app.whitepawn4 = pawn('white', 6, 3)
    app.whitepawn5 = pawn('white', 6, 4)
    app.whitepawn6 = pawn('white', 6, 5)
    app.whitepawn7 = pawn('white', 6, 6)
    app.whitepawn8 = pawn('white', 6, 7)
    app.whitepieces = [app.whiterook1, app.whiterook2, app.whiteknight1, 
        app.whiteknight2, app.whitebishop1, app.whitebishop2, app.whitequeen,
        app.whitepawn1, app.whitepawn2, app.whitepawn3, app.whitepawn4, 
        app.whitepawn5, app.whitepawn6, app.whitepawn7, app.whitepawn8, app.whiteking]
    app.blackpieces = [app.blackrook1, app.blackrook2, app.blackknight1, 
        app.blackknight2, app.blackbishop1, app.blackbishop2, app.blackqueen,
        app.blackpawn1, app.blackpawn2, app.blackpawn3, app.blackpawn4, 
        app.blackpawn5, app.blackpawn6, app.blackpawn7, app.blackpawn8, app.blackking]
    
    #list of the taken pieces for each player, displayed on side of board
    app.whitetakenpieces = []
    app.blacktakenpieces = []

    board = []
    plist = []
    for i in range(8):
        addrow = []
        addlist = []
        for j in range(8):
            if((j+i)%2==0):
                addrow.append(['white', None])
                addlist.append(None)
                continue
            addrow.append(['gray', None])
            addlist.append(None)
        board.append(addrow)
        plist.append(addlist)
    
    #CITATION image taken from online, free stock image of man on ground
    #image of bruce lee open for free use
    #photoshopped by Andy xu
    app.bvictory = "chess/assets/bvictory.png"

    #CITATION image taken by NBA, Lebron James dunking on Isaiah Thomas
    #courtesy of Bob DeChiaria USA Today
    #photoshopped by Andy xu
    app.wvictory = "chess/assets/wvictory.png"

    #CITATION image taken from Spiderman Original 
    app.stalemate = "chess/assets/stalemate.png"

    #CITATION menu screen taken from Olympia, Arnold Schwarzenegger 
    #and Ronnie Coleman free stock, photoshopped by me
    app.menu = "chess/assets/Menu.png"

    #CITATION Muscle Letter P taken from P stock image
    app.p = "chess/assets/P.png"

    #CITATION Chess pieces taken from chess.com free to use
    # Images have been pre-converted to RGBA format for proper transparency
    # Uncomment the lines below if you need to reconvert images:
    # fixAlpha("chess/assets/whitepawn.png")
    # fixAlpha("chess/assets/blackpawn.png")
    # fixAlpha("chess/assets/whiteking.png")
    # fixAlpha("chess/assets/blackking.png")
    # fixAlpha("chess/assets/whitequeen.png")
    # fixAlpha("chess/assets/blackqueen.png")
    # fixAlpha("chess/assets/whiterook.png")
    # fixAlpha("chess/assets/blackrook.png")
    # fixAlpha("chess/assets/whitebishop.png")
    # fixAlpha("chess/assets/blackbishop.png")
    # fixAlpha("chess/assets/whiteknight.png")
    # fixAlpha("chess/assets/blackknight.png")
    
    app.bking = f"chess/assets/{app.blackking.image}"
    app.bbishop = f"chess/assets/{app.blackbishop2.image}"
    app.bknight = f"chess/assets/{app.blackknight2.image}"
    app.brook = f"chess/assets/{app.blackrook1.image}"
    app.bpawn = f"chess/assets/{app.blackpawn1.image}"
    app.bqueen = f"chess/assets/{app.blackqueen.image}"
    app.wking = f"chess/assets/{app.whiteking.image}"
    app.wbishop = f"chess/assets/{app.whitebishop2.image}"
    app.wknight = f"chess/assets/{app.whiteknight1.image}"
    app.wrook = f"chess/assets/{app.whiterook1.image}"
    app.wpawn = f"chess/assets/{app.whitepawn1.image}"
    app.wqueen = f"chess/assets/{app.whitequeen.image}"
    
    #set up the board
    plist = [[app.blackrook1, app.blackknight1, app.blackbishop1, app.blackqueen, app.blackking, app.blackbishop2, app.blackknight2, app.blackrook2],
             [app.blackpawn1, app.blackpawn2, app.blackpawn3, app.blackpawn4, app.blackpawn5, app.blackpawn6, app.blackpawn7, app.blackpawn8],
             [None, None, None, None, None, None, None, None],
             [None, None, None, None, None, None, None, None],
             [None, None, None, None, None, None, None, None],
             [None, None, None, None, None, None, None, None],
             [app.whitepawn1, app.whitepawn2, app.whitepawn3, app.whitepawn4, app.whitepawn5, app.whitepawn6, app.whitepawn7, app.whitepawn8],
             [app.whiterook1, app.whiteknight1, app.whitebishop1, app.whitequeen, app.whiteking, app.whitebishop2, app.whiteknight2, app.whiterook2]]
    app.board = board
    app.plist = plist
    
    app.storeOriginal = None
    app.storePrevious = None
    app.storePreviousType = None
    app.undoList = []

class piece():
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
    def getRow(self):
        return self.row
    def getCol(self):
        return self.col
    def getColor(self):
        return self.color

class pawn(piece):
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.image = f'{self.color}pawn.png'
    def needPromotion(self):
        if(self.color == 'white'):
            if(self.row == 0):
                return True
        else:
            if(self.row == 7):
                return True
        return False
    def moves(self, board):
        legalMoves = []
        if(self.color == 'white'):
            if(self.row != 0):
                if(board[self.row-1][self.col] == None):
                    legalMoves.append((self.row-1, self.col))
                if(self.row == 6):
                    if(board[self.row-1][self.col] == None and
                    board[self.row-2][self.col] == None):
                        legalMoves.append((self.row-2, self.col))
                #attack
                if(self.col != 0):
                    if(board[self.row-1][self.col-1] != None and
                    board[self.row-1][self.col-1].getColor()!=self.color):
                        legalMoves.append((self.row-1, self.col-1, 'hit'))
                if(self.col != 7):
                    if(board[self.row-1][self.col+1] != None and
                    board[self.row-1][self.col+1].getColor()!=self.color):
                        legalMoves.append((self.row-1, self.col+1, 'hit'))
                #enpassant
                if(self.col != 0 and self.row == 3):
                    if(board[self.row-1][self.col-1] == None and
                    type(board[self.row][self.col-1]) == pawn and
                    board[self.row][self.col-1].getColor()!=self.color):
                        legalMoves.append((self.row-1, self.col-1, 'wlenpassant'))
                if(self.col != 7 and self.row == 3):
                    if(board[self.row-1][self.col+1] == None and
                    type(board[self.row][self.col+1]) == pawn and 
                    board[self.row][self.col+1].getColor()!=self.color):
                        legalMoves.append((self.row-1, self.col+1, 'wrenpassant'))
        
        else:
            if(self.row != 7):
                if(board[self.row+1][self.col] == None):
                    legalMoves.append((self.row+1, self.col))
                if(self.row == 1):
                    if(board[self.row+1][self.col] == None and
                    board[self.row+2][self.col] == None):
                        legalMoves.append((self.row+2, self.col))
                #attack
                if(self.col != 0):
                    if(board[self.row+1][self.col-1]!= None and
                        board[self.row+1][self.col-1].getColor()!=self.color):
                        legalMoves.append((self.row+1, self.col-1, 'hit'))
                if(self.col != 7):
                    if(board[self.row+1][self.col+1]!=None and
                    board[self.row+1][self.col+1].getColor()!=self.color):
                        legalMoves.append((self.row+1, self.col+1, 'hit'))
                #enpassant
                if(self.col != 0 and self.row == 4):
                    if(board[self.row+1][self.col-1] == None and
                    type(board[self.row][self.col-1]) == pawn and
                    board[self.row][self.col-1].getColor()!=self.color):
                        legalMoves.append((self.row+1, self.col-1, 'blenpassant'))
                if(self.col != 7 and self.row == 4):
                    if(board[self.row+1][self.col+1] == None and
                    type(board[self.row][self.col+1]) == pawn and 
                    board[self.row][self.col+1].getColor()!=self.color):
                        legalMoves.append((self.row+1, self.col+1, 'brenpassant'))
        return legalMoves

class bishop(piece):
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.image = f'{self.color}bishop.png'
    def moves(self, board):
        legalMoves = []
        #checking upleft
        if(self.row != 0 and self.col != 0):
            upleft = 1
            edgeCase = False
            while(board[self.row-upleft][self.col-upleft] == None):
                    legalMoves.append((self.row-upleft, self.col-upleft))
                    upleft += 1
                    if(self.col-upleft < 0 or self.row-upleft < 0):
                        edgeCase = True
                        break
            if(not edgeCase and 
            board[self.row-upleft][self.col-upleft].getColor()!=self.color):
                legalMoves.append((self.row-upleft, self.col-upleft, 'hit'))
        #checking upright
        if(self.row != 0 and self.col != 7):
            upright = 1
            edgeCase = False
            while(board[self.row-upright][self.col+upright] == None):
                    legalMoves.append((self.row-upright, self.col+upright))
                    upright += 1
                    if(self.col+upright > 7 or self.row-upright < 0):
                        edgeCase = True
                        break
            if(not edgeCase and 
            board[self.row-upright][self.col+upright].getColor()!=
            self.color):
                legalMoves.append((self.row-upright, self.col+upright, 'hit'))
        #checking downleft
        if(self.row != 7 and self.col != 0):
            downleft = 1
            edgeCase = False
            while(board[self.row+downleft][self.col-downleft] == None):
                    legalMoves.append((self.row+downleft, self.col-downleft))
                    downleft += 1
                    if(self.col-downleft < 0 or self.row+downleft > 7):
                        edgeCase = True
                        break
            if(not edgeCase and 
            board[self.row+downleft][self.col-downleft].getColor()!=
            self.color):
                legalMoves.append((self.row+downleft, self.col-downleft, 'hit'))
        #checking downright
        if(self.row != 7 and self.col != 7):
            downright = 1
            edgeCase = False
            while(board[self.row+downright][self.col+downright] == None):
                    legalMoves.append((self.row+downright, self.col+downright))
                    downright += 1
                    if(self.col+downright > 7 or self.row+downright > 7):
                        edgeCase = True
                        break
            if(not edgeCase and board[self.row+
            downright][self.col+downright].getColor()!=self.color):
                legalMoves.append((self.row+downright, 
                self.col+downright, 'hit'))
        return legalMoves
        
class knight(piece):
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.image = f'{self.color}knight.png'
    def moves(self, board):
        legalMoves = []
        #all of the knight's moves, 8 in total
        if(self.row > 1 and self.col > 0):
            if(board[self.row - 2][self.col - 1] == None):
                legalMoves.append((self.row - 2, self.col - 1))
            elif(board[self.row - 2][self.col - 1].getColor()!= self.color):
                legalMoves.append((self.row - 2, self.col - 1, 'hit'))
        if(self.row > 1 and self.col < 7):
            if(board[self.row - 2][self.col + 1] == None):
                legalMoves.append((self.row - 2, self.col + 1))
            elif(board[self.row - 2][self.col + 1].getColor()!= self.color):
                legalMoves.append((self.row - 2, self.col + 1, 'hit'))
        if(self.row < 6 and self.col > 0):
            if(board[self.row + 2][self.col - 1] == None):
                legalMoves.append((self.row + 2, self.col - 1))
            elif(board[self.row + 2][self.col - 1].getColor()!= self.color):
                legalMoves.append((self.row + 2, self.col - 1, 'hit'))
        if(self.row < 6 and self.col < 7):
            if(board[self.row + 2][self.col + 1] == None):
                legalMoves.append((self.row + 2, self.col + 1))
            elif(board[self.row + 2][self.col + 1].getColor()!= self.color):
                legalMoves.append((self.row + 2, self.col + 1, 'hit'))
        if(self.row > 0 and self.col > 1):
            if(board[self.row - 1][self.col - 2] == None):
                legalMoves.append((self.row - 1, self.col - 2))
            elif(board[self.row - 1][self.col - 2].getColor()!= self.color):
                legalMoves.append((self.row - 1, self.col - 2, 'hit'))
        if(self.row < 7 and self.col > 1):
            if(board[self.row + 1][self.col - 2] == None):
                legalMoves.append((self.row + 1, self.col - 2))
            elif(board[self.row + 1][self.col - 2].getColor()!= self.color):
                legalMoves.append((self.row + 1, self.col - 2, 'hit'))
        if(self.row > 0 and self.col < 6):
            if(board[self.row - 1][self.col + 2] == None):
                legalMoves.append((self.row - 1, self.col + 2))
            elif(board[self.row - 1][self.col + 2].getColor()!= self.color):
                legalMoves.append((self.row - 1, self.col + 2, 'hit'))
        if(self.row < 7 and self.col < 6):
            if(board[self.row + 1][self.col + 2] == None):
                legalMoves.append((self.row + 1, self.col + 2))
            elif(board[self.row + 1][self.col + 2].getColor()!= self.color):
                legalMoves.append((self.row + 1, self.col + 2, 'hit'))
        return legalMoves

class king(piece):
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.hasMoved = False
        self.kingside = True
        self.queenside = True
        self.image = f'{self.color}king.png'
    def canCastle(self):
        return self.hasMoved
    def changepermission(self, newperm):
        self.hasMoved = newperm
    def moves(self, board):
        legalMoves = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if(i == 0 and j == 0):
                    continue
                if((self.col+j <= 7) and (self.col+j >= 0) 
                and (self.row+i <= 7) and (self.row+i >= 0)):
                    if(board[self.row+i][self.col+j] == None):
                        legalMoves.append((self.row+i, self.col+j))
                    elif(board[self.row+i][self.col+j].getColor()!= self.color):
                        legalMoves.append((self.row+i, self.col+j, 'hit'))
        #kingside castle for white
        if((not self.hasMoved) and (self.kingside) and 
            (board[self.row][self.col+1]==None) and 
            (board[self.row][self.col+2]==None) and (self.color == 'white')):
            legalMoves.append((self.row, self.col+2, 'wkcastled'))
        #queenside castle for white
        if((not self.hasMoved) and (self.queenside) and 
            (board[self.row][self.col-1]==None) and 
            (board[self.row][self.col-2]==None) and
            (board[self.row][self.col-3]==None) and (self.color == 'white')):
            legalMoves.append((self.row, self.col-2, 'wqcastled'))
        if((not self.hasMoved) and (self.kingside) and 
            (board[self.row][self.col+1]==None) and 
            (board[self.row][self.col+2]==None) and (self.color == 'black')):
            legalMoves.append((self.row, self.col+2, 'bkcastled'))
        if((not self.hasMoved) and (self.queenside) and 
            (board[self.row][self.col-1]==None) and 
            (board[self.row][self.col-2]==None) and
            (board[self.row][self.col-3]==None) and (self.color == 'black')):
            legalMoves.append((self.row, self.col-2, 'bqcastled'))
        return legalMoves

class queen(piece):
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.image = f'{self.color}queen.png'
    def moves(self, board):
        legalMoves = []
        #checking upleft
        if(self.row != 0 and self.col != 0):
            upleft = 1
            edgeCase = False
            while(board[self.row-upleft][self.col-upleft] == None):
                    legalMoves.append((self.row-upleft, self.col-upleft))
                    upleft += 1
                    if(self.col-upleft < 0 or self.row-upleft < 0):
                        edgeCase = True
                        break
            if(not edgeCase and 
            board[self.row-upleft][self.col-upleft].getColor()!=self.color):
                legalMoves.append((self.row-upleft, self.col-upleft, 'hit'))
        #checking upright
        if(self.row != 0 and self.col != 7):
            upright = 1
            edgeCase = False
            while(board[self.row-upright][self.col+upright] == None):
                    legalMoves.append((self.row-upright, self.col+upright))
                    upright += 1
                    if(self.col+upright > 7 or self.row-upright < 0):
                        edgeCase = True
                        break
            if(not edgeCase and 
            board[self.row-upright][self.col+upright].getColor()!=
            self.color):
                legalMoves.append((self.row-upright, self.col+upright, 'hit'))
        #checking downleft
        if(self.row != 7 and self.col != 0):
            downleft = 1
            edgeCase = False
            while(board[self.row+downleft][self.col-downleft] == None):
                    legalMoves.append((self.row+downleft, self.col-downleft))
                    downleft += 1
                    if(self.col-downleft < 0 or self.row+downleft > 7):
                        edgeCase = True
                        break
            if(not edgeCase and 
            board[self.row+downleft][self.col-downleft].getColor()!=
            self.color):
                legalMoves.append((self.row+downleft, self.col-downleft, 'hit'))
        #checking downright
        if(self.row != 7 and self.col != 7):
            downright = 1
            edgeCase = False
            while(board[self.row+downright][self.col+downright] == None):
                    legalMoves.append((self.row+downright, self.col+downright))
                    downright += 1
                    if(self.col+downright > 7 or self.row+downright > 7):
                        edgeCase = True
                        break
            if(not edgeCase and board[self.row+
            downright][self.col+downright].getColor()!=self.color):
                legalMoves.append((self.row+downright, 
                self.col+downright, 'hit'))
        #checking the left of the rook if not on left edge
        if(self.col != 0):
            left = 1
            edgeCase = False
            while(board[self.row][self.col-left] == None):
                legalMoves.append((self.row, self.col-left))
                left += 1
                if(self.col-left < 0):
                    edgeCase = True
                    break
            if(not edgeCase and 
            board[self.row][self.col-left].getColor()!=self.color):
                legalMoves.append((self.row, self.col-left, 'hit'))
        #checking the right
        if(self.col != 7):
            right = 1
            edgeCase = False
            while(board[self.row][self.col+right] == None):
                legalMoves.append((self.row, self.col+right))
                right += 1
                if(self.col+right > 7):
                    edgeCase = True
                    break
            if(not edgeCase and 
            board[self.row][self.col+right].getColor()!=self.color):
                legalMoves.append((self.row, self.col+right, 'hit'))
        #checking upwards
        if(self.row != 0):
            up = 1
            edgeCase = False
            while(board[self.row-up][self.col] == None):
                legalMoves.append((self.row-up, self.col))
                up += 1
                if(self.row-up < 0):
                    edgeCase = True
                    break
            if(not edgeCase and 
            board[self.row-up][self.col].getColor()!=self.color):
                legalMoves.append((self.row-up, self.col, 'hit'))
        #checking downwards
        if(self.row != 7):
            down = 1
            edgeCase = False
            while(board[self.row+down][self.col] == None):
                legalMoves.append((self.row+down, self.col))
                down += 1
                if(self.row+down > 7):
                    edgeCase = True
                    break
            if(not edgeCase and 
            board[self.row+down][self.col].getColor()!=self.color):
                legalMoves.append((self.row+down, self.col, 'hit'))

        return legalMoves

class rook(piece):
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.castle = True
        self.hasMoved = False
        self.image = f'{self.color}rook.png'
    def moves(self, board):
        legalMoves = []
        #checking the left of the rook if not on left edge
        if(self.col != 0):
            left = 1
            edgeCase = False
            while(board[self.row][self.col-left] == None):
                legalMoves.append((self.row, self.col-left))
                left += 1
                if(self.col-left < 0):
                    edgeCase = True
                    break
            if(not edgeCase and 
            board[self.row][self.col-left].getColor()!=self.color):
                legalMoves.append((self.row, self.col-left, 'hit'))
        #checking the right
        if(self.col != 7):
            right = 1
            edgeCase = False
            while(board[self.row][self.col+right] == None):
                legalMoves.append((self.row, self.col+right))
                right += 1
                if(self.col+right > 7):
                    edgeCase = True
                    break
            if(not edgeCase and 
            board[self.row][self.col+right].getColor()!=self.color):
                legalMoves.append((self.row, self.col+right, 'hit'))
        #checking upwards
        if(self.row != 0):
            up = 1
            edgeCase = False
            while(board[self.row-up][self.col] == None):
                legalMoves.append((self.row-up, self.col))
                up += 1
                if(self.row-up < 0):
                    edgeCase = True
                    break
            if(not edgeCase and 
            board[self.row-up][self.col].getColor()!=self.color):
                legalMoves.append((self.row-up, self.col, 'hit'))
        #checking downwards
        if(self.row != 7):
            down = 1
            edgeCase = False
            while(board[self.row+down][self.col] == None):
                legalMoves.append((self.row+down, self.col))
                down += 1
                if(self.row+down > 7):
                    edgeCase = True
                    break
            if(not edgeCase and 
            board[self.row+down][self.col].getColor()!=self.color):
                legalMoves.append((self.row+down, self.col, 'hit'))
        return legalMoves

#checks if position is in bounds
def inBound(row, col):
    if(row < 0 or row >= 8 or col < 0 or col >=8):
        return False
    return True    

#checks if position is in check for the color king that is given
def inCheck(app, row, col, color):
    n=1
    #upleft
    while(row-n>0 and col-n>0 and app.plist[row-n][col-n]==None):
        n+=1
    if(inBound(row-n, col-n)):
        check = app.plist[row-n][col-n]
        if(check != None and ((type(check)==bishop or type(check)==queen) and check.color!=color)):
            return True
        if(n==1):
            if(check != None and type(check)==king and check.color!=color):
                return True
            elif(check != None and type(check)==pawn and check.color!=color and check.color=='black'):
                return True
    #upright
    n=1
    while(row-n>0 and col+n<7 and app.plist[row-n][col+n]==None):
        n+=1
    if(inBound(row-n, col+n)):
        check = app.plist[row-n][col+n]
        if(check != None and ((type(check)==bishop or type(check)==queen) and check.color!=color)):
            return True
        if(n==1):
            if(check != None and type(check)==king and check.color!=color):
                return True
            elif(check != None and type(check)==pawn and check.color!=color and check.color=='black'):
                return True
    #downleft
    n=1
    while(row+n<7 and col-n>0 and app.plist[row+n][col-n]==None):
        n+=1
    if(inBound(row+n, col-n)):
        check = app.plist[row+n][col-n]
        if(check != None and ((type(check)==bishop or type(check)==queen) and check.color!=color)):
            return True
        if(n==1):
            if(check != None and type(check)==king and check.color!=color):
                return True
            elif(check != None and type(check)==pawn and check.color!=color and check.color=='white'):
                return True
    #downright
    n=1
    while(row+n<7 and col+n<7 and app.plist[row+n][col+n]==None):
        n+=1
    if(inBound(row+n, col+n)):
        check = app.plist[row+n][col+n]
        if(check != None and (type(check)==bishop or type(check)==queen) and check.color!=color):
            return True
        if(n==1):
            if(check != None and type(check)==king and check.color!=color):
                return True
            elif(check != None and type(check)==pawn and check.color!=color and check.color=='white'):
                return True
    #up
    n=1
    while(row-n>0 and app.plist[row-n][col]==None):
        n+=1
    if(inBound(row-n, col)):
        check = app.plist[row-n][col]
        if(check != None and (type(check)==rook or type(check)==queen) and check.color!=color):
            return True
        if(check != None and n==1 and type(check)==king and check.color!=color):
            return True
    #down
    n=1
    while(row+n<7 and app.plist[row+n][col]==None):
        n+=1
    if(inBound(row+n, col)):
        check = app.plist[row+n][col]
        if(check != None and (type(check)==rook or type(check)==queen) and check.color!=color):
            return True
        if(check != None and n==1 and type(check)==king and check.color!=color):
            return True
    #left
    n=1
    while(col-n>0 and app.plist[row][col-n]==None):
        n+=1
    if(inBound(row, col-n)):
        check = app.plist[row][col-n]
        if(check != None and ((type(check)==rook or type(check)==queen) and check.color!=color)):
            return True
        if(check != None and n==1 and type(check)==king and check.color!=color):
            return True
    #right
    n=1
    while(col+n<7 and app.plist[row][col+n]==None):
        n+=1
    if(inBound(row, col+n)):
        check = app.plist[row][col+n]
        if(check != None and ((type(check)==rook or type(check)==queen) and check.color!=color)):
            return True
        if(check != None and n==1 and type(check)==king and check.color!=color):
            return True
    #knight upleft
    if(row > 1 and col > 0):
        check = app.plist[row-2][col-1]
        if(check != None and check.color!=color and type(check) == knight):
            return True
    #knight upright
    if(row > 1 and col < 7):
        check = app.plist[row-2][col+1]
        if(check != None and check.color!=color and type(check) == knight):
            return True
    #knight downleft
    if(row < 6 and col > 0):
        check = app.plist[row+2][col-1]
        if(check != None and check.color!=color and type(check) == knight):
            return True
    #knight downright
    if(row < 6 and col < 7):
        check = app.plist[row+2][col+1]
        if(check != None and check.color!=color and type(check) == knight):
            return True
    #knight leftup
    if(row > 0 and col > 1):
        check = app.plist[row-1][col-2]
        if(check != None and check.color!=color and type(check) == knight):
            return True
    #knight leftdown
    if(row < 7 and col > 1):
        check = app.plist[row+1][col-2]
        if(check != None and check.color!=color and type(check) == knight):
            return True
    #knight rightup
    if(row > 0 and col < 6):
        check = app.plist[row-1][col+2]
        if(check != None and check.color!=color and type(check) == knight):
            return True
    #knight rightdown
    if(row < 7 and col < 6):
        check = app.plist[row+1][col+2]
        if(check != None and check.color!=color and type(check) == knight):
            return True
    return False

#given a list of moves, filters out moves that leave king in check/illegal
def actualMoves(app, possiblemoves):
    import time
    startTime = time.time()
    actualmoves = []
    inCheckCount = 0
    for move in possiblemoves:
        #checks if castle is allowed
        if(len(move)>2 and move[2]=='wkcastled'):
            if(inCheck(app, app.whiteking.row, app.whiteking.col, 'white') or 
            inCheck(app, app.whiteking.row, app.whiteking.col+1, 'white') or
            inCheck(app, app.whiteking.row, app.whiteking.col+2, 'white')):
                continue
        elif(len(move)>2 and move[2]=='bkcastled'):
            if(inCheck(app, app.blackking.row, app.blackking.col, 'black') or
            inCheck(app, app.blackking.row, app.blackking.col+2, 'black') or
            inCheck(app, app.blackking.row, app.blackking.col+1, 'black')):
                continue
        elif(len(move)>2 and move[2]=='wqcastled'):
            if(inCheck(app, app.whiteking.row, app.whiteking.col, 'white') or 
            inCheck(app, app.whiteking.row, app.whiteking.col-1, 'white') or
            inCheck(app, app.whiteking.row, app.whiteking.col-2, 'white') or 
            inCheck(app, app.whiteking.row, app.whiteking.col-3, 'white')):
                continue
        elif(len(move)>2 and move[2]=='bqcastled'):
            if(inCheck(app, app.blackking.row, app.blackking.col, 'black') or 
            inCheck(app, app.blackking.row, app.blackking.col-1, 'black') or
            inCheck(app, app.blackking.row, app.blackking.col-2, 'black') or 
            inCheck(app, app.blackking.row, app.blackking.col-3, 'black')):
                continue
        #checks if enpassant is possible for white left
        if(len(move)>2 and move[2]=='wlenpassant'):
            if(app.storePreviousType != pawn or app.storePrevious[0]-1 != move[0] 
            or app.storePrevious[1]!=move[1] or abs(app.storeOriginal-app.storePrevious[0])!=2):
                continue
        #white right enpassant
        if(len(move)>2 and move[2]=='wrenpassant'):
            if(app.storePreviousType != pawn or (app.storePrevious[0]-1) != move[0] 
            or app.storePrevious[1]!=move[1] or abs(app.storeOriginal-app.storePrevious[0])!=2):
                continue
        #black left enpassant
        if(len(move)>2 and move[2]=='blenpassant'):
            if(app.storePreviousType != pawn or app.storePrevious[0]+1 != move[0] 
            or app.storePrevious[1]!=move[1] or abs(app.storeOriginal-app.storePrevious[0])!=2):
                continue
        #black right enpassant
        if(len(move)>2 and move[2]=='brenpassant'):
            if(app.storePreviousType != pawn or app.storePrevious[0]+1 != move[0] 
            or app.storePrevious[1]!=move[1] or abs(app.storeOriginal-app.storePrevious[0])!=2):
                continue

        #backtracks: makes the move, checks if own king is in check after, removes if illegal
        saveState = app.plist[app.prevclick[0]][app.prevclick[1]]
        saveState2 = app.plist[move[0]][move[1]]
        app.plist[move[0]][move[1]] = app.plist[app.prevclick[0]][app.prevclick[1]]
        app.plist[app.prevclick[0]][app.prevclick[1]] = None
        app.plist[move[0]][move[1]].row = move[0]
        app.plist[move[0]][move[1]].col = move[1]
        if(saveState.color == 'white'):
            if(not inCheck(app, app.whiteking.row, app.whiteking.col, 'white')):
                actualmoves.append(move)
        elif(saveState.color == 'black'):
            if(not inCheck(app, app.blackking.row, app.blackking.col, 'black')):
                actualmoves.append(move)
        app.plist[app.prevclick[0]][app.prevclick[1]] = saveState
        app.plist[app.prevclick[0]][app.prevclick[1]].row = app.prevclick[0]
        app.plist[app.prevclick[0]][app.prevclick[1]].col = app.prevclick[1]
        app.plist[move[0]][move[1]] = saveState2
    
    return actualmoves

#restarts the game if prompted
def restartGame(app):
    app.blackrook1 = rook('black', 0, 0)
    app.blackknight1 = knight('black', 0, 1)
    app.blackbishop1 = bishop('black', 0, 2)
    app.blackqueen = queen('black', 0, 3)
    app.blackking = king('black', 0, 4)
    app.blackbishop2 = bishop('black', 0, 5)
    app.blackknight2 = knight('black', 0, 6)
    app.blackrook2 = rook('black', 0, 7)
    app.whiterook1 = rook('white', 7, 0)
    app.whiteknight1 = knight('white', 7, 1)
    app.whitebishop1 = bishop('white', 7, 2)
    app.whitequeen = queen('white', 7, 3)
    app.whiteking = king('white', 7, 4)
    app.whitebishop2 = bishop('white', 7, 5)
    app.whiteknight2 = knight('white', 7, 6)
    app.whiterook2 = rook('white', 7, 7)
    app.blackpawn1 = pawn('black', 1, 0)
    app.blackpawn2 = pawn('black', 1, 1)
    app.blackpawn3 = pawn('black', 1, 2)
    app.blackpawn4 = pawn('black', 1, 3)
    app.blackpawn5 = pawn('black', 1, 4)
    app.blackpawn6 = pawn('black', 1, 5)
    app.blackpawn7 = pawn('black', 1, 6)
    app.blackpawn8 = pawn('black', 1, 7)
    app.whitepawn1 = pawn('white', 6, 0)
    app.whitepawn2 = pawn('white', 6, 1)
    app.whitepawn3 = pawn('white', 6, 2)
    app.whitepawn4 = pawn('white', 6, 3)
    app.whitepawn5 = pawn('white', 6, 4)
    app.whitepawn6 = pawn('white', 6, 5)
    app.whitepawn7 = pawn('white', 6, 6)
    app.whitepawn8 = pawn('white', 6, 7)
    app.plist = [[app.blackrook1, app.blackknight1, app.blackbishop1, app.blackqueen, app.blackking, app.blackbishop2, app.blackknight2, app.blackrook2],
             [app.blackpawn1, app.blackpawn2, app.blackpawn3, app.blackpawn4, app.blackpawn5, app.blackpawn6, app.blackpawn7, app.blackpawn8],
             [None, None, None, None, None, None, None, None],
             [None, None, None, None, None, None, None, None],
             [None, None, None, None, None, None, None, None],
             [None, None, None, None, None, None, None, None],
             [app.whitepawn1, app.whitepawn2, app.whitepawn3, app.whitepawn4, app.whitepawn5, app.whitepawn6, app.whitepawn7, app.whitepawn8],
             [app.whiterook1, app.whiteknight1, app.whitebishop1, app.whitequeen, app.whiteking, app.whitebishop2, app.whiteknight2, app.whiterook2]]
    app.turn = True
    app.storeOriginal = None
    app.storePrevious = None
    app.storePreviousType = None
    app.whitetakenpieces = []
    app.blacktakenpieces = []
    app.whitepieces = [app.whiterook1, app.whiterook2, app.whiteknight1, 
        app.whiteknight2, app.whitebishop1, app.whitebishop2, app.whitequeen,
        app.whitepawn1, app.whitepawn2, app.whitepawn3, app.whitepawn4, 
        app.whitepawn5, app.whitepawn6, app.whitepawn7, app.whitepawn8, app.whiteking]
    app.blackpieces = [app.blackrook1, app.blackrook2, app.blackknight1, 
        app.blackknight2, app.blackbishop1, app.blackbishop2, app.blackqueen,
        app.blackpawn1, app.blackpawn2, app.blackpawn3, app.blackpawn4, 
        app.blackpawn5, app.blackpawn6, app.blackpawn7, app.blackpawn8, app.blackking]
    app.prevclick = None
    app.firstclickwork = False
    app.numTurns = 0
    app.gameOver = False
    app.winner = ""
    app.computerThinking = False
    
    # Reset animation state
    app.animatingPiece = None
    app.animationStartPos = None
    app.animationEndPos = None
    app.animationProgress = 0.0
    
    # Reset castling rights
    app.whiteking.hasMoved = False
    app.whiteking.kingside = True
    app.whiteking.queenside = True
    app.blackking.hasMoved = False
    app.blackking.kingside = True
    app.blackking.queenside = True
    
    # Reset rook movement flags
    app.whiterook1.hasMoved = False
    app.whiterook2.hasMoved = False
    app.blackrook1.hasMoved = False
    app.blackrook2.hasMoved = False
    
    board = []
    for i in range(8):
        addrow = []
        for j in range(8):
            if((j+i)%2==0):
                addrow.append(['white', None])
                continue
            addrow.append(['gray', None])
        board.append(addrow)
    app.board = board
    app.undoList = []

def undoMove(app):
    #0: original piece row
    #1: original piece col
    #2: original piece
    #3: piece to move back
    #4: original piece's row for en passant
    #5: stores the Previous move for that turn for en passant 
    #6: store previous type (if pawn and #5 is true, allow en passant after undo)
    #7: move to undo
    #8: color
    #9: special instance
    #10: special instance 2 for castling
    u = app.undoList[-1]
    #removes the first click to stop turn from glitching
    app.prevclick = None
    app.firstclickwork = False
    app.plist[u[0]][u[1]] = u[2]
    app.plist[u[0]][u[1]].row = u[0]
    app.plist[u[0]][u[1]].col = u[1]
    #only run through this if promoted, need to remove promoted piece from pieces
    #also need to add the deleted pawn back
    if(len(u)>9 and u[9] == 'promotion' and u[8]=='white'):
        app.whitepieces.remove(app.plist[u[7][0]][u[7][1]])
        app.plist[u[7][0]][u[7][1]] = u[3]
        app.plist[u[0]][u[1]] = u[10]
        app.whitepieces.append(app.plist[u[0]][u[1]])
    elif(len(u)>9 and u[9] == 'promotion' and u[8]=='black'):
        app.blackpieces.remove(app.plist[u[7][0]][u[7][1]])
        app.plist[u[7][0]][u[7][1]] = u[3]
        app.plist[u[0]][u[1]] = u[10]
        app.blackpieces.append(app.plist[u[0]][u[1]])
    else:
        app.plist[u[7][0]][u[7][1]] = u[3]
    #if the piece is not nothing 
    if(u[3] != None):
        app.plist[u[7][0]][u[7][1]].row = u[7][0]
        app.plist[u[7][0]][u[7][1]].col = u[7][1]
        if(len(u[7])>2 and u[7][2]=='hit'):
            if(u[8] == 'white'):
                app.blackpieces.append(app.plist[u[7][0]][u[7][1]])
                app.whitetakenpieces.remove(app.plist[u[7][0]][u[7][1]])
            else:
                app.whitepieces.append(app.plist[u[7][0]][u[7][1]])
                app.blacktakenpieces.remove(app.plist[u[7][0]][u[7][1]])
    if(len(u[7])>2 and u[7][2]=='wkcastled'):
        app.plist[7][7] = app.plist[7][5]
        app.plist[7][7].col = 7
        app.plist[7][5] = None
        app.plist[7][4].kingside = True
        app.plist[7][4].hasMoved = False
    elif(len(u[7])>2 and u[7][2]=='wqcastled'):
        app.plist[7][0] = app.plist[7][3]
        app.plist[7][0].col = 0
        app.plist[7][3] = None
        app.plist[7][4].queenside = True
        app.plist[7][4].hasMoved = False
    elif(len(u[7])>2 and u[7][2]=='bqcastled'):
        app.plist[0][0] = app.plist[0][3]
        app.plist[0][0].col = 0
        app.plist[0][3] = None
        app.plist[0][4].queenside = True
        app.plist[0][4].hasMoved = False
    elif(len(u[7])>2 and u[7][2]=='bkcastled'):
        app.plist[0][7] = app.plist[0][5]
        app.plist[0][7].col = 7
        app.plist[0][5] = None
        app.plist[0][4].kingside = True
        app.plist[0][4].hasMoved = False
    elif(len(u[7])>2 and u[7][2]=='wlenpassant'):
        app.plist[u[7][0]+1][u[7][1]]=u[9]
        app.blackpieces.append(app.plist[u[7][0]+1][u[7][1]])
        app.whitetakenpieces.remove(app.plist[u[7][0]+1][u[7][1]])
    elif(len(u[7])>2 and u[7][2]=='wrenpassant'):
        app.plist[u[7][0]+1][u[7][1]]=u[9]
        app.blackpieces.append(app.plist[u[7][0]+1][u[7][1]])
        app.whitetakenpieces.remove(app.plist[u[7][0]+1][u[7][1]])
    elif(len(u[7])>2 and u[7][2]=='blenpassant'):
        app.plist[u[7][0]-1][u[7][1]]=u[9]
        app.whitepieces.append(app.plist[u[7][0]-1][u[7][1]])
        app.blacktakenpieces.remove(app.plist[u[7][0]-1][u[7][1]])
    elif(len(u[7])>2 and u[7][2]=='brenpassant'):
        app.plist[u[7][0]-1][u[7][1]]=u[9]
        app.whitepieces.append(app.plist[u[7][0]-1][u[7][1]])
        app.blacktakenpieces.remove(app.plist[u[7][0]-1][u[7][1]])
    if(len(u)>10 and u[10] == 'wking'):
        app.whiteking.changepermission(u[9])
        print(app.whiteking.canCastle())
    elif(len(u)>10 and u[10] == 'bking'):
        app.blackking.hasMoved = u[9]
    elif(len(u)>10 and u[10] == 'wrook1'):
        app.whiteking.queenside = u[9]
    elif(len(u)>10 and u[10] == 'brook1'):
        app.blackking.queenside = u[9]
    elif(len(u)>10 and u[10] == 'wrook2'):
        app.whiteking.kingside = u[9]
    elif(len(u)>10 and u[10] == 'brook2'):
        app.blackking.kingside = u[9]
    #resets values to undo'ed move
    app.storeOriginal = u[4]
    app.storePrevious = u[5]
    app.storePreviousType = u[6]
    app.undoList = app.undoList[:-1]
    #resets turn if it was white's turn to decrease move counter
    if(app.turn):
        app.numTurns -=1
    #switches the turn counter
    app.turn = not app.turn

def onKeyPress(app, key):
    if(key == 'p'):
        app.gameStarted = True

def onStep(app):
    # Update animation progress
    if app.animatingPiece is not None and app.animationProgress < 1.0:
        app.animationProgress += app.animationSpeed
        if app.animationProgress >= 1.0:
            # Animation complete - clear animation state
            # Note: source position was already cleared in executeMove
            app.animationProgress = 1.0
            app.animatingPiece = None
            app.animationStartPos = None
            app.animationEndPos = None
    
    # Handle computer moves
    if app.gameStarted and not app.gameOver and app.gameMode == 'computer':
        # Only make computer move if no animation is in progress
        if app.animatingPiece is None:
            # Check if it's the computer's turn
            computersTurn = (app.computerPlayer == 'white' and app.turn) or (app.computerPlayer == 'black' and not app.turn)
            
            if computersTurn and not app.computerThinking:
                app.computerThinking = True
                makeComputerMove(app)

def makeComputerMove(app):
    """Execute the computer's move."""
    if app.gameOver:
        app.computerThinking = False
        return
        
    computerMove = getComputerMove(app)
    
    if computerMove is None:
        app.computerThinking = False
        return
    
    piece, move = computerMove
    
    # Execute the move (similar to the human move logic in mousePressed)
    executeMove(app, piece, move)
    
    app.computerThinking = False

def executeMove(app, piece, move):
    """Execute a move (used by both human and AI)."""
    # Store for undo functionality
    if app.turn:
        app.undoList.append([
            piece.row, piece.col, piece, app.plist[move[0]][move[1]],
            app.storeOriginal, app.storePrevious, app.storePreviousType,
            move, 'white'])
        if type(piece) == king:
            app.undoList[-1].extend([app.whiteking.hasMoved, 'wking'])
        elif piece == app.whiterook1:
            app.undoList[-1].extend([app.whiteking.queenside, 'wrook1'])
        elif piece == app.whiterook2:
            app.undoList[-1].extend([app.whiteking.kingside, 'wrook2'])
    else:
        app.undoList.append([
            piece.row, piece.col, piece, app.plist[move[0]][move[1]],
            app.storeOriginal, app.storePrevious, app.storePreviousType,
            move, 'black'])
        if type(piece) == king:
            app.undoList[-1].extend([app.blackking.hasMoved, 'bking'])
        elif piece == app.blackrook1:
            app.undoList[-1].extend([app.blackking.queenside, 'brook1'])
        elif piece == app.blackrook2:
            app.undoList[-1].extend([app.blackking.kingside, 'brook2'])

    # Handle special moves and piece movement
    handleSpecialMoves(app, piece, move)
    
    # Start animation
    app.animatingPiece = piece
    app.animationStartPos = [piece.row, piece.col]
    app.animationEndPos = [move[0], move[1]]
    app.animationProgress = 0.0
    
    # Move the piece - clear source position immediately to fix board drawing
    app.storeOriginal = piece.row
    app.storePrevious = move
    app.storePreviousType = type(piece)
    originalRow, originalCol = piece.row, piece.col
    piece.row = move[0]
    piece.col = move[1]
    # Clear the source position immediately so board draws correctly
    app.plist[originalRow][originalCol] = None
    app.plist[move[0]][move[1]] = piece
    
    # Handle pawn promotion (simplified for AI)
    if type(piece) == pawn and piece.needPromotion():
        # Auto-promote to queen for AI
        newPiece = queen(piece.color, piece.row, piece.col)
        promotion(app, piece, newPiece, piece.color)
        app.plist[move[0]][move[1]] = newPiece
        app.undoList[-1].extend(["promotion", piece])
    
    # Change turn
    if not app.turn:
        app.numTurns += 1
    app.turn = not app.turn
    
    # Check for game over
    checkGameOver(app)

def handleSpecialMoves(app, piece, move):
    """Handle castling, en passant, captures, etc."""
    # Store original position before moving
    originalRow, originalCol = piece.row, piece.col
    # Clear original position after animation completes (handled in onStep)
    
    # Handle captures and special moves
    if len(move) > 2:
        if move[2] == 'hit':
            capturedPiece = app.plist[move[0]][move[1]]
            if piece.color == 'white':
                app.whitetakenpieces.append(capturedPiece)
                app.blackpieces.remove(capturedPiece)
            else:
                app.blacktakenpieces.append(capturedPiece)
                app.whitepieces.remove(capturedPiece)
        # Handle other special moves (castling, en passant) - simplified for now
    
    # Update king/rook movement flags for castling
    updateCastlingRights(app, piece)

def updateCastlingRights(app, piece):
    """Update castling rights when king or rook moves."""
    if type(piece) == king:
        if piece.color == 'white':
            app.whiteking.hasMoved = True
        else:
            app.blackking.hasMoved = True
    elif type(piece) == rook:
        if piece == app.whiterook2:
            app.whiteking.kingside = False
        elif piece == app.whiterook1:
            app.whiteking.queenside = False
        elif piece == app.blackrook2:
            app.blackking.kingside = False
        elif piece == app.blackrook1:
            app.blackking.queenside = False

def checkGameOver(app):
    """Check for checkmate or stalemate."""
    color = 'white' if app.turn else 'black'
    king = app.whiteking if app.turn else app.blackking
    pieces = app.whitepieces if app.turn else app.blackpieces
    
    # Count valid moves
    totalMoves = 0
    for piece in pieces:
        possibleMoves = piece.moves(app.plist)
        originalPrevclick = app.prevclick
        app.prevclick = [piece.row, piece.col]
        validMoves = actualMoves(app, possibleMoves)
        app.prevclick = originalPrevclick
        totalMoves += len(validMoves)
    
    if totalMoves == 0:
        if inCheck(app, king.row, king.col, color):
            app.gameOver = True
            app.winner = 'Black' if app.turn else 'White'
        else:
            app.gameOver = True
            app.winner = ""  # Stalemate

def onMousePress(app, mouseX, mouseY):
    #as long as game is not over and game hasn't started (menu screen)
    if(not app.gameStarted):
        if app.gameMode is None:
            # Game mode selection
            buttonWidth = 300
            buttonHeight = 60
            buttonX = app.width//2 - buttonWidth//2
            if buttonX <= mouseX <= buttonX + buttonWidth:
                if 350 <= mouseY <= 410:  # Human vs Human
                    app.gameMode = 'human'
                    app.gameStarted = True
                    return
                elif 430 <= mouseY <= 490:  # Human vs Computer
                    app.gameMode = 'computer'
                    return
        elif app.gameMode == 'computer' and app.difficulty is None:
            # Difficulty selection
            buttonWidth = 300
            buttonHeight = 60
            buttonX = app.width//2 - buttonWidth//2
            if buttonX <= mouseX <= buttonX + buttonWidth:
                if 300 <= mouseY <= 360:  # Easy
                    app.difficulty = 'easy'
                    app.gameStarted = True
                    return
                elif 380 <= mouseY <= 440:  # Medium
                    app.difficulty = 'medium'
                    app.gameStarted = True
                    return
                elif 460 <= mouseY <= 520:  # Hard
                    app.difficulty = 'hard'
                    app.gameStarted = True
                    return
            # Back button
            if 50 <= mouseX <= 170 and app.height - 80 <= mouseY <= app.height - 40:
                app.gameMode = None
                return
        elif app.gameMode == 'human':
            # Start human vs human game
            if(mouseX > 150 and mouseY > 510 and mouseX < 200 and mouseY < 560):
                app.gameStarted = True
                return
    if(app.gameStarted):
        # Reset button
        buttonWidth = app.width/8
        buttonHeight = 55
        buttonX = app.width - buttonWidth - 20
        resetButtonY = app.margin + app.cellSize * 8 + 90
        if(buttonX <= mouseX <= buttonX + buttonWidth and 
           resetButtonY <= mouseY <= resetButtonY + buttonHeight):
            restartGame(app)
            # Keep game started - just reset the board
            app.gameStarted = True
            return
    if(not app.gameOver and app.gameStarted):
        # Don't allow human moves when computer is thinking
        if app.gameMode == 'computer' and app.computerThinking:
            return
        
        # Don't allow moves on computer's turn
        if app.gameMode == 'computer':
            computersTurn = (app.computerPlayer == 'white' and app.turn) or (app.computerPlayer == 'black' and not app.turn)
            if computersTurn:
                return
        
        # Undo button
        buttonWidth = app.width/8
        buttonHeight = 55
        buttonX = app.width - buttonWidth - 20
        undoButtonY = app.margin + app.cellSize * 8 + 20
        if(buttonX <= mouseX <= buttonX + buttonWidth and 
           undoButtonY <= mouseY <= undoButtonY + buttonHeight):
            if(len(app.undoList) >= 1):
                undoMove(app)
        dx = ((mouseX - app.margin)//app.cellSize)
        #insures in bounds, no out of bounds for window
        if (dx > 7 or dx < 0):
            return
        dy = ((mouseY - app.margin)//app.cellSize)
        if (dy > 7 or dy < 0):
            return
        #if I haven't clicked yet, and I click on a piece, it highlights the move and sets prevclick to that place
        if(app.firstclickwork == False and app.plist[dy][dx]!=None):
            if((app.turn and app.plist[dy][dx].getColor()=='white') or 
            (not app.turn and app.plist[dy][dx].getColor()=='black')):
                app.prevclick = [dy, dx]
                app.firstclickwork = True
        #first click
        elif(app.firstclickwork):
            #iterates through every move
            possiblemoves = app.plist[app.prevclick[0]][app.prevclick[1]].moves(app.plist)
            #remove the illegal moves through checking in actualMoves
            actualmoves = actualMoves(app, possiblemoves)
            for move in actualmoves:
                if(move[0] == dy and move[1] == dx):
                    if(app.turn):
                        app.undoList.append([
                            app.plist[app.prevclick[0]][app.prevclick[1]].row,  
                            app.plist[app.prevclick[0]][app.prevclick[1]].col, 
                            app.plist[app.prevclick[0]][app.prevclick[1]],     
                            app.plist[move[0]][move[1]],                        
                            app.storeOriginal,                                  
                            app.storePrevious,                                  
                            app.storePreviousType,
                            move,
                            'white'])
                        if(type(app.plist[app.prevclick[0]][app.prevclick[1]]) == king):
                            app.undoList[-1].extend([app.whiteking.hasMoved, 'wking'])
                        elif(app.plist[app.prevclick[0]][app.prevclick[1]] == app.whiterook1):
                            app.undoList[-1].extend([app.whiteking.queenside, 'wrook1'])
                        elif(app.plist[app.prevclick[0]][app.prevclick[1]] == app.whiterook2):
                            app.undoList[-1].extend([app.whiteking.kingside, 'wrook2'])
                        
                    else:
                        app.undoList.append([
                            app.plist[app.prevclick[0]][app.prevclick[1]].row,  
                            app.plist[app.prevclick[0]][app.prevclick[1]].col, 
                            app.plist[app.prevclick[0]][app.prevclick[1]],      
                            app.plist[move[0]][move[1]],                        
                            app.storeOriginal,                                  
                            app.storePrevious,                                 
                            app.storePreviousType,
                            move,
                            'black'])
                        if(type(app.plist[app.prevclick[0]][app.prevclick[1]]) == king):
                            app.undoList[-1].extend([app.blackking.hasMoved, 'bking'])
                        elif(app.plist[app.prevclick[0]][app.prevclick[1]] == app.blackrook1):
                            app.undoList[-1].extend([app.blackking.queenside, 'brook1'])
                        elif(app.plist[app.prevclick[0]][app.prevclick[1]] == app.blackrook2):
                            app.undoList[-1].extend([app.blackking.kingside, 'brook2'])
                    #if the king or rook moves, need to remove perms for castling
                    if(type(app.plist[app.prevclick[0]][app.prevclick[1]])==king 
                    or type(app.plist[app.prevclick[0]][app.prevclick[1]])==rook):
                        if(app.plist[app.prevclick[0]][ 
                            app.prevclick[1]].color == 'white' and 
                            type(app.plist[app.prevclick[0]][
                                app.prevclick[1]])==king):
                            app.whiteking.hasMoved = True
                        if(app.plist[app.prevclick[0]][
                            app.prevclick[1]].color == 'black' and 
                            type(app.plist[app.prevclick[0]][
                                app.prevclick[1]])==king):
                            app.blackking.hasMoved = True
                        elif((app.plist[app.prevclick[0]][
                            app.prevclick[1]])==app.whiterook2):
                            app.whiteking.kingside = False
                        elif((app.plist[app.prevclick[0]][
                            app.prevclick[1]])==app.whiterook1):
                            app.whiteking.queenside = False
                        elif((app.plist[app.prevclick[0]][
                            app.prevclick[1]])==app.blackrook2):
                            app.whiteking.kingside = False
                        elif((app.plist[app.prevclick[0]][
                            app.prevclick[1]])==app.blackrook1):
                            app.blackking.queenside = False
                    #en passant detailed by 2nd index of move
                    if(len(move)>2 and move[2] == 'wlenpassant'):
                        app.whitetakenpieces.append(app.plist[move[0]+1][move[1]])
                        app.blackpieces.remove(app.plist[move[0]+1][move[1]])
                        app.undoList[-1].extend([app.plist[move[0]+1][move[1]]])
                        app.plist[move[0]+1][move[1]] = None
                    if(len(move)>2 and move[2] == 'wrenpassant'):
                        app.whitetakenpieces.append(app.plist[move[0]+1][move[1]])
                        app.blackpieces.remove(app.plist[move[0]+1][move[1]])
                        app.undoList[-1].extend([app.plist[move[0]+1][move[1]]])
                        app.plist[move[0]+1][move[1]] = None
                    if(len(move)>2 and move[2] == 'blenpassant'):
                        app.blacktakenpieces.append(app.plist[move[0]-1][move[1]])
                        app.whitepieces.remove(app.plist[move[0]-1][move[1]])
                        app.undoList[-1].extend([app.plist[move[0]-1][move[1]]])
                        app.plist[move[0]-1][move[1]] = None
                    if(len(move)>2 and move[2] == 'brenpassant'):
                        app.blacktakenpieces.append(app.plist[move[0]-1][move[1]])
                        app.whitepieces.remove(app.plist[move[0]-1][move[1]])
                        app.undoList[-1].extend([app.plist[move[0]-1][move[1]]])
                        app.plist[move[0]-1][move[1]] = None
                    #castled detailed by 2nd index of move
                    if(len(move)>2) and move[2] == 'wkcastled' and dx == 6:
                        app.plist[7][5] = app.plist[7][7]
                        app.plist[7][5].col = 5
                        app.plist[7][7]=None
                    if(len(move)>2) and move[2] == 'bkcastled' and dx == 6:
                        app.plist[0][5] = app.plist[0][7]
                        app.plist[0][5].col = 5
                        app.plist[0][7] = None
                    if(len(move)>2) and move[2] == 'wqcastled' and dx == 2:
                        app.plist[7][3] = app.plist[7][0]
                        app.plist[7][3].col = 3
                        app.plist[7][0] = None
                    if(len(move)>2) and move[2] == 'bqcastled' and dx == 2:
                        app.plist[0][3] = app.plist[0][0]
                        app.plist[0][3].col = 3
                        app.plist[0][0] = None
                    #if it's an attack move, add the hit piece to taken pieces and remove from total piece list
                    if(len(move)>2 and move[2] =='hit'):
                        if(app.plist[app.prevclick[0]][app.prevclick[1]].color=='white'):
                            app.whitetakenpieces.append(app.plist[move[0]][move[1]])
                            app.blackpieces.remove(app.plist[move[0]][move[1]])
                        else:
                            app.blacktakenpieces.append(app.plist[move[0]][move[1]])
                            app.whitepieces.remove(app.plist[move[0]][move[1]])
                    #set the piece to that new move place
                    #stores original to 
                    app.storeOriginal = (app.plist[app.prevclick[0]][app.prevclick[1]].row)
                    app.storePrevious = move
                    app.storePreviousType = type(app.plist[app.prevclick[0]][app.prevclick[1]])
                    
                    # Start animation
                    movingPiece = app.plist[app.prevclick[0]][app.prevclick[1]]
                    app.animatingPiece = movingPiece
                    app.animationStartPos = [app.prevclick[0], app.prevclick[1]]
                    app.animationEndPos = [move[0], move[1]]
                    app.animationProgress = 0.0
                    
                    # Update piece position in plist
                    app.plist[app.prevclick[0]][app.prevclick[1]].row = move[0]
                    app.plist[app.prevclick[0]][app.prevclick[1]].col = move[1]
                    app.plist[move[0]][move[1]] = app.plist[
                        app.prevclick[0]][app.prevclick[1]]
                    app.plist[app.prevclick[0]][app.prevclick[1]] = None
                    promotionSquare = app.plist[move[0]][move[1]]
                    #checking if pawn reached the last rank, if so, prompt a piece to promote
                    if(type(promotionSquare)==pawn):
                        if(promotionSquare.needPromotion()):
                            promotedPiece = app.getTextInput("What piece would you like to promote to? \n k for knight, q for queen, r for rook, and b for bishop.")
                            while ((promotedPiece != "k") and (promotedPiece != "r") and (promotedPiece!= "q") and (promotedPiece!= "b")):
                                app.showMessage("Bruh try again and do better.\n k for knight, q for queen, r for rook, and b for bishop.")
                                promotedPiece = app.getTextInput("What piece would you like to promote to? \n k for knight, q for queen, r for rook, and b for bishop.")
                            if(promotedPiece == "k"):
                                newPiece = knight(promotionSquare.color, promotionSquare.row, promotionSquare.col)
                                promotion(app, promotionSquare, newPiece, promotionSquare.color)
                                app.plist[move[0]][move[1]] = newPiece
                            elif(promotedPiece == "r"):
                                newPiece = rook(promotionSquare.color, promotionSquare.row, promotionSquare.col)
                                promotion(app, promotionSquare, newPiece, promotionSquare.color)
                                app.plist[move[0]][move[1]] = newPiece
                            elif(promotedPiece == "q"):
                                newPiece = queen(promotionSquare.color, promotionSquare.row, promotionSquare.col)
                                promotion(app, promotionSquare, newPiece, promotionSquare.color)
                                app.plist[move[0]][move[1]] = newPiece
                            elif(promotedPiece == "b"):
                                newPiece = bishop(promotionSquare.color, promotionSquare.row, promotionSquare.col)
                                promotion(app, promotionSquare, newPiece, promotionSquare.color)
                                app.plist[move[0]][move[1]] = newPiece
                            #adding to special move 
                            app.undoList[-1].extend(["promotion", promotionSquare])
                    #after black's turn, change the total move counter
                    if(not app.turn):
                        app.numTurns+=1
                    #change the turn
                    app.turn = not app.turn
                    break
            #resets the click
            app.prevclick = None
            app.firstclickwork = False
        #checks for white checkmate
        if(app.turn):
            total = 0
            for piece in app.whitepieces:
                possiblemoves = piece.moves(app.plist)
                actualmoves = []
                #for all the possible moves, if it works, add to actual moves. 
                for move in possiblemoves:
                    saveState = piece
                    piecerow = piece.row
                    piececol = piece.col
                    saveState2 = app.plist[move[0]][move[1]]
                    app.plist[move[0]][move[1]] = piece
                    app.plist[move[0]][move[1]].row = move[0]
                    app.plist[move[0]][move[1]].col = move[1]
                    app.plist[piecerow][piececol] = None
                    if(saveState.color == 'white'):
                        if(not inCheck(app, app.whiteking.row, app.whiteking.col, 'white')):
                            actualmoves.append(move)
                    else:
                        if(not inCheck(app, app.blackking.row, app.blackking.col, 'black')):
                            actualmoves.append(move)
                    app.plist[piecerow][piececol] = saveState
                    app.plist[piecerow][piececol].row = piecerow
                    app.plist[piecerow][piececol].col = piececol
                    app.plist[move[0]][move[1]] = saveState2
                total+=len(actualmoves)
            #total moves is 0 when checkmate, so gameOver is changed
            if(total == 0):
                if(not inCheck(app, app.whiteking.row, app.whiteking.col, 'white')):
                    app.gameOver = True
                    app.winner = ""
                else:
                    app.gameOver = True
                    app.winner = 'Black'
        #checks for black checkmate, same format
        else:
            total = 0
            for piece in app.blackpieces:
                possiblemoves = piece.moves(app.plist)
                actualmoves = []
                for move in possiblemoves:
                    saveState = piece
                    piecerow = piece.row
                    piececol = piece.col
                    saveState2 = app.plist[move[0]][move[1]]
                    app.plist[move[0]][move[1]] = piece
                    app.plist[move[0]][move[1]].row = move[0]
                    app.plist[move[0]][move[1]].col = move[1]
                    app.plist[piecerow][piececol] = None
                    if(saveState.color == 'white'):
                        if(not inCheck(app, app.whiteking.row, app.whiteking.col, 'white')):
                            actualmoves.append(move)
                    else:
                        if(not inCheck(app, app.blackking.row, app.blackking.col, 'black')):
                            actualmoves.append(move)
                    app.plist[piecerow][piececol] = saveState
                    app.plist[piecerow][piececol].row = piecerow
                    app.plist[piecerow][piececol].col = piececol
                    app.plist[move[0]][move[1]] = saveState2
                total+=len(actualmoves)
            if(total == 0):
                if(not inCheck(app, app.blackking.row, app.blackking.col, 'black')):
                    app.gameOver = True
                    app.winner = ""
                else:
                    app.gameOver = True
                    app.winner = 'White'

#promotion adds the new piece to pieces list while removing the pawn
def promotion(app, promotedPawn, newPiece, color):
    if(color == 'white'):
        app.whitepieces.remove(promotedPawn)
        app.whitepieces.append(newPiece)
    else:
        app.blackpieces.remove(promotedPawn)
        app.blackpieces.append(newPiece)


def redrawAll(app):
    #menu screen
    if(not app.gameStarted):
        if app.gameMode is None:
            # Main menu - game mode selection - NO IMAGES
            drawRect(0, 0, app.width, app.height, fill='lightblue')
            drawLabel("C h e s s  G a m e", app.width//2, 60, 
                     font="Georgia", size=30, bold=True)
            
            drawLabel("Graphics working! No images for now.", app.width//2, 120, 
                     font="Georgia", size=16, bold=True, fill='green')
            
            # Game mode buttons
            buttonWidth = 300
            buttonHeight = 60
            buttonX = app.width//2 - buttonWidth//2
            drawRect(buttonX, 350, buttonWidth, buttonHeight, fill='white', border='black', borderWidth=2)
            drawLabel("Human vs Human", app.width//2, 380, font="Georgia", size=20, bold=True)
            
            drawRect(buttonX, 430, buttonWidth, buttonHeight, fill='lightgreen', border='black', borderWidth=2)
            drawLabel("Human vs Computer", app.width//2, 460, font="Georgia", size=20, bold=True)
            
            drawLabel("Coded by Andy Xu 15-112", app.width//2, app.height-50,
                     font="Georgia", size=15, italic=True)
            
        elif app.gameMode == 'computer' and app.difficulty is None:
            # Difficulty selection menu
            drawRect(0, 0, app.width, app.height, fill='lightgray')
            drawLabel("Select Difficulty", app.width//2, 60, 
                     font="Georgia", size=30, bold=True)
            
            # Difficulty buttons
            buttonWidth = 300
            buttonHeight = 60
            buttonX = app.width//2 - buttonWidth//2
            drawRect(buttonX, 300, buttonWidth, buttonHeight, fill='lightgreen', border='black', borderWidth=2)
            drawLabel("Easy", app.width//2, 330, font="Georgia", size=20, bold=True)
            
            drawRect(buttonX, 380, buttonWidth, buttonHeight, fill='yellow', border='black', borderWidth=2)
            drawLabel("Medium", app.width//2, 410, font="Georgia", size=20, bold=True)
            
            drawRect(buttonX, 460, buttonWidth, buttonHeight, fill='orange', border='black', borderWidth=2)
            drawLabel("Hard", app.width//2, 490, font="Georgia", size=20, bold=True)
            
            # Back button
            drawRect(50, app.height - 80, 120, 40, fill='gray', border='black', borderWidth=2)
            drawLabel("Back", 110, app.height - 60, font="Georgia", size=16, bold=True)
        
        else:
            # Old start screen for human vs human
            drawRect(0, 0, app.width, app.height, fill='lightyellow')
            drawLabel("T w o  P l a y e r  C h e s s", app.width//2, 60, 
                     font="Georgia", size=30, bold=True)
            drawLabel("CLICK P TO START PLAYING", app.width//2, app.height-100,
                     font="Georgia", size=25, bold=True)
            drawLabel("Coded by Andy Xu 15-112", app.width//2, app.height-50,
                     font="Georgia", size=15, italic=True)
    #board, eval bar, taken pieces, move counter, etc.
    #for when the game truly starts
    if(app.gameStarted):
        # Game title
        if app.gameMode == 'human':
            drawLabel('2P CHESS', app.width/2, 35, 
                     font='Arial', size=22, bold=True)
        else:
            drawLabel(f'CHESS vs AI ({app.difficulty.upper()})', app.width/2, 35,
                     font='Arial', size=22, bold=True)
        
        #displays whose turn it is
        if app.gameMode == 'computer' and app.computerThinking:
            drawLabel('Computer thinking...', app.width/2 + 300, 35, 
                     font='Arial', size=20, bold=True, fill='red')
        elif(app.turn):
            turnText = 'Turn: White'
            if app.gameMode == 'computer' and app.computerPlayer == 'white':
                turnText += ' (AI)'
            drawLabel(turnText, app.width/2 + 300, 35, 
                     font='Arial', size=20, bold=True)
        else:
            turnText = 'Turn: Black'
            if app.gameMode == 'computer' and app.computerPlayer == 'black':
                turnText += ' (AI)'
            drawLabel(turnText, app.width/2 + 300, 35, 
                     font='Arial', size=20, bold=True)
        drawLabel(f'Moves: {app.numTurns}', app.width/2 - 300, 35,
                 font='Arial', size=20, bold=True)
        drawBoard(app)
        drawTakenPieces(app)
        drawUndoButton(app)
        drawResetButton(app)
        drawPieces(app)
        #if the first click is on a piece, show the moves for that piece
        if(app.firstclickwork):
            if(app.plist[app.prevclick[0]][app.prevclick[1]] != None):
                moves = app.plist[app.prevclick[0]][app.prevclick[1]].moves(app.plist)
                actualmoves = actualMoves(app, moves)
                for move in actualmoves:
                    #checks for 'hit', if hit then make red
                    if(len(move) < 3 or (len(move) > 2 and move[2] == 2)):
                        drawMoves(app, move[0], move[1], False)
                    elif(move[2]=='hit'):
                        drawMoves(app, move[0], move[1], True)
                    elif(move[2]=='wqcastled' or move[2]=='bqcastled' or 
                        move[2]=='bkcastled' or move[2]=='wkcastled'):
                        drawMoves(app, move[0], move[1], None)
                    elif(move[2]=='wlenpassant' or move[2]=='wrenpassant'
                        or move[2]=='blenpassant' or move[2]=='brenpassant'):
                        drawMoves(app, move[0], move[1], 'e')
        drawEvalBar(app)
        #checkmate will display the victory message
        if(app.gameOver):
            drawGameOver(app)

def drawGameOver(app):
    drawRect(60, app.height/2 - 30, app.width-120, 60, fill='chartreuse')
    if(app.winner=='White'):
        drawLabel('Good Game, The Winner Is White', app.width/2, app.height/2,
                 font='Arial', size=20, bold=True)
        drawImage(app.wvictory, app.width/2, app.height/2 + 50, 
                 width=200, height=150, align='center')
    elif(app.winner=='Black'):
        drawLabel('Good Game, The Winner Is Black', app.width/2, app.height/2,
                 font='Arial', size=20, bold=True)
        drawImage(app.bvictory, app.width/2, app.height/2 + 50, 
                 width=200, height=150, align='center')
    else:
        drawLabel('STALEMATE', app.width/2, app.height/2,
                 font='Arial', size=24, bold=True)
        drawImage(app.stalemate, app.width/2, app.height/2 + 50, 
                 width=200, height=150, align='center')

#boundaries adjusted for larger screen
def drawUndoButton(app):
    buttonWidth = app.width/8
    buttonHeight = 55
    buttonX = app.width - buttonWidth - 20
    buttonY = app.margin + app.cellSize * 8 + 20
    drawRect(buttonX, buttonY, buttonWidth, buttonHeight,
             fill='black', border='black', borderWidth=3)
    drawLabel('UNDO', buttonX + buttonWidth/2, buttonY + buttonHeight/2, 
             fill='white', font="Helvetica", size=16, bold=True)

#boundaries adjusted for larger screen
def drawResetButton(app):
    buttonWidth = app.width/8
    buttonHeight = 55
    buttonX = app.width - buttonWidth - 20
    buttonY = app.margin + app.cellSize * 8 + 90
    drawRect(buttonX, buttonY, buttonWidth, buttonHeight,
             fill='white', border='black', borderWidth=3)
    drawLabel('RESET', buttonX + buttonWidth/2, buttonY + buttonHeight/2, 
             fill='black', font="Helvetica", size=16, bold=True)

def drawBoard(app):
    for i in range(8):
        for j in range(8):
            # Calculate checkerboard pattern directly
            color = "white" if ((i + j) % 2 == 0) else "gray"
            drawCell(app, i, j, color)

def drawTakenPieces(app):
    #draws all of the pieces on the edge of the board to show taken
    whitepawns, whiteknights, whitebishops, whiterooks, whitequeens = [],[],[],[],[]
    blackpawns, blackknights, blackbishops, blackrooks, blackqueens = [],[],[],[],[]
    whites = []
    blacks = []
    for piece in app.whitetakenpieces:
        if(type(piece)==pawn):
            whitepawns.append(piece)
        elif(type(piece)==knight):
            whiteknights.append(piece)
        elif(type(piece)==bishop):
            whitebishops.append(piece)
        elif(type(piece)==rook):
            whiterooks.append(piece)
        elif(type(piece)==queen):
            whitequeens.append(piece)
    whites.extend(whitepawns)
    whites.extend(whiteknights)
    whites.extend(whitebishops)
    whites.extend(whiterooks)
    whites.extend(whitequeens)
    for piece in app.blacktakenpieces:
        if(type(piece)==pawn):
            blackpawns.append(piece)
        elif(type(piece)==knight):
            blackknights.append(piece)
        elif(type(piece)==bishop):
            blackbishops.append(piece)
        elif(type(piece)==rook):
            blackrooks.append(piece)
        elif(type(piece)==queen):
            blackqueens.append(piece)
    blacks.extend(blackpawns)
    blacks.extend(blackknights)
    blacks.extend(blackbishops)
    blacks.extend(blackrooks)
    blacks.extend(blackqueens)
    for ind in range(len(whites)):
        # Draw small text representation of captured pieces
        pieceChar = ''
        if(type(whites[ind])==pawn):
            pieceChar = 'p'
        elif(type(whites[ind])==rook):
            pieceChar = 'r'
        elif(type(whites[ind])==queen):
            pieceChar = 'q'
        elif(type(whites[ind])==knight):
            pieceChar = 'n'
        elif(type(whites[ind])==bishop):
            pieceChar = 'b'
        
        x = app.margin//2-app.margin//6 if (ind%2==0) else app.margin//2+app.margin//6
        y = app.margin*0.5+app.cellSize*8-ind*(app.margin//4)
        drawLabel(pieceChar, x, y, font='Arial', size=10, bold=True, fill='black')
        
    for ind in range(len(blacks)):
        # Draw small text representation of captured pieces
        pieceChar = ''
        if(type(blacks[ind])==pawn):
            pieceChar = 'P'
        elif(type(blacks[ind])==rook):
            pieceChar = 'R'
        elif(type(blacks[ind])==queen):
            pieceChar = 'Q'
        elif(type(blacks[ind])==knight):
            pieceChar = 'N'
        elif(type(blacks[ind])==bishop):
            pieceChar = 'B'
        
        x = app.margin//2-app.margin//6 if (ind % 2 == 0) else app.margin//2+app.margin//6
        y = app.margin*1.5+ind*(app.margin//4)
        drawLabel(pieceChar, x, y, font='Arial', size=10, bold=True, fill='white')

def drawEvalBar(app):
    #advantage is based on the pieces on the board. Thus, promotions will gain points
    advantage = 0
    for piece in app.whitepieces:
        if(type(piece)==pawn):
            advantage+=1
        elif(type(piece)==bishop or type(piece)==knight):
            advantage+=3
        elif(type(piece)==rook):
            advantage+=5
        elif(type(piece)==queen):
            advantage+=9
    for piece in app.blackpieces:
        if(type(piece)==pawn):
            advantage-=1
        elif(type(piece)==bishop or type(piece)==knight):
            advantage-=3
        elif(type(piece)==rook):
            advantage-=5
        elif(type(piece)==queen):
            advantage-=9
    
    # Calculate bar dimensions properly
    maxAdvantage = 40  # Maximum expected advantage (for scaling)
    barHeight = 25
    barY = app.height - app.margin - 10
    barCenterX = app.width // 2
    barHalfWidth = app.width // 4  # Half the bar width
    
    # Draw title label (higher up to avoid overlap)
    drawLabel('EVALUATION BAR', app.width//2, barY - 35,
             font='Arial', size=14, bold=True)
    
    # Draw background bar
    drawRect(barCenterX - barHalfWidth, barY, barHalfWidth * 2, barHeight,
             fill='lightgray', border='black', borderWidth=2)
    
    # Draw evaluation bar rectangle
    if advantage != 0:
        # Scale advantage to bar width (clamp to maxAdvantage)
        clampedAdvantage = max(-maxAdvantage, min(maxAdvantage, advantage))
        barWidth = abs(clampedAdvantage / maxAdvantage * barHalfWidth * 2)
        
        if advantage > 0:
            # White advantage - extend right from center
            barX = barCenterX
            drawRect(barX, barY, barWidth, barHeight, fill='white', border='black', borderWidth=2)
        else:
            # Black advantage - extend left from center
            barX = barCenterX - barWidth
            drawRect(barX, barY, barWidth, barHeight, fill='black', border='white', borderWidth=2)
    
    # Draw center line
    drawLine(barCenterX, barY, barCenterX, barY + barHeight, 
             fill='black', lineWidth=2)
    
    # Draw advantage value (below the bar)
    drawLabel(str(advantage), app.width//2, barY + barHeight + 20,
             font='Arial', size=14, bold=True)

#d is for castle, en passant, hits, and normal moves
def drawMoves(app, moverow, movecol, d):
    x = app.margin + app.cellSize * (movecol + 0.5)
    y = app.margin + app.cellSize * (moverow + 0.5)
    radius = app.cellSize * 0.1
    
    if(d == None):
        drawCircle(x, y, radius, fill='yellow')
    elif(d == True):
        drawCircle(x, y, radius, fill='red')
    elif(d == 'e'):
        drawCircle(x, y, radius, fill='blue')
    else:
        drawCircle(x, y, radius, fill='green')

#paraphrased from HW6 Tetris, used to draw the 8x8 chessboard
def drawCell(app, row, col, color):
    drawRect(app.margin+app.cellSize*col, 
             app.margin+app.cellSize*row, 
             app.cellSize, app.cellSize, 
             fill=color, border="black", borderWidth=3)

#paraphrased from HW6 Tetris
def drawPieces(app):
    for i in range(8):
        for j in range(8):
            d = app.plist[i][j]
            if(d!=None):
                # Check if this piece is being animated
                if (app.animatingPiece is not None and 
                    app.animatingPiece == d and 
                    app.animationProgress < 1.0):
                    # Redraw board squares that the piece passes over during animation
                    # This ensures the correct checkerboard pattern shows through
                    if app.animationStartPos is not None:
                        startRow, startCol = app.animationStartPos
                        endRow, endCol = app.animationEndPos
                        # Redraw source square (now empty) with correct checkerboard color
                        startColor = "white" if ((startRow + startCol) % 2 == 0) else "gray"
                        drawCell(app, startRow, startCol, startColor)
                        # Redraw destination square if different (may have captured piece)
                        if startRow != endRow or startCol != endCol:
                            endColor = "white" if ((endRow + endCol) % 2 == 0) else "gray"
                            drawCell(app, endRow, endCol, endColor)
                    
                    # Draw piece at animated position
                    startX = app.margin + app.cellSize * (app.animationStartPos[1] + 0.5)
                    startY = app.margin + app.cellSize * (app.animationStartPos[0] + 0.5)
                    endX = app.margin + app.cellSize * (app.animationEndPos[1] + 0.5)
                    endY = app.margin + app.cellSize * (app.animationEndPos[0] + 0.5)
                    
                    # Interpolate position with easing
                    progress = app.animationProgress
                    # Easing function for smooth animation
                    easedProgress = progress * (2 - progress)  # Ease out
                    
                    currentX = startX + (endX - startX) * easedProgress
                    currentY = startY + (endY - startY) * easedProgress
                    
                    # Draw piece at animated position
                    size = app.cellSize * 0.9
                    if type(d) == king:
                        image = app.wking if d.getColor() == 'white' else app.bking
                    elif type(d) == queen:
                        image = app.wqueen if d.getColor() == 'white' else app.bqueen
                    elif type(d) == rook:
                        image = app.wrook if d.getColor() == 'white' else app.brook
                    elif type(d) == bishop:
                        image = app.wbishop if d.getColor() == 'white' else app.bbishop
                    elif type(d) == knight:
                        image = app.wknight if d.getColor() == 'white' else app.bknight
                    elif type(d) == pawn:
                        image = app.wpawn if d.getColor() == 'white' else app.bpawn
                    else:
                        image = None
                    
                    if image:
                        drawImage(image, currentX, currentY, width=size, height=size, align='center')
                else:
                    # Draw piece normally (but skip if it's the animating piece at its old position)
                    if (app.animatingPiece is not None and 
                        app.animatingPiece == d and 
                        [i, j] == app.animationStartPos):
                        # Don't draw at old position during animation
                        continue
                    # Draw piece - board square already drawn by drawBoard()
                    drawP(app, i, j, d)

#draws the piece
def drawP(app, row, col, piece):
    # Draw piece images
    x = app.margin+app.cellSize*(col+0.5)
    y = app.margin+app.cellSize*(row+0.5)
    size = app.cellSize * 0.9
    
    # Get the appropriate image based on piece type and color
    if type(piece) == king:
        image = app.wking if piece.getColor() == 'white' else app.bking
    elif type(piece) == queen:
        image = app.wqueen if piece.getColor() == 'white' else app.bqueen
    elif type(piece) == rook:
        image = app.wrook if piece.getColor() == 'white' else app.brook
    elif type(piece) == bishop:
        image = app.wbishop if piece.getColor() == 'white' else app.bbishop
    elif type(piece) == knight:
        image = app.wknight if piece.getColor() == 'white' else app.bknight
    elif type(piece) == pawn:
        image = app.wpawn if piece.getColor() == 'white' else app.bpawn
    else:
        return
    
    # Draw the image centered on the square
    drawImage(image, x, y, width=size, height=size, align='center')

#runs the game
def main():
    global app, _app_instance
    width, height = 900, 950
    
    # Create game instance
    app = Game(width, height)
    _app_instance = app  # Set for wrapper functions
    
    # Initialize game state (equivalent to onAppStart)
    onAppStart(app)
    
    # Main game loop
    running = True
    FPS = 60
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouseX, mouseY = event.pos
                    onMousePress(app, mouseX, mouseY)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and not app.gameStarted:
                    if app.gameMode == 'human':
                        app.gameStarted = True
        
        # Update animation (equivalent to onStep)
        if app.animatingPiece is not None:
            app.animationProgress += app.animationSpeed
            if app.animationProgress >= 1.0:
                app.animationProgress = 1.0
                # Animation complete - clear the piece from source position
                if app.animationStartPos is not None:
                    app.plist[app.animationStartPos[0]][app.animationStartPos[1]] = None
                app.animatingPiece = None
                app.animationStartPos = None
                app.animationEndPos = None
                app.animationProgress = 0.0
        
        # Computer move logic (if it's computer's turn and no animation)
        if (app.gameStarted and not app.gameOver and 
            app.gameMode == 'computer' and 
            app.animatingPiece is None and
            not app.computerThinking):
            currentPlayer = 'white' if app.turn else 'black'
            if currentPlayer == app.computerPlayer:
                app.computerThinking = True
                computerMove = getComputerMove(app)
                if computerMove:
                    piece, move = computerMove
                    executeMove(app, piece, move)
                app.computerThinking = False
        
        # Redraw everything
        app.screen.fill(COLORS.get('white', (255, 255, 255)))
        redrawAll(app)
        pygame.display.flip()
        
        # Control frame rate
        app.clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()