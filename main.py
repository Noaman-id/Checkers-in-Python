from mysql import connector
import os
from dao import *
import pygame
from PIL import Image as GIF

pygame.init()
pygame.mixer.init()
move_sound = pygame.mixer.Sound("./assets/move-self.mp3")
clickSound = pygame.mixer.Sound("./assets/clickSound.wav")
backNosie = pygame.mixer.Sound("./assets/backNoise.wav")
backNosie.set_volume(0.03)
typingClickSound = pygame.mixer.Sound("./assets/typingClick.mp3")
clock = pygame.time.Clock()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAME_WIDTH = 620
FRAME_HEIGHT = 513
BOARD_X = 115
BOARD_Y = 69
CUBE_SIZE= 50

from PIL import Image
import pygame

font = pygame.font.Font("assets/fonts/Alkhemikal.ttf", 36)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

torch = pygame.image.load("./assets/torch.png").convert_alpha()
torch = pygame.transform.scale(torch, (250, 200))

arrow = pygame.image.load("./assets/arrow.png").convert_alpha()
arrow = pygame.transform.scale(arrow, (30, 30))

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
frameEnd = pygame.transform.scale(frameEnd, (500, 350))

menuFrame = pygame.image.load("./assets/menuFrame.png").convert_alpha()
menuFrame = pygame.transform.scale(menuFrame, (300, 60))

leaderBoardFrame = pygame.transform.rotate(frameEnd, 90)
leaderBoardFrame = pygame.transform.scale(leaderBoardFrame, (400, 590))

volumeFrame = pygame.image.load("./assets/volumeFrame.png")
volumeFrame = pygame.transform.rotate(volumeFrame,180)
volumeFrame = pygame.transform.scale(volumeFrame, (100,55))

muteLbo9 = pygame.image.load("./assets/muteLbo9.png")
muteLbo9 = pygame.transform.scale(muteLbo9, (50, 27))

Lbo9 = pygame.image.load("./assets/Lbo9.png")
Lbo9 = pygame.transform.scale(Lbo9, (60, 30))

sideFrame = pygame.image.load("./assets/sideFrame.png")
sideFrame = pygame.transform.scale(sideFrame, (300, 60))

sideFrameExtra = pygame.transform.scale(sideFrame, (350, 60))
sideFrameRotated = pygame.transform.flip(sideFrame,True,False)

newCursor = pygame.image.load("./assets/newCursor.png")
newCursor = pygame.transform.scale(newCursor, (30, 30))

forceEat = pygame.image.load("./assets/forceEat.png")
forceEat = pygame.transform.scale(forceEat, (50, 50))

Header = pygame.image.load("./assets/Header.png")
Header = pygame.transform.scale(Header, (200, 50))

eatCursor = pygame.image.load("./assets/eatCursor.png")
eatCursor = pygame.transform.scale(eatCursor, (30, 30))

backButton = pygame.image.load("./assets/backButton.png")
backButton = pygame.transform.scale(backButton, (100, 50))

def getConnection():
    return connector.connect(
        user='root', 
        password='Noaman-2005',
        database='db_game',
        host='127.0.0.1',
        port=3306
    )

class pieces:
    def __init__(self,x,y,color,image,promoted=False):
        self.x= x
        self.y= y
        self.xInBoard = (x - BOARD_X) // CUBE_SIZE
        self.yInBoard = (y - BOARD_Y) // CUBE_SIZE
        self.color= color
        self.image= image
        self.promoted= promoted
        

    def draw(self,surface):
        surface.blit(self.image, (self.x,self.y))    

def draw_cursor(cursor_img):
    x, y = pygame.mouse.get_pos()
    screen.blit(cursor_img, (x-7, y-2))

def load_gif_frames(path, size):
    gif = GIF.open(path)
    frames = []
    try:
        while True:
            frame = gif.convert('RGBA')
            pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, 'RGBA')
            pygame_image = pygame.transform.scale(pygame_image, size)
            frames.append(pygame_image)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames

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

