from mysql import connector
from dao import *
import pygame
import json

pygame.init()
pygame.mixer.init()
move_sound = pygame.mixer.Sound("./assets/move-self.mp3")
clickSound = pygame.mixer.Sound("./assets/clickSound.wav")
clock = pygame.time.Clock()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAME_WIDTH = 600
FRAME_HEIGHT = 513
BOARD_X = 115
BOARD_Y = 69
CUBE_SIZE= 50

font = pygame.font.Font("assets/fonts/Alkhemikal.ttf", 36)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

torch = pygame.image.load("./assets/torch.png").convert_alpha()
torch = pygame.transform.scale(torch, (250, 200))

arrow = pygame.image.load("./assets/arrow.png").convert_alpha()
arrow = pygame.transform.scale(arrow, (250, 200))

background = pygame.image.load("./assets/background.png").convert_alpha()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

frame = pygame.image.load("./assets/frame.png").convert_alpha()
frame = pygame.transform.scale(frame, (FRAME_WIDTH,FRAME_HEIGHT))

whitePiece = pygame.image.load("./assets/whitePiece.png").convert_alpha()
whitePiece = pygame.transform.scale(whitePiece, (40, 40))

blackPiece = pygame.image.load("./assets/blackPiece.png").convert_alpha()
blackPiece = pygame.transform.scale(blackPiece, (40, 40)) 

promoWhite = pygame.image.load("./assets/promotedWhite.png").convert_alpha()
promoWhite = pygame.transform.scale(promoWhite, (40, 40))

promoBlack = pygame.image.load("./assets/promotedBlack.png").convert_alpha()
promoBlack = pygame.transform.scale(promoBlack, (40, 40)) 

selectedWhite = pygame.image.load("./assets/selectedWhite.png").convert_alpha()
selectedWhite = pygame.transform.scale(selectedWhite, (40, 40))

selectedBlack = pygame.image.load("./assets/selectedBlack.png").convert_alpha()
selectedBlack = pygame.transform.scale(selectedBlack, (40, 40))

selectedWhitePromo = pygame.image.load("./assets/selectedWhitePromo.png").convert_alpha()
selectedWhitePromo = pygame.transform.scale(selectedWhitePromo, (40, 40))

selectedBlackPromo = pygame.image.load("./assets/selectedBlackPromo.png").convert_alpha()
selectedBlackPromo = pygame.transform.scale(selectedBlackPromo, (40, 40))

frameEnd = pygame.image.load("./assets/endingFrame.png").convert_alpha()
frameEnd = pygame.transform.scale(frameEnd, (600, 400))

menuFrame = pygame.image.load("./assets/menuFrame.png").convert_alpha()
menuFrame = pygame.transform.scale(menuFrame, (400, 350))

def getConnection():
    return connector.connect(
        user='root', 
        password='',
        database='db_game',
        host='127.0.0.1',
        port=3306
    )

class pieces:
    def __init__(self,x,y,color,image):
        self.x= x
        self.y= y
        self.xInBoard = (x - BOARD_X) // CUBE_SIZE
        self.yInBoard = (y - BOARD_Y) // CUBE_SIZE
        self.color= color
        self.image= image
        self.promoted= False

    def draw(self,surface):
        surface.blit(self.image, (self.x,self.y))    

def draw_board(boardX,boardY):
    place_x= boardX
    place_y= boardY
    index = 1

    for j in range(8):
        for i in range(8):
            if index == 1:
                square = pygame.Rect((place_x,place_y,50,50))
                pygame.draw.rect(screen,(200,200,200), square)
            else:
                square = pygame.Rect((place_x,place_y,50,50))
                pygame.draw.rect(screen,(0,0,100), square)
                    
            place_x += CUBE_SIZE
            index = index * -1
        place_y += CUBE_SIZE   
        place_x = boardX
        index = index * -1

def deployPieces(boardX,boardY):

    piecesList = []

    index = 1
    for row in range(3):
        for col in range(8):
            if index == -1:
                x = col * CUBE_SIZE + 5 + boardX
                y = row * CUBE_SIZE + 5 + boardY
                piecesList.append(pieces(x, y,'white', whitePiece))
            index *= -1    
        index *= -1    
    for row in range(5, 8):
        for col in range(8):
            if index == -1:
                x = col * CUBE_SIZE + 5 + boardX
                y = row * CUBE_SIZE + 5 + boardY
                piecesList.append(pieces(x, y,'black', blackPiece))
            index *= -1    
        index *= -1

    return piecesList    

