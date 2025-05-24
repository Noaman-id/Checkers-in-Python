from mysql import connector
from dao import *
import pygame
 
pygame.init()
pygame.mixer.init()
move_sound = pygame.mixer.Sound("./assets/move-self.mp3")
clock = pygame.time.Clock()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BOARD_X = 200
BOARD_Y = 100
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

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

selectedWhitePromo = pygame.image.load("./assets/selectedWhite.png").convert_alpha()
selectedWhitePromo = pygame.transform.scale(selectedWhitePromo, (40, 40))

selectedBlackPromo = pygame.image.load("./assets/selectedBlack.png").convert_alpha()
selectedBlackPromo = pygame.transform.scale(selectedBlackPromo, (40, 40))

turn = 1

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
                    
            place_x += 50
            index = index * -1
        place_y += 50   
        place_x = boardX
        index = index * -1

def deployPieces(boardX,boardY):

    piecesList = []

    index = 1
    for row in range(3):
        for col in range(8):
            if index == -1:
                x = col * 50 + 5 + boardX
                y = row * 50 + 5 + boardY
                piecesList.append(pieces(x, y,'white', whitePiece))
            index *= -1    
        index *= -1    
    for row in range(5, 8):
        for col in range(8):
            if index == -1:
                x = col * 50 + 5 + boardX
                y = row * 50 + 5 + boardY
                piecesList.append(pieces(x, y,'black', blackPiece))
            index *= -1    
        index *= -1

    return piecesList    

def isSpotEmpty(piecesList,x,y):
    if x < 0 or y < 0 or x > 7 or y > 7:
        return False
    for piece in piecesList:
        piece_x = (piece.x - BOARD_X) // 50
        piece_y = (piece.y - BOARD_Y) // 50
        if piece_x == x and piece_y == y:
            return piece
    return True

def getColor(piecesList,x,y):
    if x < 0 or y < 0 or x > 7 or y > 7:
        return False
    for piece in piecesList:
        piece_x = (piece.x - BOARD_X) // 50
        piece_y = (piece.y - BOARD_Y) // 50
        if piece_x == x and piece_y == y:
            return piece.color