background_frames = load_gif_frames("./assets/background-purple.gif", (SCREEN_WIDTH, SCREEN_HEIGHT))
frame_index = 0
animation_timer = 0
animation_speed = 100

def getColor(piecesList,x,y):
    if x < 0 or y < 0 or x > 7 or y > 7:
        return False
    for piece in piecesList:
        piece_x = (piece.x - BOARD_X) // CUBE_SIZE
        piece_y = (piece.y - BOARD_Y) // CUBE_SIZE
        if piece_x == x and piece_y == y:
            return piece.color

def availablePlaces(thePiece,piecesList,turn,extraMove):
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
            
        if thePiece.promoted == True or extraMove != None:
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
        if thePiece.promoted == True or extraMove != None:
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

def selectedPiece(pos,piecesList,turn,extraMove):

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

            return availablePlaces(piece, piecesList, turn,extraMove)

    return []

def isPieceSelectedForEat(pos,turn,piecesList):
    for piece in piecesList:
        if pygame.Rect(piece.x, piece.y, 40, 40).collidepoint(pos):
            
            if turn == 1 and piece.color == 'black':
                return piece
            elif  turn == -1 and piece.color == 'white':
                return piece
    return None

def checkGameOver(piecesList,whitePlayer,blackPlayer):
    white = 0
    black = 0 
    quit = False
    for piece in piecesList:
        if piece.color == 'white': 
            white += 1 
        else:
            black += 1
    if black == 0 or white == 0:
        if black == 0:
            if whitePlayer != 'Guest1':
                try:
                    score = getByName(whitePlayer,con)[2]
                    update(whitePlayer,score+1,con)
                except Exception as e:
                    print(e)    
                    exit(0)
            winner = font.render('Congragulation sir',True,(0,0,0))   
            winnerAnnouce = font.render(f'{whitePlayer} you won',True,(0,0,0))
        
        if white == 0:
            if blackPlayer != 'Guest2': 
                try:   
                    score = getByName(blackPlayer,con)[2]
                    update(blackPlayer,score+1,con)
                except Exception as e:
                    print(e)
                    exit(0)
            winner = font.render('Congragulation sir',True,(0,0,0))
            winnerAnnouce = font.render(f'{whitePlayer} you won',True,(0,0,0))    
        while quit == False:
            draw_animated_background()
            draw_cursor(newCursor)
            screen.blit(frameEnd,(75,100))
            screen.blit(winner,(270,250))
            screen.blit(winnerAnnouce,(290,300))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
                    quit = True
            pygame.display.update()        
        return True
    return False

def saveGame(piecesList,turn,whitePlayer,blackPlayer):
    
    with open('data.txt','w') as f:

        f.write(str(turn) + '\n')
        f.write(whitePlayer + '\n')
        f.write(blackPlayer + '\n')


        for piece in piecesList:
            f.write(str(piece.color) + '\n')
            f.write(str(piece.x) + '\n')
            f.write(str(piece.y) + '\n')
            f.write(str(piece.promoted) + '\n')

def loadGame():
    with open('data.txt','r')as f:
        turn = int(f.readline().strip())
        whitePlayer = f.readline().strip()
        blackPlayer = f.readline().strip()
        piecesList= []

        while True:
            color = f.readline().strip()
            if color == '':
                break
            x = int(f.readline().strip())
            y = int(f.readline().strip())
            promoted = f.readline().strip() == "True"

            if color == 'white':
                image = promoWhite if promoted == 'True' else whitePiece
            else:
                image = promoBlack if promoted == 'True' else blackPiece

            piece = pieces(x,y,color,image)         
            piece.promoted = promoted
            piecesList.append(piece)

    return startGame(piecesList,True,turn,whitePlayer,blackPlayer)

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

def draw_animated_background():
    global frame_index, animation_timer
    current_time = pygame.time.get_ticks()
    if current_time - animation_timer > animation_speed:
        frame_index = (frame_index + 1) % len(background_frames)
        animation_timer = current_time
    screen.blit(background_frames[frame_index], (0, 0))