def isSpotEmpty(piecesList,x,y):
    if x < 0 or y < 0 or x > 7 or y > 7:
        return False
    for piece in piecesList:
        piece_x = (piece.x - BOARD_X) // CUBE_SIZE
        piece_y = (piece.y - BOARD_Y) // CUBE_SIZE
        if piece_x == x and piece_y == y:
            return piece
    return True

def getColor(piecesList,x,y):
    if x < 0 or y < 0 or x > 7 or y > 7:
        return False
    for piece in piecesList:
        piece_x = (piece.x - BOARD_X) // CUBE_SIZE
        piece_y = (piece.y - BOARD_Y) // CUBE_SIZE
        if piece_x == x and piece_y == y:
            return piece.color

def availablePlaces(thePiece,piecesList,turn):
    available = []
    thePieceSquareX = (thePiece.x - BOARD_X) // CUBE_SIZE
    thePieceSquareY = (thePiece.y - BOARD_Y) // CUBE_SIZE
    if thePiece.color == 'black'and turn == -1:
        if isSpotEmpty(piecesList,thePieceSquareX-1,thePieceSquareY-1) == True:
            square = pygame.Rect((thePiece.x-55,thePiece.y-55,CUBE_SIZE,CUBE_SIZE))
            pygame.draw.rect(screen,(000,128,000), square)
            available.append((thePiece.x-55,thePiece.y-55,thePiece,0,0))
            
        elif isSpotEmpty(piecesList,thePieceSquareX-2,thePieceSquareY-2) == True and getColor(piecesList,thePieceSquareX-1,thePieceSquareY-1) == 'white':
            square = pygame.Rect((thePiece.x-105,thePiece.y-105,CUBE_SIZE,CUBE_SIZE))
            pygame.draw.rect(screen,(000,128,000), square)
            available.append((thePiece.x-105,thePiece.y-105,thePiece,isSpotEmpty(piecesList,thePieceSquareX-1,thePieceSquareY-1)))

        if isSpotEmpty(piecesList,thePieceSquareX+1,thePieceSquareY-1) == True:
            square = pygame.Rect((thePiece.x+45,thePiece.y-55,CUBE_SIZE,CUBE_SIZE))
            pygame.draw.rect(screen,(000,128,000), square)
            available.append((thePiece.x+45,thePiece.y-55,thePiece,0,0))

        elif isSpotEmpty(piecesList,thePieceSquareX+2,thePieceSquareY-2) == True and getColor(piecesList,thePieceSquareX+1,thePieceSquareY-1) == 'white':
            square = pygame.Rect((thePiece.x+95,thePiece.y-105,CUBE_SIZE,CUBE_SIZE))
            pygame.draw.rect(screen,(000,128,000), square)
            available.append((thePiece.x+95,thePiece.y-105,thePiece,isSpotEmpty(piecesList,thePieceSquareX+1,thePieceSquareY-1)))   
            
        if thePiece.promoted == True:
            if isSpotEmpty(piecesList,thePieceSquareX-1,thePieceSquareY+1) == True:
                square = pygame.Rect((thePiece.x-55,thePiece.y+45,CUBE_SIZE,CUBE_SIZE))
                pygame.draw.rect(screen,(000,128,000), square)
                available.append((thePiece.x-55,thePiece.y+45,thePiece,0,0))
                
            elif isSpotEmpty(piecesList,thePieceSquareX-2,thePieceSquareY+2) == True and getColor(piecesList,thePieceSquareX-1,thePieceSquareY+1) == 'white':
                square = pygame.Rect((thePiece.x-105,thePiece.y+95,CUBE_SIZE,CUBE_SIZE))
                pygame.draw.rect(screen,(000,128,000), square)
                available.append((thePiece.x-105,thePiece.y+95,thePiece,isSpotEmpty(piecesList,thePieceSquareX-1,thePieceSquareY+1)))

            if isSpotEmpty(piecesList,thePieceSquareX+1,thePieceSquareY+1) == True:
                square = pygame.Rect((thePiece.x+45,thePiece.y+45,CUBE_SIZE,CUBE_SIZE))
                pygame.draw.rect(screen,(000,128,000), square)
                available.append((thePiece.x+45,thePiece.y+45,thePiece,0,0))

            elif isSpotEmpty(piecesList,thePieceSquareX+2,thePieceSquareY+2) == True and getColor(piecesList,thePieceSquareX+1,thePieceSquareY+1) == 'white':
                square = pygame.Rect((thePiece.x+95,thePiece.y+95,CUBE_SIZE,CUBE_SIZE))
                pygame.draw.rect(screen,(000,128,000), square)
                available.append((thePiece.x+95,thePiece.y+95,thePiece,isSpotEmpty(piecesList,thePieceSquareX+1,thePieceSquareY+1)))

    elif thePiece.color == 'white'and turn == 1:
        if isSpotEmpty(piecesList,thePieceSquareX-1,thePieceSquareY+1) == True:
            square = pygame.Rect((thePiece.x-55,thePiece.y+45,CUBE_SIZE,CUBE_SIZE))
            pygame.draw.rect(screen,(000,128,000), square)
            available.append((thePiece.x-55,thePiece.y+45,thePiece,0,0))

        elif isSpotEmpty(piecesList,thePieceSquareX-2,thePieceSquareY+2) == True and getColor(piecesList,thePieceSquareX-1,thePieceSquareY+1) == 'black':
            square = pygame.Rect((thePiece.x-105,thePiece.y+95,CUBE_SIZE,CUBE_SIZE))
            pygame.draw.rect(screen,(000,128,000), square)
            available.append((thePiece.x-105,thePiece.y+95,thePiece,isSpotEmpty(piecesList,thePieceSquareX-1,thePieceSquareY+1)))

        if isSpotEmpty(piecesList,thePieceSquareX+1,thePieceSquareY+1) == True:
            square = pygame.Rect((thePiece.x+45,thePiece.y+45,CUBE_SIZE,CUBE_SIZE))
            pygame.draw.rect(screen,(000,128,000), square)
            available.append((thePiece.x+45,thePiece.y+45,thePiece,0,0))

        elif isSpotEmpty(piecesList,thePieceSquareX+2,thePieceSquareY+2) == True and getColor(piecesList,thePieceSquareX+1,thePieceSquareY+1) == 'black':
            square = pygame.Rect((thePiece.x+95,thePiece.y+95,CUBE_SIZE,CUBE_SIZE))
            pygame.draw.rect(screen,(000,128,000), square)
            available.append((thePiece.x+95,thePiece.y+95,thePiece,isSpotEmpty(piecesList,thePieceSquareX+1,thePieceSquareY+1)))    
        if thePiece.promoted == True:
            if isSpotEmpty(piecesList,thePieceSquareX-1,thePieceSquareY-1) == True:
                square = pygame.Rect((thePiece.x-55,thePiece.y-55,CUBE_SIZE,CUBE_SIZE))
                pygame.draw.rect(screen,(000,128,000), square)
                available.append((thePiece.x-55,thePiece.y-55,thePiece,0,0))
                
            elif isSpotEmpty(piecesList,thePieceSquareX-2,thePieceSquareY-2) == True and getColor(piecesList,thePieceSquareX-1,thePieceSquareY-1) == 'black':
                square = pygame.Rect((thePiece.x-105,thePiece.y-105,CUBE_SIZE,CUBE_SIZE))
                pygame.draw.rect(screen,(000,128,000), square)
                available.append((thePiece.x-105,thePiece.y-105,thePiece,isSpotEmpty(piecesList,thePieceSquareX-1,thePieceSquareY-1)))

            if isSpotEmpty(piecesList,thePieceSquareX+1,thePieceSquareY-1) == True:
                square = pygame.Rect((thePiece.x+45,thePiece.y-55,CUBE_SIZE,CUBE_SIZE))
                pygame.draw.rect(screen,(000,128,000), square)
                available.append((thePiece.x+45,thePiece.y-55,thePiece,0,0))

            elif isSpotEmpty(piecesList,thePieceSquareX+2,thePieceSquareY-2) == True and getColor(piecesList,thePieceSquareX+1,thePieceSquareY-1) == 'black':
                square = pygame.Rect((thePiece.x+95,thePiece.y-105,CUBE_SIZE,CUBE_SIZE))
                pygame.draw.rect(screen,(000,128,000), square)
                available.append((thePiece.x+95,thePiece.y-105,thePiece,isSpotEmpty(piecesList,thePieceSquareX+1,thePieceSquareY-1)))    

    return available