def availablePlaces(thePiece,piecesList):
    available = []
    thePieceSquareX = (thePiece.x - BOARD_X) // 50
    thePieceSquareY = (thePiece.y - BOARD_Y) // 50
    global turn
    if thePiece.color == 'black'and turn == -1:
        if isSpotEmpty(piecesList,thePieceSquareX-1,thePieceSquareY-1) == True:
            square = pygame.Rect((thePiece.x-55,thePiece.y-55,50,50))
            pygame.draw.rect(screen,(000,128,000), square)
            available.append((thePiece.x-55,thePiece.y-55,thePiece,0,0))
            
        elif isSpotEmpty(piecesList,thePieceSquareX-2,thePieceSquareY-2) == True and getColor(piecesList,thePieceSquareX-1,thePieceSquareY-1) == 'white':
            square = pygame.Rect((thePiece.x-105,thePiece.y-105,50,50))
            pygame.draw.rect(screen,(000,128,000), square)
            available.append((thePiece.x-105,thePiece.y-105,thePiece,isSpotEmpty(piecesList,thePieceSquareX-1,thePieceSquareY-1)))

        if isSpotEmpty(piecesList,thePieceSquareX+1,thePieceSquareY-1) == True:
            square = pygame.Rect((thePiece.x+45,thePiece.y-55,50,50))
            pygame.draw.rect(screen,(000,128,000), square)
            available.append((thePiece.x+45,thePiece.y-55,thePiece,0,0))

        elif isSpotEmpty(piecesList,thePieceSquareX+2,thePieceSquareY-2) == True and getColor(piecesList,thePieceSquareX+1,thePieceSquareY-1) == 'white':
            square = pygame.Rect((thePiece.x+95,thePiece.y-105,50,50))
            pygame.draw.rect(screen,(000,128,000), square)
            available.append((thePiece.x+95,thePiece.y-105,thePiece,isSpotEmpty(piecesList,thePieceSquareX+1,thePieceSquareY-1)))   
            
        if thePiece.promoted == True:
            if isSpotEmpty(piecesList,thePieceSquareX-1,thePieceSquareY+1) == True:
                square = pygame.Rect((thePiece.x-55,thePiece.y+45,50,50))
                pygame.draw.rect(screen,(000,128,000), square)
                available.append((thePiece.x-55,thePiece.y+45,thePiece,0,0))
                
            elif isSpotEmpty(piecesList,thePieceSquareX-2,thePieceSquareY+2) == True and getColor(piecesList,thePieceSquareX-1,thePieceSquareY+1) == 'white':
                square = pygame.Rect((thePiece.x-105,thePiece.y+95,50,50))
                pygame.draw.rect(screen,(000,128,000), square)
                available.append((thePiece.x-105,thePiece.y+95,thePiece,isSpotEmpty(piecesList,thePieceSquareX-1,thePieceSquareY+1)))

            if isSpotEmpty(piecesList,thePieceSquareX+1,thePieceSquareY+1) == True:
                square = pygame.Rect((thePiece.x+45,thePiece.y+45,50,50))
                pygame.draw.rect(screen,(000,128,000), square)
                available.append((thePiece.x+45,thePiece.y+45,thePiece,0,0))

            elif isSpotEmpty(piecesList,thePieceSquareX+2,thePieceSquareY+2) == True and getColor(piecesList,thePieceSquareX+1,thePieceSquareY+1) == 'white':
                square = pygame.Rect((thePiece.x+95,thePiece.y+95,50,50))
                pygame.draw.rect(screen,(000,128,000), square)
                available.append((thePiece.x+95,thePiece.y+95,thePiece,isSpotEmpty(piecesList,thePieceSquareX+1,thePieceSquareY+1)))

    elif thePiece.color == 'white'and turn == 1:
        if isSpotEmpty(piecesList,thePieceSquareX-1,thePieceSquareY+1) == True:
            square = pygame.Rect((thePiece.x-55,thePiece.y+45,50,50))
            pygame.draw.rect(screen,(000,128,000), square)
            available.append((thePiece.x-55,thePiece.y+45,thePiece,0,0))

        elif isSpotEmpty(piecesList,thePieceSquareX-2,thePieceSquareY+2) == True and getColor(piecesList,thePieceSquareX-1,thePieceSquareY+1) == 'black':
            square = pygame.Rect((thePiece.x-105,thePiece.y+95,50,50))
            pygame.draw.rect(screen,(000,128,000), square)
            available.append((thePiece.x-105,thePiece.y+95,thePiece,isSpotEmpty(piecesList,thePieceSquareX-1,thePieceSquareY+1)))

        if isSpotEmpty(piecesList,thePieceSquareX+1,thePieceSquareY+1) == True:
            square = pygame.Rect((thePiece.x+45,thePiece.y+45,50,50))
            pygame.draw.rect(screen,(000,128,000), square)
            available.append((thePiece.x+45,thePiece.y+45,thePiece,0,0))

        elif isSpotEmpty(piecesList,thePieceSquareX+2,thePieceSquareY+2) == True and getColor(piecesList,thePieceSquareX+1,thePieceSquareY+1) == 'black':
            square = pygame.Rect((thePiece.x+95,thePiece.y+95,50,50))
            pygame.draw.rect(screen,(000,128,000), square)
            available.append((thePiece.x+95,thePiece.y+95,thePiece,isSpotEmpty(piecesList,thePieceSquareX+1,thePieceSquareY+1)))    
        if thePiece.promoted == True:
            if isSpotEmpty(piecesList,thePieceSquareX-1,thePieceSquareY-1) == True:
                square = pygame.Rect((thePiece.x-55,thePiece.y-55,50,50))
                pygame.draw.rect(screen,(000,128,000), square)
                available.append((thePiece.x-55,thePiece.y-55,thePiece,0,0))
                
            elif isSpotEmpty(piecesList,thePieceSquareX-2,thePieceSquareY-2) == True and getColor(piecesList,thePieceSquareX-1,thePieceSquareY-1) == 'black':
                square = pygame.Rect((thePiece.x-105,thePiece.y-105,50,50))
                pygame.draw.rect(screen,(000,128,000), square)
                available.append((thePiece.x-105,thePiece.y-105,thePiece,isSpotEmpty(piecesList,thePieceSquareX-1,thePieceSquareY-1)))

            if isSpotEmpty(piecesList,thePieceSquareX+1,thePieceSquareY-1) == True:
                square = pygame.Rect((thePiece.x+45,thePiece.y-55,50,50))
                pygame.draw.rect(screen,(000,128,000), square)
                available.append((thePiece.x+45,thePiece.y-55,thePiece,0,0))

            elif isSpotEmpty(piecesList,thePieceSquareX+2,thePieceSquareY-2) == True and getColor(piecesList,thePieceSquareX+1,thePieceSquareY-1) == 'black':
                square = pygame.Rect((thePiece.x+95,thePiece.y-105,50,50))
                pygame.draw.rect(screen,(000,128,000), square)
                available.append((thePiece.x+95,thePiece.y-105,thePiece,isSpotEmpty(piecesList,thePieceSquareX+1,thePieceSquareY-1)))    

    return available