def canPieceBeAte(Eaten,piecesList,extra):
    EatenX = (Eaten.x - BOARD_X)// CUBE_SIZE
    EatenY = (Eaten.y - BOARD_Y)// CUBE_SIZE
    if Eaten.color == 'white':
        for piece in piecesList:
            piece_x = (piece.x - BOARD_X) // CUBE_SIZE
            piece_y = (piece.y - BOARD_Y) // CUBE_SIZE
            if piece.color != Eaten.color:
                if (piece_x == EatenX-1 and piece_y == EatenY+1 and isSpotEmpty(piecesList,EatenX+1,EatenY-1)):
                    return (piece,(EatenX+1,EatenY-1))
                elif (piece_x == EatenX+1 and piece_y == EatenY+1 and isSpotEmpty(piecesList,EatenX-1,EatenY-1)):
                    return (piece,(EatenX-1,EatenY-1))
                if extra != None or piece.promoted:
                    if (piece_x == EatenX+1 and piece_y == EatenY-1 and isSpotEmpty(piecesList,EatenX-1,EatenY+1)):
                        return (piece,(EatenX-1,EatenY+1))
                    elif (piece_x == EatenX-1 and piece_y == EatenY-1 and isSpotEmpty(piecesList,EatenX+1,EatenY+1)):
                        return (piece,(EatenX+1,EatenY+1))
    else :      
        for piece in piecesList:
            piece_x = (piece.x - BOARD_X) // CUBE_SIZE
            piece_y = (piece.y - BOARD_Y) // CUBE_SIZE
            if piece.color != Eaten.color:
                if (piece_x == EatenX+1 and piece_y == EatenY-1 and isSpotEmpty(piecesList,EatenX-1,EatenY+1)):
                    return (piece,(EatenX-1,EatenY+1))
                elif (piece_x == EatenX-1 and piece_y == EatenY-1 and isSpotEmpty(piecesList,EatenX+1,EatenY+1)):
                    return (piece,(EatenX+1,EatenY+1))
                if extra != None or piece.promoted:
                    if (piece_x == EatenX+1 and piece_y == EatenY-1 and isSpotEmpty(piecesList,EatenX-1,EatenY+1)): 
                        return (piece,(EatenX-1,EatenY+1))
                    elif (piece_x == EatenX-1 and piece_y == EatenY-1 and isSpotEmpty(piecesList,EatenX+1,EatenY+1)):
                        return (piece,(EatenX+1,EatenY+1))
    return None                       

def Nfakh(gameHistory, piecesList, extra=None):
    if len(gameHistory) < 2:
        return

    # Get the previous move (the one before the last)
    prev_move = gameHistory[-2]
    color = prev_move[0]
    promoted = prev_move[1]
    old_pos = prev_move[2]
    new_pos = prev_move[3]

    # 1. Roll back the board to before the last move
    temp_pieces = deployPieces(BOARD_X, BOARD_Y)
    for move in gameHistory[:-1]:
        for piece in temp_pieces:
            if (piece.x, piece.y) == move[2] and piece.color == move[0] and piece.promoted == move[1]:
                piece.x, piece.y = move[3]
                piece.promoted = move[1]
                if move[4]:  # If a capture happened
                    cap_x = (move[2][0] + move[3][0]) // 2
                    cap_y = (move[2][1] + move[3][1]) // 2
                    for p in temp_pieces:
                        if (p.x, p.y) == (cap_x, cap_y) and p.color != move[0]:
                            temp_pieces.remove(p)
                            break
                break

    # 2. Find the piece that moved in the previous move
    for piece in temp_pieces:
        if (piece.x, piece.y) == new_pos and piece.color == color and piece.promoted == promoted:
            # 3. Check if it had a forced capture at that state
            missed_eat = canPieceBeAte(piece, temp_pieces, extra)
            if missed_eat is not None:
                # 4. Remove the piece from the current board
                for real_piece in piecesList:
                    if (real_piece.x, real_piece.y) == new_pos and real_piece.color == color and real_piece.promoted == promoted:
                        piecesList.remove(real_piece)
                        return
            break