def selectedPiece(pos,piecesList,turn):

    for piece in piecesList:
        if pygame.Rect(piece.x, piece.y, 40, 40).collidepoint(pos):
            for p in piecesList:
                if p is not piece:
                    p.image = promoBlack if (p.color=='black' and p.promoted) else \
                              blackPiece   if p.color=='black' else \
                              promoWhite  if (p.promoted) else \
                              whitePiece

            if piece.color == 'black':
                piece.image = selectedBlackPromo if piece.promoted else selectedBlack
            else:
                piece.image = selectedWhitePromo if piece.promoted else selectedWhite

            return availablePlaces(piece, piecesList, turn)

    return []
                
def checkGameOver(piecesList):
    white = 0
    black = 0 
    quit = False
    for piece in piecesList:
        if piece.color == 'white': 
            white += 1 
        else:
            black += 1
    if black == 0 or white == 0:
        while quit == False:
            screen.blit(background,(0,0))
            screen.blit(frameEnd,(100,100))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
                    quit = True

            pygame.display.update()        
        return True
    return False

def saveGame(piecesList,turn):
    
    with open('data.txt','w') as f:

        f.write(str(turn) + '\n')

        for piece in piecesList:
            f.write(str(piece.color) + '\n')
            f.write(str(piece.x) + '\n')
            f.write(str(piece.y) + '\n')
            f.write(str(piece.promoted) + '\n')

