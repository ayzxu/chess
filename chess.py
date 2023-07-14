import math, copy, random

from cmu_112_graphics import *

def gameDimensions():
    rows = 8
    cols = 8
    cellSize = 60
    margin = 60
    return (rows, cols, cellSize, margin)

def appStarted(app):
    d = gameDimensions()
    #checks for checkmate, returns winner when over
    app.gameStarted = False
    app.gameOver = False
    app.winner = ''

    #holds the previous click so each player can think and highlight moves
    app.prevclick = None
    app.firstclickwork = False
    #True is white's move, False is black's move
    app.numTurns = 0
    app.turn = True
    
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
    app.bvictory = app.loadImage("bvictory.png")

    #CITATION image taken by NBA, Lebron James dunking on Isaiah Thomas
    #courtesy of Bob DeChiaria USA Today
    #photoshopped by Andy xu
    app.wvictory = app.loadImage("wvictory.png")

    #CITATION image taken from Spiderman Original 
    app.stalemate = app.loadImage("stalemate.png")

    #CITATION menu screen taken from Olympia, Arnold Schwarzenegger 
    #and Ronnie Coleman free stock, photoshopped by me
    app.menu = app.loadImage("Menu.png")

    #CITATION Muscle Letter P taken from P stock image
    app.p = app.loadImage("P.png")

    #CITATION Chess pieces taken from chess.com free to use
    app.bking = app.loadImage(app.blackking.image)
    app.bbishop = app.loadImage(app.blackbishop2.image)
    app.bknight = app.loadImage(app.blackknight2.image)
    app.brook = app.loadImage(app.blackrook1.image)
    app.bpawn = app.loadImage(app.blackpawn1.image)
    app.bqueen = app.loadImage(app.blackqueen.image)
    app.wking = app.loadImage(app.whiteking.image)
    app.wbishop = app.loadImage(app.whitebishop2.image)
    app.wknight = app.loadImage(app.whiteknight1.image)
    app.wrook = app.loadImage(app.whiterook1.image)
    app.wpawn = app.loadImage(app.whitepawn1.image)
    app.wqueen = app.loadImage(app.whitequeen.image)
    
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
    actualmoves = []
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
    app.gameStarted = False
    app.winner = ""
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

def keyPressed(app, event):
    if(event.key == 'p'):
        app.gameStarted = True