def reSummenDeadSoliders(gameHistory,piecesList):
    move = gameHistory[-1]
    if move[-1][0] == True:
        deadX = (move[2][0] + move[3][0]) // 2
        deadY = (move[2][1] + move[3][1]) // 2
        promoted = move[4][1]
        color = 'black' if move[0] == 'white' else 'white'
        
        if color == 'white':
            image = promoWhite if promoted else whitePiece
        else:
            image = promoBlack if promoted else blackPiece
        
        piecesList.append(pieces(deadX,deadY,color,image,promoted))
        
def startGame(piecesList,loaded,turn = 1,whitePlayer = 'Guest1',blackPlayer = 'Guest2'):
    gameHistory = []
    
    backNosie.stop()
    
    saveButton = pygame.Rect(700, 20, 200, 50)
    saveText = font.render("Save", True, (200,0,0))

    whiteText = font.render(whitePlayer, True, (240,240,240))
    blackText = font.render(blackPlayer, True, (240,240,240))

    forceButton = pygame.Rect(530,230,50,50)
    takeBackButton = pygame.Rect(590,230,100,50)

    try:
        if whitePlayer != 'Guest1': 
            score = getByName(whitePlayer,con)[2]
            whiteScore = 'Score : '+ str(score) 
            whiteScore = font.render(whiteScore,True, (240,240,240))
        
        if blackPlayer != 'Guest2':
            score = getByName(blackPlayer,con)[2]
            blackScore = 'Score : '+ str(score) 
            blackScore = font.render(blackScore,True,(240,240,240))
    except Exception as e:
        print(e)
    if loaded == False:   
        draw_animated_background()
        screen.blit(frame, (100, -30))
        
        piecesList = deployPieces(BOARD_X, BOARD_Y)
    game_end = False 
    availablePlaces = []
    selected_piece = None

    if whitePlayer != 'Guest1':
        screen.blit(whiteScore,(BOARD_X+420,BOARD_Y+65))
    if blackPlayer != 'Guest2':
        screen.blit(blackScore,(BOARD_X+420,BOARD_Y+300))
    
    extraMove = []
    quit = False
    Cursor = newCursor
    while not game_end:
        draw_animated_background()
        screen.blit(frame, (100, -30))
        screen.blit(saveText,(700,20))
        screen.blit(whiteText,(BOARD_X+420,BOARD_Y+20))
        screen.blit(blackText,(BOARD_X+420,BOARD_Y+345))

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
                quit = True
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                moved = False
                if Cursor == eatCursor and isPieceSelectedForEat(pos,turn,piecesList) != None:
                    Eaten = isPieceSelectedForEat(pos,turn,piecesList)
                    if canPieceBeAte(Eaten,piecesList,extraMove)!=None:
                        Eater,(X,Y) = canPieceBeAte(Eaten,piecesList,extraMove)
                        Eater.x=BOARD_X + X * CUBE_SIZE +5
                        Eater.y=BOARD_Y + Y * CUBE_SIZE +5
                        piecesList.remove(Eaten)
                        Cursor = newCursor
                        extraMove = canRecapture(Eater.x,Eater.y,piecesList)
                        if extraMove == []:
                            turn *= -1 
                if takeBackButton.collidepoint(pos):
                    clickSound.play()
                    if gameHistory != []:
                        for piece in piecesList:
                            if piece.x == gameHistory[len(gameHistory)-1][3][0] and piece.y == gameHistory[len(gameHistory)-1][3][1]:
                                piecesList.remove(piece)
                                color = gameHistory[-1][0]
                                promoted = gameHistory[-1][4][1]
                                x = gameHistory[len(gameHistory)-1][2][0]
                                y = gameHistory[len(gameHistory)-1][2][1]
                                if color == 'white'and not promoted:
                                    piecesList.append(pieces(x,y,color,whitePiece,promoted))
                                elif color == 'white'and promoted:
                                    piecesList.append(pieces(x,y,color,promoWhite,promoted))
                                elif color == 'black' and promoted:
                                    piecesList.append(pieces(x,y,color,promoBlack,promoted))
                                else:
                                    piecesList.append(pieces(x,y,color,blackPiece,promoted))
                        reSummenDeadSoliders(gameHistory,piecesList)
                        gameHistory.pop()
                        turn *= -1

                if saveButton.collidepoint(pos):
                    saveGame(piecesList,turn,whitePlayer,blackPlayer)
                    return True

                if forceButton.collidepoint(pos):
                    clickSound.play()
                    if Cursor == newCursor:
                        Cursor = eatCursor
                    else:
                        Cursor = newCursor
                        
                for click in availablePlaces:
                    if pygame.Rect(click[0], click[1], CUBE_SIZE, CUBE_SIZE).collidepoint(pos):
                        #Nfakh(gameHistory,piecesList,extraMove)
                        lastMoveCap = False
                        wasPromo = False
                        if click[3]:  
                            wasPromo = click[3].promoted
                            piecesList.remove(click[3])
                            lastMoveCap=True

                        initX = click[2].x
                        initY = click[2].y
                        click[2].x = click[0] + 5
                        click[2].y = click[1] + 5
                        move_sound.play()
                        extraMove = []

                        if lastMoveCap == True:     
                            gameHistory.append((click[2].color,click[2].promoted,(initX,initY),(click[2].x,click[2].y),(True,wasPromo)))                     
                            extraMove = canRecapture(click[2].x,click[2].y,piecesList)
                        else:    
                            gameHistory.append((click[2].color,click[2].promoted,(initX,initY),(click[2].x,click[2].y),(False,wasPromo)))    
                        if extraMove == []:
                            turn *= -1
                            extraMove = None
                        moved = True
                        break
                
                availablePlaces = []
                
                if not moved:
                    availablePlaces = selectedPiece(pos, piecesList,turn,extraMove) or []
                
        screen.blit(forceEat,(530,230)) 
        screen.blit(backButton,(590,230))           
        draw_cursor(Cursor)        
        pygame.display.update()       
        clock.tick(60) 

        game_end = checkGameOver(piecesList,whitePlayer,blackPlayer)
        if quit == True:
            pygame.quit()