def loadGame():
    with open('data.txt','r')as f:
        turn = int(f.readline().strip())
        piecesList= []

        while True:
            color = f.readline().strip()
            if color == '':
                break
            x = int(f.readline().strip())
            y = int(f.readline().strip())
            promoted = f.readline().strip() == True

            if color == 'white':
                image = promoWhite if promoted == 'True' else whitePiece
            else:
                image = promoBlack if promoted == 'True' else blackPiece

            piece = pieces(x,y,color,image)         
            piece.promoted = promoted
            piecesList.append(piece)

    return startGame(piecesList,True,turn)


    x = (xd - BOARD_X) // CUBE_SIZE
    y = (yd - BOARD_Y) // CUBE_SIZE  

    availablePlaces = []

    for piece in piecesList:
        if piece.xInBoard == x and piece.yInBoard == y :
            break

    if piece != None:
        if piece.color == 'white':
            if isSpotEmpty(piecesList,piece.xInBoard + 1 ,piece.yInBoard + 1) == False and getColor(piecesList,piece.xInBoard + 1 ,piece.yInBoard + 1) == 'black' and isSpotEmpty(piecesList,piece.xInBoard + 2 ,piece.yInBoard + 2) == True:
                availablePlaces.append((piece.xInBoard + 2 ,piece.yInBoard + 2))
                square = pygame.Rect((xd+110,piece.y+110,CUBE_SIZE,CUBE_SIZE))
                pygame.draw.rect(screen,(000,128,000), square)
            if isSpotEmpty(piecesList,piece.xInBoard - 1 ,piece.yInBoard + 1) == False and getColor(piecesList,piece.xInBoard - 1 ,piece.yInBoard + 1) == 'black' and isSpotEmpty(piecesList,piece.xInBoard - 2 ,piece.yInBoard + 2) == True:
                availablePlaces.append((piece.xInBoard - 2 ,piece.yInBoard + 2))
                square = pygame.Rect((piece.x-110,piece.y+110,CUBE_SIZE,CUBE_SIZE))
                pygame.draw.rect(screen,(000,128,000), square)
            if piece.promoted == True:
                if isSpotEmpty(piecesList,piece.xInBoard + 1 ,piece.yInBoard - 1) == False and getColor(piecesList,piece.xInBoard + 1 ,piece.yInBoard - 1) == 'black' and isSpotEmpty(piecesList,piece.xInBoard + 2 ,piece.yInBoard - 2) == True:
                    availablePlaces.append((piece.xInBoard + 2 ,piece.yInBoard - 2))
                    square = pygame.Rect((piece.x+110,piece.y-110,CUBE_SIZE,CUBE_SIZE))
                    pygame.draw.rect(screen,(000,128,000), square)
                if isSpotEmpty(piecesList,piece.xInBoard - 1 ,piece.yInBoard - 1) == False and getColor(piecesList,piece.xInBoard - 1 ,piece.yInBoard - 1) == 'black' and isSpotEmpty(piecesList,piece.xInBoard - 2 ,piece.yInBoard - 2) == True:
                    availablePlaces.append((piece.xInBoard - 2 ,piece.yInBoard - 2))
                    square = pygame.Rect((piece.x-110,piece.y-110,CUBE_SIZE,CUBE_SIZE))
                    pygame.draw.rect(screen,(000,128,000), square)
        else:

            if isSpotEmpty(piecesList,piece.xInBoard + 1 ,piece.yInBoard - 1) == False and getColor(piecesList,piece.xInBoard + 1 ,piece.yInBoard - 1) == 'white' and isSpotEmpty(piecesList,piece.xInBoard + 2 ,piece.yInBoard - 2) == True:
                availablePlaces.append((piece.xInBoard + 2 ,piece.yInBoard - 2))
                square = pygame.Rect((piece.x+110,piece.y-110,CUBE_SIZE,CUBE_SIZE))
                pygame.draw.rect(screen,(000,128,000), square)
            if isSpotEmpty(piecesList,piece.xInBoard - 1 ,piece.yInBoard - 1) == False and getColor(piecesList,piece.xInBoard - 1 ,piece.yInBoard - 1) == 'white' and isSpotEmpty(piecesList,piece.xInBoard - 2 ,piece.yInBoard - 2) == True:
                availablePlaces.append((piece.xInBoard - 2 ,piece.yInBoard - 2))
                square = pygame.Rect((piece.x-110,piece.y-110,CUBE_SIZE,CUBE_SIZE))
                pygame.draw.rect(screen,(000,128,000), square)

            if piece.promoted == True:
                if isSpotEmpty(piecesList,piece.xInBoard + 1 ,piece.yInBoard + 1) == False and getColor(piecesList,piece.xInBoard + 1 ,piece.yInBoard + 1) == 'white' and isSpotEmpty(piecesList,piece.xInBoard + 2 ,piece.yInBoard + 2,piecesList) == True:
                    availablePlaces.append((piece.xInBoard + 2 ,piece.yInBoard + 2))
                    square = pygame.Rect((piece.x+110,piece.y+110,CUBE_SIZE,CUBE_SIZE))
                    pygame.draw.rect(screen,(000,128,000), square)
                if isSpotEmpty(piecesList,piece.xInBoard - 1 ,piece.yInBoard + 1) == False and getColor(piecesList,piece.xInBoard - 1 ,piece.yInBoard + 1) == 'white' and isSpotEmpty(piecesList,piece.xInBoard - 2 ,piece.yInBoard + 2,piecesList) == True:
                    availablePlaces.append((piece.xInBoard - 2 ,piece.yInBoard + 2))
                    square = pygame.Rect((piece.x-110,piece.y+110,CUBE_SIZE,CUBE_SIZE))
                    pygame.draw.rect(screen,(000,128,000), square)

    return availablePlaces