def selectedPiece(pos,piecesList):

    for piece in piecesList:
        piece_rect = pygame.Rect(piece.x,piece.y,40,40)
        if piece_rect.collidepoint(pos):
            if piece.color == 'black':
                if piece.promoted == False:
                    piece.image = selectedBlack
                else:
                    piece.image = selectedBlackPromo
            else:
                if piece.promoted == False:
                    piece.image = selectedWhite
                else:
                    piece.image = selectedWhitePromo
                    print('afaefae')
            return availablePlaces(piece,piecesList)
        else:
            if piece.color == 'black':
                piece.image = promoBlack if piece.promoted else blackPiece
            else:
                piece.image = promoWhite if piece.promoted else whitePiece

def startGame():
    game_end = False    
    
    draw_board(BOARD_X,BOARD_Y)
    piecesList= deployPieces(BOARD_X,BOARD_Y)
    
    availablePlaces = []
    while game_end == False:

        for piece in piecesList:
            piece.draw(screen)
            pieceX = (piece.x - BOARD_X) // 50
            pieceY = (piece.y - BOARD_Y) // 50
            if piece.color == 'white':
                if pieceX == 0 and pieceY == 7 or pieceX == 2 and pieceY == 7 or pieceX == 3 and pieceY == 7 or pieceX == 4 and pieceY == 7: 
                    piece.promoted = True
                    piece.image = promoWhite
            else:
                if pieceX == 1 and pieceY == 0 or pieceX == 3 and pieceY == 0 or pieceX == 5 and pieceY == 0 or pieceX == 7 and pieceY == 0: 
                    piece.promoted = True
                    piece.image = promoBlack
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_end = True   
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                draw_board(BOARD_X,BOARD_Y)
                moved = False
                if availablePlaces is not None:
                    for click in availablePlaces:
                        if pygame.Rect(click[0], click[1], 50, 50).collidepoint(pos):
                            if click[3] != True:
                                for deletePiece in piecesList:
                                    if click[3] == deletePiece:
                                        piecesList.remove(deletePiece)
                            click[2].x=click[0]+5
                            click[2].y=click[1]+5
                            move_sound.play()
                            global turn
                            turn = turn * -1
                            moved = True
                            break
                availablePlaces=[]

                for piece in piecesList:
                    if piece.color == 'black':
                        piece.image = promoBlack if piece.promoted else blackPiece
                    else:
                        piece.image = promoWhite if piece.promoted else whitePiece
                if moved == False:            
                    availablePlaces = selectedPiece(pos,piecesList)

        pygame.display.update()       
        clock.tick(60) 
    
    pygame.quit()

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
    startGame()
                