def checkPlayers(whitePlayer,blackPlayer):
    running = True
    try:
        if whitePlayer != 'Guest1':
            if getByName(whitePlayer,con):
                print(f'Welcom back sir {whitePlayer}')
            else: 
                create((whitePlayer,0),con)
        if blackPlayer != 'Guest2' :
            if getByName(blackPlayer,con):
                print(f'Welcom back sir {blackPlayer}')
            else: 
                create((blackPlayer,0),con)       
    except Exception as e:
        print(e)
        exit(0)   
    return

def provideName():

    running = True
    box2 = pygame.Rect(250,320,200,40)
    box1 = pygame.Rect(250,230,200,40)
    color_inactive = pygame.Color('white')
    color_active = pygame.Color('black')
    color1 = color_inactive
    color2 = color_inactive
    text_Box1=''
    text_Box2=''
    active1 = False
    active2 = False

    Player2 = font.render("Guest2:", True, (240,240,240))
    Player1 = font.render("Guest1:", True, (240,240,240))

    while running:
        draw_animated_background()
        screen.blit(frameEnd,(150,120))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if box1.collidepoint(event.pos):
                    color1 = color_active
                    color2 = color_inactive
                    active1 = True
                    active2 = False
                elif box2.collidepoint(event.pos):
                    color2 = color_active
                    color1 = color_inactive
                    active1 = False
                    active2 = True
                else:
                    color1 = color_inactive
                    color2 = color_inactive
                    active1 = False
                    active2 = False

            elif event.type == pygame.KEYDOWN:
                typingClickSound.play()
                if active1:
                    if event.key == pygame.K_BACKSPACE:
                        text_Box1 = text_Box1[:-1]
                    else:
                        text_Box1 += event.unicode
                elif active2:
                    if event.key == pygame.K_BACKSPACE:
                        text_Box2 = text_Box2[:-1]
                    else:
                        text_Box2 += event.unicode   
                if event.key == pygame.K_RETURN:
                    if whitePlayer == '':
                        whitePlayer = 'Guest1'
                    if blackPlayer == '':
                        blackPlayer = 'Guest2'
                    
                    checkPlayers(whitePlayer,blackPlayer)
                    startGame([],False,1,whitePlayer,blackPlayer)
                    return
        txt_surface1 = font.render(text_Box1, True, 'black')
        txt_surface2 = font.render(text_Box2, True, 'black')
        box1.w = 300
        box2.w = 300

        whitePlayer = text_Box1
        blackPlayer = text_Box2

        screen.blit(txt_surface1, (box1.x+10, box1.y))
        screen.blit(txt_surface2, (box2.x+10, box2.y))

        pygame.draw.rect(screen, color1,box1, 2)
        pygame.draw.rect(screen, color2,box2, 2)

        screen.blit(Player1,(box1.x,box1.y-35))
        screen.blit(Player2,(box2.x,box2.y-35))
        draw_cursor(newCursor)
        pygame.display.update()
        clock.tick(30)