def canRecapture(xd, yd, piecesList):

    px = (xd - BOARD_X) // CUBE_SIZE
    py = (yd - BOARD_Y) // CUBE_SIZE

    thePiece = None
    for piece in piecesList:
        bx = (piece.x - BOARD_X) // CUBE_SIZE
        by = (piece.y - BOARD_Y) // CUBE_SIZE
        if bx == px and by == py:
            thePiece = piece
            break
    if not thePiece:
        return []

    available = []

    if thePiece.color == 'white':
        mid = isSpotEmpty(piecesList, px+1, py+1)
        if mid is not True and getColor(piecesList, px+1, py+1) == 'black' and isSpotEmpty(piecesList, px+2, py+2) == True:
            sx = BOARD_X + (px+2)*CUBE_SIZE + 5
            sy = BOARD_Y + (py+2)*CUBE_SIZE + 5
            pygame.draw.rect(screen, (0,128,0), (sx, sy, CUBE_SIZE, CUBE_SIZE))
            available.append((sx, sy, thePiece, mid))

        mid = isSpotEmpty(piecesList, px-1, py+1)
        if mid is not True and getColor(piecesList, px-1, py+1) == 'black' and isSpotEmpty(piecesList, px-2, py+2) == True:
            sx = BOARD_X + (px-2)*CUBE_SIZE + 5
            sy = BOARD_Y + (py+2)*CUBE_SIZE + 5
            pygame.draw.rect(screen, (0,128,0), (sx, sy, CUBE_SIZE, CUBE_SIZE))
            available.append((sx, sy, thePiece, mid))

        if thePiece.promoted:
            mid = isSpotEmpty(piecesList, px+1, py-1)
            if mid is not True and getColor(piecesList, px+1, py-1) == 'black' and isSpotEmpty(piecesList, px+2, py-2) == True:
                sx = BOARD_X + (px+2)*CUBE_SIZE + 5
                sy = BOARD_Y + (py-2)*CUBE_SIZE + 5
                pygame.draw.rect(screen, (0,128,0), (sx, sy, CUBE_SIZE, CUBE_SIZE))
                available.append((sx, sy, thePiece, mid))

            mid = isSpotEmpty(piecesList, px-1, py-1)
            if mid is not True and getColor(piecesList, px-1, py-1) == 'black' and isSpotEmpty(piecesList, px-2, py-2) == True:
                sx = BOARD_X + (px-2)*CUBE_SIZE + 5
                sy = BOARD_Y + (py-2)*CUBE_SIZE + 5
                pygame.draw.rect(screen, (0,128,0), (sx, sy, CUBE_SIZE, CUBE_SIZE))
                available.append((sx, sy, thePiece, mid))

    else:  
        
        mid = isSpotEmpty(piecesList, px+1, py-1)
        if mid is not True and getColor(piecesList, px+1, py-1) == 'white' and isSpotEmpty(piecesList, px+2, py-2) == True:
            sx = BOARD_X + (px+2)*CUBE_SIZE + 5
            sy = BOARD_Y + (py-2)*CUBE_SIZE + 5
            pygame.draw.rect(screen, (0,128,0), (sx, sy, CUBE_SIZE, CUBE_SIZE))
            available.append((sx, sy, thePiece, mid))

        mid = isSpotEmpty(piecesList, px-1, py-1)
        if mid is not True and getColor(piecesList, px-1, py-1) == 'white' and isSpotEmpty(piecesList, px-2, py-2) == True:
            sx = BOARD_X + (px-2)*CUBE_SIZE + 5
            sy = BOARD_Y + (py-2)*CUBE_SIZE + 5
            pygame.draw.rect(screen, (0,128,0), (sx, sy, CUBE_SIZE, CUBE_SIZE))
            available.append((sx, sy, thePiece, mid))

        if thePiece.promoted:
            mid = isSpotEmpty(piecesList, px+1, py+1)
            if mid is not True and getColor(piecesList, px+1, py+1) == 'white' and isSpotEmpty(piecesList, px+2, py+2) == True:
                sx = BOARD_X + (px+2)*CUBE_SIZE + 5
                sy = BOARD_Y + (py+2)*CUBE_SIZE + 5
                pygame.draw.rect(screen, (0,128,0), (sx, sy, CUBE_SIZE, CUBE_SIZE))
                available.append((sx, sy, thePiece, mid))

            mid = isSpotEmpty(piecesList, px-1, py+1)
            if mid is not True and getColor(piecesList, px-1, py+1) == 'white' and isSpotEmpty(piecesList, px-2, py+2) == True:
                sx = BOARD_X + (px-2)*CUBE_SIZE + 5
                sy = BOARD_Y + (py+2)*CUBE_SIZE + 5
                pygame.draw.rect(screen, (0,128,0), (sx, sy, CUBE_SIZE, CUBE_SIZE))
                available.append((sx, sy, thePiece, mid))

    return available