def mousePressed(app, event):
    #as long as game is not over and game hasn't started (menu screen)
    if(not app.gameStarted):
        if(event.x > 150 and event.y > 510 and event.x < 200 and event.y < 560):
            app.gameStarted = True
            return
    if(app.gameStarted):
        if(event.x > 545 and event.x < 595 and event.y > 305 and event.y < 355):
            restartGame(app)
            app.gameStarted = False
            return
    if(not app.gameOver and app.gameStarted):
        if(event.x > 545 and event.x < 595 and event.y > 245 and event.y < 295):
            if(len(app.undoList) >= 1):
                undoMove(app)
        dx = ((event.x - app.margin)//app.cellSize)
        #insures in bounds, no out of bounds for window
        if (dx > 7 or dx < 0):
            return
        dy = ((event.y - app.margin)//app.cellSize)
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
                    app.plist[app.prevclick[0]][app.prevclick[1]].row = move[0]
                    app.plist[app.prevclick[0]][app.prevclick[1]].col = move[1]
                    app.plist[move[0]][move[1]] = app.plist[
                        app.prevclick[0]][app.prevclick[1]]
                    app.plist[app.prevclick[0]][app.prevclick[1]] = None
                    promotionSquare = app.plist[move[0]][move[1]]
                    #checking if pawn reached the last rank, if so, prompt a piece to promote
                    if(type(promotionSquare)==pawn):
                        if(promotionSquare.needPromotion()):
                            promotedPiece = app.getUserInput("What piece would you like to promote to? \n k for knight, q for queen, r for rook, and b for bishop.")
                            while ((promotedPiece != "k") and (promotedPiece != "r") and (promotedPiece!= "q") and (promotedPiece!= "b")):
                                app.showMessage("Bruh try again and do better.\n k for knight, q for queen, r for rook, and b for bishop.")
                                promotedPiece = app.getUserInput("What piece would you like to promote to? \n k for knight, q for queen, r for rook, and b for bishop.")
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

def redrawAll(app, canvas):
    #menu screen
    if(not app.gameStarted):
        canvas.create_image(app.width//2, app.height//2-20, 
            image=ImageTk.PhotoImage(app.menu))
        canvas.create_text(app.width//2, 60, text = "T w o  P l a y e r  C h e s s", 
        font = ("Georgia", "30", "bold"))
        canvas.create_text(app.width//2, app.height-100, text = "CLICK          TO START PLAYING",
        font = ("Georgia 25 bold"))
        canvas.create_text(app.width//2, app.height-50, text = "Coded by Andy Xu 15-112",
        font = ("Georgia 15 italic"))
        p = app.scaleImage(app.p, 0.8)
        canvas.create_image(180, app.height-100, 
            image=ImageTk.PhotoImage(p))
    #board, eval bar, taken pieces, move counter, etc.
    #for when the game truly starts
    if(app.gameStarted):
        canvas.create_text(app.width/2, 30, text = '2P CHESS',
        font = 'Arial 17 bold')
        #displays whose turn it is
        if(app.turn):
            canvas.create_text(app.width/2 + 200, 30, text = 'Turn: White', 
            font = 'Arial 17 bold')
        else:
            canvas.create_text(app.width/2 + 200, 30, text = 'Turn: Black', 
            font = 'Arial 17 bold')
        canvas.create_text(app.width/2 - 200, 30, text = f'Moves: {app.numTurns}',
            font = 'Arial 17 bold')
        drawBoard(app, canvas)
        drawTakenPieces(app, canvas)
        drawUndoButton(app, canvas)
        drawResetButton(app, canvas)
        drawPieces(app, canvas)
        #if the first click is on a piece, show the moves for that piece
        if(app.firstclickwork):
            if(app.plist[app.prevclick[0]][app.prevclick[1]] != None):
                moves = app.plist[app.prevclick[0]][app.prevclick[1]].moves(app.plist)
                actualmoves = actualMoves(app, moves)
                for move in actualmoves:
                    #checks for 'hit', if hit then make red
                    if(len(move) < 3 or (len(move) > 2 and move[2] == 2)):
                        drawMoves(app, canvas, move[0], move[1], False)
                    elif(move[2]=='hit'):
                        drawMoves(app, canvas, move[0], move[1], True)
                    elif(move[2]=='wqcastled' or move[2]=='bqcastled' or 
                        move[2]=='bkcastled' or move[2]=='wkcastled'):
                        drawMoves(app, canvas, move[0], move[1], None)
                    elif(move[2]=='wlenpassant' or move[2]=='wrenpassant'
                        or move[2]=='blenpassant' or move[2]=='brenpassant'):
                        drawMoves(app, canvas, move[0], move[1], 'e')
        drawEvalBar(app, canvas)
        #checkmate will display the victory message
        if(app.gameOver):
            drawGameOver(app, canvas)

def drawGameOver(app, canvas):
    canvas.create_rectangle(60, app.height/2 + 30, app.width-60, app.height/2 - 30, fill = 'chartreuse')
    if(app.winner=='White'):
        canvas.create_text(app.width/2, app.height/2, text = 'Good Game, The Winner Is White',
            font = 'Arial 20 bold')
        canvas.create_image(app.width//2, app.height//2-150,
            image=ImageTk.PhotoImage(app.wvictory))
    elif(app.winner=='Black'):
        canvas.create_text(app.width/2, app.height/2, text = 'Good Game, The Winner Is Black',
            font = 'Arial 20 bold')
        canvas.create_image(app.width//2, app.height//2-130,
            image=ImageTk.PhotoImage(app.bvictory))
    else:
        canvas.create_text(app.width/2, app.height/2, text = 'STALEMATE',
            font = 'Arial 24 bold')
        canvas.create_image(app.width//2, app.height//2-115,
            image=ImageTk.PhotoImage(app.stalemate))

#boundaries are 545, 595 x and 245, 295 y
def drawUndoButton(app, canvas):
    canvas.create_rectangle(app.width-app.width/10+5, 245, app.width-5, 295,
        fill = 'black', width = 3)
    canvas.create_text(app.width-30, 270, text = 'UNDO', fill = 'white', 
        font = ("Helvetica Bg", "12", "bold"))

#boundaries are 545, 595 x and 305, 355 y
def drawResetButton(app, canvas):
    canvas.create_rectangle(app.width-app.width/10+5, 305, app.width-5, 355,
    fill = 'white', width = 3)
    canvas.create_text(app.width-30, 330, text = 'RESET', fill = 'black',
        font = ("Helvetica Bg", "10", "bold"))

def drawBoard(app, canvas):
    for i in range(8):
        for j in range(8):
            drawCell(app, canvas, i, j, app.board[i][j][0])

def drawTakenPieces(app, canvas):
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
        if(type(whites[ind])==pawn):
            t = app.bpawn
        elif(type(whites[ind])==rook):
            t = app.brook
        elif(type(whites[ind])==queen):
            t = app.bqueen
        elif(type(whites[ind])==knight):
            t = app.bknight
        elif(type(whites[ind])==bishop):
            t = app.bbishop
        smallt = app.scaleImage(t, 1/2)
        if(ind%2==0):
            canvas.create_image(app.margin//2-app.margin//6,
            app.margin*0.5+app.cellSize*8-ind*(app.margin//4), 
            image=ImageTk.PhotoImage(smallt))
        else:
            canvas.create_image(app.margin//2+app.margin//6,
            app.margin*0.5+app.cellSize*8-ind*(app.margin//4), 
            image=ImageTk.PhotoImage(smallt))
    for ind in range(len(blacks)):
        if(type(blacks[ind])==pawn):
            t = app.wpawn 
        elif(type(blacks[ind])==rook):
            t = app.wrook
        elif(type(blacks[ind])==queen):
            t = app.wqueen
        elif(type(blacks[ind])==knight):
            t = app.wknight
        elif(type(blacks[ind])==bishop):
            t = app.wbishop
        smallt = app.scaleImage(t, 1/2)
        if(ind % 2 == 0):
            canvas.create_image(app.margin//2-app.margin//6,
            app.margin*1.5+ind*(app.margin//4), 
            image=ImageTk.PhotoImage(smallt))
        else:
            canvas.create_image(app.margin//2+app.margin//6,
            app.margin*1.5+ind*(app.margin//4), 
            image=ImageTk.PhotoImage(smallt))

def drawEvalBar(app, canvas):
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
            advantage+=8
    for piece in app.blackpieces:
        if(type(piece)==pawn):
            advantage-=1
        elif(type(piece)==bishop or type(piece)==knight):
            advantage-=3
        elif(type(piece)==rook):
            advantage-=5
        elif(type(piece)==queen):
            advantage-=8
    canvas.create_text(app.width//2, app.height-app.margin//3, text = 
        'EVALUATION BAR', font = 'Arial 15 bold')
    canvas.create_line(app.width//2, app.height-app.margin//2-10, app.width, 
        app.height-app.margin//2-10, width = 5, fill = 'black')
    canvas.create_line(0, app.height-app.margin//2-10, app.width//2, 
        app.height-app.margin//2-10, width = 5, fill = 'light gray')
    canvas.create_rectangle(app.width//2, app.height-app.margin+5, 
        app.width//2-advantage*8, app.height-app.margin, fill = 'gray')
    canvas.create_text(app.width//2, app.height-app.margin*1.25, 
        text = str(advantage), font = 'Arial 15 bold')

#d is for castle, en passant, hits, and normal moves
def drawMoves(app, canvas, moverow, movecol, d):
    if(d == None):
        canvas.create_oval(app.margin+app.cellSize*(movecol + 0.4), 
            app.margin+app.cellSize*(moverow + 0.4), app.margin + 
            app.cellSize*(movecol+0.6), app.margin+app.cellSize*(moverow+0.6),
            fill = 'yellow', width = 0)
    elif(d == True):
        canvas.create_oval(app.margin+app.cellSize*(movecol + 0.4), 
            app.margin+app.cellSize*(moverow + 0.4), app.margin + 
            app.cellSize*(movecol+0.6), app.margin+app.cellSize*(moverow+0.6),
            fill = 'red', width = 0)
    elif(d == 'e'):
        canvas.create_oval(app.margin+app.cellSize*(movecol + 0.4), 
            app.margin+app.cellSize*(moverow + 0.4), app.margin + 
            app.cellSize*(movecol+0.6), app.margin+app.cellSize*(moverow+0.6),
            fill = 'blue', width = 0)
    else:
        canvas.create_oval(app.margin+app.cellSize*(movecol + 0.4), 
            app.margin+app.cellSize*(moverow + 0.4), app.margin + 
            app.cellSize*(movecol+0.6), app.margin+app.cellSize*(moverow+0.6),
            fill = 'green', width = 0)

#paraphrased from HW6 Tetris, used to draw the 8x8 chessboard
def drawCell(app, canvas, row, col, color):
    canvas.create_rectangle(app.margin+app.cellSize*col, 
    app.margin+app.cellSize*row, 
    app.margin+app.cellSize*(col+1), app.margin+app.cellSize*(row+1), fill =
    color, outline = "black", width=3)

#paraphrased from HW6 Tetris
def drawPieces(app, canvas):
    for i in range(8):
        for j in range(8):
            d = app.plist[i][j]
            if(d!=None):
                if(type(d)==pawn and 
                    d.getColor()=='black'):
                    drawP(app, canvas, i, j, app.bpawn)
                elif(type(d)==queen and
                    d.getColor()=='black'):
                    drawP(app, canvas, i, j, app.bqueen)
                elif(type(d)==rook and
                    d.getColor()=='black'):
                    drawP(app, canvas, i, j, app.brook)
                elif(type(d)==knight and
                    d.getColor()=='black'):
                    drawP(app, canvas, i, j, app.bknight)
                elif(type(d)==king and
                    d.getColor()=='black'):
                    drawP(app, canvas, i, j, app.bking)
                elif(type(d)==bishop and
                    d.getColor()=='black'):
                    drawP(app, canvas, i, j, app.bbishop)
                if(type(d)==pawn and 
                    d.getColor()=='white'):
                    drawP(app, canvas, i, j, app.wpawn)
                elif(type(d)==queen and
                    d.getColor()=='white'):
                    drawP(app, canvas, i, j, app.wqueen)
                elif(type(d)==rook and
                    d.getColor()=='white'):
                    drawP(app, canvas, i, j, app.wrook)
                elif(type(d)==knight and
                    d.getColor()=='white'):
                    drawP(app, canvas, i, j, app.wknight)
                elif(type(d)==king and
                    d.getColor()=='white'):
                    drawP(app, canvas, i, j, app.wking)
                elif(type(d)==bishop and
                    d.getColor()=='white'):
                    drawP(app, canvas, i, j, app.wbishop)

#draws the piece
def drawP(app, canvas, row, col, piece):
    canvas.create_image(app.margin+app.cellSize*(col+0.5),
    app.margin+app.cellSize*(row+0.5), image=ImageTk.PhotoImage(piece))

#runs the game
def playChess():
    runApp(width = 600, height = 640)

# ___________________________________

def main():
    playChess()

if __name__ == '__main__':
    main()