def deletePlayer():
    running = True
    box1 = pygame.Rect(250,280,200,40)
    color_inactive = pygame.Color('white')
    color_active = pygame.Color('black')
    color1 = color_inactive
    text_Box1=''
    active1 = False

    Dtxt = font.render("Name to be deleted:", True, (240,240,240))

    while running:
        draw_animated_background()
        screen.blit(frameEnd,(150,150))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if box1.collidepoint(event.pos):
                    color1 = color_active
                    active1 = True
                else:
                    color1 = color_inactive
                    active1 = False

            elif event.type == pygame.KEYDOWN:
                typingClickSound.play()
                if active1:
                    if event.key == pygame.K_BACKSPACE:
                        text_Box1 = text_Box1[:-1]
                    else:
                        text_Box1 += event.unicode 
                if event.key == pygame.K_RETURN:
                    try:
                        if getByName(deletedPlayer,con):
                            delete(deletedPlayer,con)
                            print('deleted succesfuly !!')
                        else:
                            print("not found!!")    
                    except Exception as e:
                        print(e)
                        exit(0)    
                    return
        txt_surface1 = font.render(text_Box1, True, 'black')

        box1.w = 300

        deletedPlayer = text_Box1

        screen.blit(txt_surface1, (box1.x+10, box1.y))

        pygame.draw.rect(screen, color1,box1, 2)

        screen.blit(Dtxt,(box1.x,box1.y-40))

        draw_cursor(newCursor)
        pygame.display.update()
        clock.tick(30)

def loadData(data):
    finalList=[]
    name=''
    for letter in range(len(data)):
        if data[letter] == ',':
            try:
                if getByName(name,con):
                    pass
                else:
                    finalList.append((name,0))
            except Exception as e:
                print(e)
                exit(0)
            name = ''
        else:
            name += data[letter]
    try:        
        if getByName(name,con):
            pass
        else:        
            finalList.append((name,0))
        load(finalList,con)            
    except Exception as e:
        print(e)
        exit(0)
    return

def loadList():
    running = True
    input_box = pygame.Rect(10, 270, 500, 50)
    color_inactive = pygame.Color('white')
    color_active = pygame.Color('black')
    color = color_inactive
    active = False
    user_input = ''

    Txt = font.render("List of names (seperator is ','):", True, (240,240,240))

    while running:
        draw_animated_background()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                    color = color_active
                else:
                    active = False
                    color = color_inactive

            elif event.type == pygame.KEYDOWN:
                typingClickSound.play()
                if event.key == pygame.K_RETURN:
                    if data != '': 
                        loadData(data)
                    return
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    else:
                        user_input += event.unicode

        data = user_input

        txt_surface = font.render(user_input, True, 'white')
        input_box.w = 780
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))
        pygame.draw.rect(screen, color, input_box, 2)

        screen.blit(Txt,(input_box.x,input_box.y-40))

        draw_cursor(newCursor)
        pygame.display.update()
        clock.tick(30)