def startGame(piecesList,loaded,turn = 1):
    saveButton = pygame.Rect(700, 20, 200, 50)
    saveText = font.render("Save", True, (200,0,0))
    if loaded == False:   
        screen.blit(background, (0, 0))
        screen.blit(frame, (100, -30))
        
        piecesList = deployPieces(BOARD_X, BOARD_Y)
    game_end = False 
    availablePlaces = []
    selected_piece = None

    while not game_end:
        
        screen.blit(background, (0, 0))
        screen.blit(frame, (100, -30))
        screen.blit(saveText,(700,20))
        draw_board(BOARD_X, BOARD_Y)  
        
        for piece in piecesList:
            piece.draw(screen)
            
            pieceX = (piece.x - BOARD_X) // CUBE_SIZE
            pieceY = (piece.y - BOARD_Y) // CUBE_SIZE
            if piece.color == 'white':
                if pieceX in {0, 2, 4, 6} and pieceY == 7: 
                    piece.promoted = True
                    piece.image = promoWhite
            else:
                if pieceX in {1, 3, 5, 7} and pieceY == 0: 
                    piece.promoted = True
                    piece.image = promoBlack

        for place in availablePlaces:
            pygame.draw.rect(screen, (0, 128, 0), (place[0], place[1], CUBE_SIZE, CUBE_SIZE))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True   
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                moved = False
                
                if saveButton.collidepoint(pos):
                    saveGame(piecesList,turn)
                    return True

                for click in availablePlaces:
                    if pygame.Rect(click[0], click[1], CUBE_SIZE, CUBE_SIZE).collidepoint(pos):
                        if click[3]:  
                            piecesList.remove(click[3])
                        click[2].x = click[0] + 5
                        click[2].y = click[1] + 5
                        move_sound.play()
                        
                        extraMove = canRecapture(click[2].x,click[2].y,piecesList)
                        print(str(extraMove))
                        
                        if extraMove == []:
                            turn *= -1
                        moved = True
                        break
                
                availablePlaces = []
                
                if not moved:
                    availablePlaces = selectedPiece(pos, piecesList,turn) or []
                
        pygame.display.update()       
        clock.tick(60) 

        game_end = checkGameOver(piecesList)
    
    pygame.quit()

def menu():
    choose = False
    screen.blit(background, (0, 0))
    
    start_button = pygame.Rect(300, 250, 200, 50)
    quit_button = pygame.Rect(300, 400, 200, 50)
    loadButton = pygame.Rect(300, 325, 200, 50)

    while not choose:
        getIn = False
        screen.blit(background, (0, 0))
        screen.blit(menuFrame,(190,170))
        screen.blit(torch,(0,0))
        screen.blit(torch,(550,0))


        start_text = font.render("Start Game", True, (240,240,240))
        quit_text = font.render("Quit", True, (240,240,240))
        loadText = font.render("Load", True, (240,240,240))

        screen.blit(start_text, (start_button.x +20, start_button.y + 15))
        screen.blit(quit_text, (quit_button.x +60, quit_button.y ))
        screen.blit(loadText, (loadButton.x+60,loadButton.y))

        pos = pygame.mouse.get_pos()

        if start_button.collidepoint(pos):
            screen.blit(arrow, (start_button.x - 170, start_button.y-65))
        elif quit_button.collidepoint(pos):
            screen.blit(arrow, (quit_button.x - 170, quit_button.y-80))
        elif loadButton.collidepoint(pos):
            screen.blit(arrow, (loadButton.x - 170, loadButton.y-80))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choose = True
                pygame.quit()
                return
              
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_button.collidepoint(pos):
                    clickSound.play()
                    choose = startGame([],False)
                    getIn = True
                elif loadButton.collidepoint(pos):
                    clickSound.play()
                    loadGame()
                    choose= True
                    getIn = True    
                elif quit_button.collidepoint(pos):
                    clickSound.play()
                    choose = True
                    pygame.quit()
                    return
        if not getIn:
            pygame.display.update()
        clock.tick(60)           
                    
if __name__ == "__main__":
    """ try:
        con = getConnection()
        data = [('player_10',10),('player_11',11)]
        create(('zoro',0),con)
        load(data,con)
        read(con)
        if getByName('player_10',con):
            print('exist')
        else: 
            print('! exist')    
    except Exception as e:
        print(e) """
    menu()
                