def leaderBoardList():
    running = True

    try:
        data = read(con)
    except Exception as e:
        print(e)
        exit(0)    

    data.sort(key=lambda x: x[2], reverse=True)

    while running:
        draw_animated_background()
        screen.blit(leaderBoardFrame,(200,10))

        title = font.render("Leaderboard", True, (255, 0, 0))
        screen.blit(title, (300, 60))

        y = 110
        i = 1
        for (id, name, score) in data[:10]:
            text = font.render(f"{i}. {name}-{score}", True, (0, 0, 0))
            screen.blit(text, (290, y))
            y += 40
            i += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
            
        draw_cursor(newCursor)
        pygame.display.update()

def menu():
    choose = False
    draw_animated_background()
    backNosie.play()
    start_button = pygame.Rect(245, 247, 300, 60)
    quit_button = pygame.Rect(245, 360, 300, 60)
    loadButton = pygame.Rect(245, 305, 300, 60)
    deleteButton = pygame.Rect(400,41, 300, 50)
    loadbutton = pygame.Rect(100,40, 300, 50)
    leaderBoard = pygame.Rect(210,530, 400, 50)
    volumeButton = pygame.Rect(SCREEN_WIDTH-90,45,100,50)

    theVolumeIcon = Lbo9

    while not choose:
        getIn = False
        draw_animated_background()

        start_text = font.render("Start Game", True, (240,240,240))
        quit_text = font.render("Quit", True, (240,240,240))
        loadText = font.render("Load", True, (240,240,240))
        deleteTxt = font.render("Delete", True, (200,200,200))
        loadTxt = font.render("load", True, (200,200,200))
        leaderTxt = font.render("Leader Board", True, (200,200,200))

        screen.blit(menuFrame,(start_button.x,start_button.y))
        screen.blit(menuFrame,(loadButton.x,loadButton.y))
        screen.blit(menuFrame,(quit_button.x,quit_button.y))
        screen.blit(volumeFrame,(volumeButton.x,volumeButton.y))
        screen.blit(sideFrameExtra, (leaderBoard.x,leaderBoard.y))
        screen.blit(sideFrameRotated, (deleteButton.x,deleteButton.y))
        screen.blit(sideFrame, (loadbutton.x,loadbutton.y))


        screen.blit(start_text, (320, start_button.y+13))
        screen.blit(quit_text, (360, quit_button.y+13))
        screen.blit(loadText, (360, loadButton.y+13))
        screen.blit(deleteTxt, (510,50))
        screen.blit(loadTxt, (220,50))
        screen.blit(leaderTxt, (295,540))
        if theVolumeIcon == muteLbo9 :
            screen.blit(theVolumeIcon, (SCREEN_WIDTH-61,60))
        else:
            screen.blit(theVolumeIcon, (SCREEN_WIDTH-70,57))

        pos = pygame.mouse.get_pos()

        if start_button.collidepoint(pos):
            screen.blit(arrow, (start_button.x - 35, start_button.y+15))
        elif quit_button.collidepoint(pos):
            screen.blit(arrow, (quit_button.x - 35, quit_button.y+15))
        elif loadButton.collidepoint(pos):
            screen.blit(arrow, (loadButton.x - 35, loadButton.y+15))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choose = True
                pygame.quit()
                return
              
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_button.collidepoint(pos):
                    clickSound.play()
                    provideName()
                    theVolumeIcon = Lbo9
                    backNosie.play()
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
                    exit(0)
                elif deleteButton.collidepoint(pos):
                    clickSound.play()
                    deletePlayer()
                elif loadbutton.collidepoint(pos):
                    clickSound.play()
                    loadList()   
                elif leaderBoard.collidepoint(pos):
                    clickSound.play()
                    leaderBoardList()
                elif volumeButton.collidepoint(pos):
                    clickSound.play()
                    if theVolumeIcon == muteLbo9:
                        backNosie.play()
                        theVolumeIcon = Lbo9         
                    else:
                        backNosie.stop()
                        theVolumeIcon = muteLbo9
        if not getIn:
            draw_cursor(newCursor)
            pygame.display.update()
        clock.tick(60)           

con = getConnection()

if __name__ == "__main__":
    pygame.mouse.set_visible(False)
    menu()
    