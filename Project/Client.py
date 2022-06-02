from calendar import c
import pygame
from network import Network
import random
import medium_mode_DandF as speech
import camera
import IMU_main
import camera
import game
from tutorial import tutorial
from pydub import AudioSegment
from pydub.playback import play
# from board import drawBoard


## Pygame Inits
pygame.font.init()
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.mixer.music.load("Archive/skating.wav")
pygame.mixer.music.set_volume(0.7)

FPS = 60

WIDTH, HEIGHT = 1400, 800
#number of squares per edge of game board
BOARD_EDGE = 5
#size of game board
BOARD_EDGE_SIZE = 500
#size of each square in the game board
SQUARE_EDGE = BOARD_EDGE_SIZE/BOARD_EDGE
TEXT_HEIGHT = (HEIGHT - BOARD_EDGE_SIZE)* 3/4 + BOARD_EDGE_SIZE

DIE_LENGTH = 150

SQUARE_WIDTH = WIDTH//7
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")
MODES = ['Keyboard', 'Camera', 'Speech', 'IMU']
SOUNDS = ['Notes/A3.wav', 'Notes/B3.wav', 'Notes/C4.wav', 'Notes/D4.wav', 'Notes/E4.wav', 'Notes/F4.wav', 'Notes/G4.wav']
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

red=pygame.image.load("Archive/red.jpg")
yellow=pygame.image.load("Archive/yellow.jpg")
blue=pygame.image.load("Archive/blue.jpg")
p1=pygame.image.load("Archive/p1.png")
p2=pygame.image.load("Archive/p2.png")
back=pygame.image.load("Archive/back.jpg")
D1=pygame.image.load("Archive/Dice1.jpg")
D2=pygame.image.load("Archive/Dice2.jpg")
D3=pygame.image.load("Archive/Dice3.jpg")
D4=pygame.image.load("Archive/Dice4.jpg")
D5=pygame.image.load("Archive/Dice5.jpg")
D6=pygame.image.load("Archive/Dice6.jpg")

#adjust images to correct size
red=pygame.transform.scale(red, (SQUARE_EDGE, SQUARE_EDGE))
yellow=pygame.transform.scale(yellow, (SQUARE_EDGE, SQUARE_EDGE))
blue=pygame.transform.scale(blue, (SQUARE_EDGE, SQUARE_EDGE))
p1=pygame.transform.scale(p1, (SQUARE_EDGE//2, SQUARE_EDGE//2))
p2=pygame.transform.scale(p2, (SQUARE_EDGE//2, SQUARE_EDGE//2))
back=pygame.transform.scale(back, (WIDTH, HEIGHT))
D1=pygame.transform.scale(D1, (DIE_LENGTH,DIE_LENGTH))
D2=pygame.transform.scale(D2, (DIE_LENGTH,DIE_LENGTH))
D3=pygame.transform.scale(D3, (DIE_LENGTH,DIE_LENGTH))
D4=pygame.transform.scale(D4, (DIE_LENGTH,DIE_LENGTH))
D5=pygame.transform.scale(D5, (DIE_LENGTH,DIE_LENGTH))
D6=pygame.transform.scale(D6, (DIE_LENGTH,DIE_LENGTH))

DICE = {1:D1, 2:D2, 3:D3, 4:D4, 5:D5, 6:D6}
ROLLED = False ## Client variable to make sure dice roll is only sent once

SQUARE_WIDTH = WIDTH//7
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")
MODES = ['Keyboard', 'Camera', 'Speech', 'IMU']
SOUNDS = ['Notes/A3.wav', 'Notes/B3.wav', 'Notes/C4.wav', 'Notes/D4.wav', 'Notes/E4.wav', 'Notes/F4.wav', 'Notes/G4.wav']
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

red=pygame.image.load("Archive/red.jpg")
yellow=pygame.image.load("Archive/yellow.jpg")
blue=pygame.image.load("Archive/blue.jpg")
checkered=pygame.image.load("Archive/checkered.png")
p1=pygame.image.load("Archive/p1.png")
p2=pygame.image.load("Archive/p2.png")
back=pygame.image.load("Archive/back.jpg")
D1=pygame.image.load("Archive/Dice1.jpg")
D2=pygame.image.load("Archive/Dice2.jpg")
D3=pygame.image.load("Archive/Dice3.jpg")
D4=pygame.image.load("Archive/Dice4.jpg")
D5=pygame.image.load("Archive/Dice5.jpg")
D6=pygame.image.load("Archive/Dice6.jpg")

#adjust images to correct size
red=pygame.transform.scale(red, (SQUARE_EDGE, SQUARE_EDGE))
yellow=pygame.transform.scale(yellow, (SQUARE_EDGE, SQUARE_EDGE))
blue=pygame.transform.scale(blue, (SQUARE_EDGE, SQUARE_EDGE))
checkered=pygame.transform.scale(checkered, (SQUARE_EDGE, SQUARE_EDGE))
p1=pygame.transform.scale(p1, (SQUARE_EDGE//2, SQUARE_EDGE//2))
p2=pygame.transform.scale(p2, (SQUARE_EDGE//2, SQUARE_EDGE//2))
legendBlue=pygame.transform.scale(blue, (SQUARE_EDGE//2, SQUARE_EDGE//2))
legendYellow=pygame.transform.scale(yellow, (SQUARE_EDGE//2, SQUARE_EDGE//2))
legendRed=pygame.transform.scale(red, (SQUARE_EDGE//2, SQUARE_EDGE//2))
back=pygame.transform.scale(back, (WIDTH, HEIGHT))
D1=pygame.transform.scale(D1, (DIE_LENGTH,DIE_LENGTH))
D2=pygame.transform.scale(D2, (DIE_LENGTH,DIE_LENGTH))
D3=pygame.transform.scale(D3, (DIE_LENGTH,DIE_LENGTH))
D4=pygame.transform.scale(D4, (DIE_LENGTH,DIE_LENGTH))
D5=pygame.transform.scale(D5, (DIE_LENGTH,DIE_LENGTH))
D6=pygame.transform.scale(D6, (DIE_LENGTH,DIE_LENGTH))

DICE = {1:D1, 2:D2, 3:D3, 4:D4, 5:D5, 6:D6}

def playGame(game, WIN):
        if game.currMode == 'Keyboard':
            game.currAnswer = input('^, >, v')
        elif game.currMode == 'IMU':
            game.currAnswer = IMU_main.main(WIN, game.currRoll)
        elif game.currMode == 'Camera':
            game.currAnswer = camera.camera(WIN, game.currRoll, 7)
        elif game.currMode == 'Speech':
            game.currAnswer = speech.speechRecognition(WIN)
        return(game.currAnswer)

def drawWindow(WIN, game):

    WIN.fill((0,0,0))
    font = pygame.font.SysFont('comicsansms', 64)
    text = font.render("Waiting for Player...", True, (255,255,255))
    WIN.blit(text, text.get_rect(center = (WIDTH/2, HEIGHT/2)))
    pygame.display.update()

def drawLegend():
    font = pygame.font.SysFont('comicsansms', 24)
    WIN.blit(p1, (0,0))
    WIN.blit(p2, (0, SQUARE_EDGE//2))
    WIN.blit(legendRed, (0, 2*SQUARE_EDGE//2))
    WIN.blit(legendYellow, (0, 3*SQUARE_EDGE//2))
    WIN.blit(legendBlue, (0, 4*SQUARE_EDGE//2))
    text1 = font.render("Player 1", True, (255,255,255))
    text2 = font.render("Player 2", True, (255,255,255))
    IMUtext = font.render("IMU", True, (255,255,255))
    cameratext = font.render("Camera", True, (255,255,255))
    speechtext = font.render("Speech", True, (255,255,255))
    WIN.blit(text1, (SQUARE_EDGE//2 + 10, 0))
    WIN.blit(text2, (SQUARE_EDGE//2 + 10, SQUARE_EDGE//2))
    WIN.blit(cameratext, (SQUARE_EDGE//2 + 10, 2*SQUARE_EDGE//2))
    WIN.blit(speechtext, (SQUARE_EDGE//2 + 10, 3*SQUARE_EDGE//2))
    WIN.blit(IMUtext, (SQUARE_EDGE//2 + 10, 4*SQUARE_EDGE//2))

def drawBoard(WIN, game, turn = False):
    WIN.fill((0,0,0))
    WIN.blit(back,(0,0))
    font = pygame.font.SysFont('comicsansms', 64)
    drawLegend()
    drawBoardGrid(game)
    if turn:
        txt = font.render('Click to roll the die!', True, (255,255,255))    
    else:
        txt = font.render("Other player's turn", True, (255,255,255))
    txtRect = txt.get_rect(center = (WIDTH/2, TEXT_HEIGHT))
    WIN.blit(txt, txtRect)
    pygame.display.update()

def drawBoardGrid(game, players = 2, moving = False, r = 0, c = 0):
    board_height_start = 550
    board_width_start = (WIDTH - BOARD_EDGE_SIZE)/2

    font = pygame.font.SysFont('comicsansms', 24)
    txt = font.render("Other player's turn", True, (255,255,255))

    for i in range(game.boardH):
        #if i%2 == 0:
        board_width_start = (WIDTH - BOARD_EDGE_SIZE)/2
        # else:
        #     board_width_start = (WIDTH - BOARD_EDGE_SIZE)/2 + SQUARE_EDGE*game.boardW
        for j in range(game.boardW):
            if game.board[i][j] == 1:
                WIN.blit(red,(board_width_start,board_height_start))
            elif game.board[i][j] == 2:
                WIN.blit(yellow,(board_width_start,board_height_start))
            elif game.board[i][j] == 3:
                WIN.blit(blue,(board_width_start,board_height_start))
            else:
                print("ERROR: Board numbers are wrong")
            if i == game.boardH-1 and j == game.boardW-1:
                WIN.blit(checkered, (board_width_start,board_height_start))
            #if i%2 == 0:
            board_width_start += SQUARE_EDGE
            # else:
            #     board_width_start -= SQUARE_EDGE
        board_height_start -= SQUARE_EDGE

    #for i in range(game.numPlayers):
    r1 = BOARD_EDGE - game.spots[0]//BOARD_EDGE
    if ((game.spots[0]//BOARD_EDGE)%2) == 0:
        c1 = game.spots[0]%BOARD_EDGE
    else:
        c1 = BOARD_EDGE - game.spots[0]%BOARD_EDGE - 1
    r2 = BOARD_EDGE - game.spots[1] // BOARD_EDGE
    if ((game.spots[1]//BOARD_EDGE)%2) == 0:
        c2 = game.spots[1]%BOARD_EDGE
    else:
        c2 = BOARD_EDGE - game.spots[1]%BOARD_EDGE - 1

    if moving:
        if game.currPlayer == 0:
            r1 = r
            c1 = c
        else:
            r2 = r
            c2 = c

    w1 = 450
    #(WIDTH - BOARD_EDGE_SIZE)/2 - 2*SQUARE_EDGE
    h1 = 75
    WIN.blit(p1,(w1 + (c1)*SQUARE_EDGE, h1 + r1*SQUARE_EDGE))
    if players > 1:
        WIN.blit(p2,(w1 + (c2)*SQUARE_EDGE+50,h1 + r2*SQUARE_EDGE))

def moving():
    spot = game.oldSpot
    inc = SQUARE_EDGE//20
    if (spot//BOARD_EDGE == BOARD_EDGE and (spot%BOARD_EDGE)%2 == 0) or (spot//BOARD_EDGE == 0 and (spot%BOARD_EDGE)%2 == 1):
        dir = "up"
    elif (spot%BOARD_EDGE)%2 == 0:
        dir = "right"
    else:
        dir = "left"

    r = BOARD_EDGE - spot//BOARD_EDGE
    c = BOARD_EDGE - spot%BOARD_EDGE
    while spot < game.spots[0]:
        for i in range(20):
            if dir == "up":
                r += inc
            elif dir == "right":
                c += inc
            else:
                c -= inc
            drawBoardGrid(game, 2, True, r, c)
        spot += 1
            





def drawDiceRoll(WIN, roll):
    diceRect = D1.get_rect(center = (WIDTH/2, TEXT_HEIGHT))
    pygame.mixer.music.pause()
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('Archive/dice.wav'))
    for i in range(50):
        pygame.time.delay(60)
        WIN.fill((0,0,0))
        WIN.blit(back, (0,0))
        num = random.randint(1,6)
        WIN.blit(DICE[num], diceRect)
        pygame.display.update()

    WIN.fill((0,0,0))
    WIN.blit(back, (0,0))
    WIN.blit(DICE[roll], diceRect)
    pygame.display.update()
    pygame.time.delay(3000)
    pygame.mixer.music.unpause()

def drawMove(WIN, game):
    WIN.fill((0,0,0))
    WIN.blit(back, (0,0))
    font = pygame.font.SysFont('comicsansms', 64)
    txt = font.render('Correct!' , True, (255,255,255))
    txtRect = txt.get_rect(center = (WIDTH/2, TEXT_HEIGHT))
    WIN.blit(txt, txtRect)
    pygame.display.update()
    pygame.time.delay(4000)
    ## TO DO: make animation for player movement on board
    #moving()

def drawTurn(WIN):
    WIN.fill((0,0,0))
    font = pygame.font.SysFont('comicsansms', 64)
    txt = font.render("Other player's move" , True, (255,255,255))
    txtRect = txt.get_rect(center = (WIDTH/2, TEXT_HEIGHT))
    WIN.blit(txt, txtRect)
    pygame.display.update()

def drawEnd(WIN, game):
    WIN.fill((0,0,0))
    WIN.blit(back, (0,0))
    font = pygame.font.SysFont('comicsansms', 64)
    txt = font.render("Player " + str(game.winner + 1) + " wins!" , True, (255,255,255))
    txtRect = txt.get_rect(center = (WIDTH/2, TEXT_HEIGHT))
    WIN.blit(txt, txtRect)
    pygame.mixer.Channel(1).play(pygame.mixer.Sound('Archive/winner.wav'))
    pygame.display.update()
    pygame.time.delay(6000)

def drawSound(WIN, note):
    WIN.fill((0,0,0))
    font = pygame.font.SysFont('Arial', 64)
    for i in range(7):
        if i == note:
            pygame.draw.rect(WIN, (255, 0, 0), pygame.Rect(i*SQUARE_WIDTH, HEIGHT//2-(SQUARE_WIDTH//2), SQUARE_WIDTH, SQUARE_WIDTH), 3)
        else:
            pygame.draw.rect(WIN, (0, 255, 0), pygame.Rect(i*SQUARE_WIDTH, HEIGHT//2-(SQUARE_WIDTH//2), SQUARE_WIDTH, SQUARE_WIDTH), 3)
        txt = font.render(LETTERS[i], True, (255,255,255))
        txtRect = txt.get_rect(center = (i*SQUARE_WIDTH + SQUARE_WIDTH//2, HEIGHT//2))
        WIN.blit(txt, txtRect)
    pygame.display.update()

def checkQuit():
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

def playSound(WIN,game):
    for i in range(game.currRoll):
        checkQuit()
        drawSound(WIN, game.melody[i])
        sound = AudioSegment.from_wav(SOUNDS[game.melody[i]])
        play(sound)

def main():
    n = Network()
    player = int(n.getP())
    run = True
    clock = pygame.time.Clock()
    

    while run:
        clock.tick(FPS)
        try:
            game = n.send("get")
        except:
            menu_screen()


        if not game.connected():
            drawWindow(WIN, game)
        
        else:

            if game.phase == 'board':
                ROLLED = False
                if game.currPlayer == player:
                    drawBoard(WIN, game, True)
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            n.send('board')
                else:
                    drawBoard(WIN, game)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                        
            
            elif game.phase == 'dice':
                if game.currPlayer == player:
                    if not ROLLED:
                        roll = random.randint(1, 6)
                        print(str(roll))
                        n.send(str(roll))
                        drawDiceRoll(WIN, roll)
                # else:
                #     if game.rolled:
                #         drawDiceRoll(WIN, game.currRoll)
                #     n.send('dice')
                if game.rolled:
                    game = n.send("get")
                    drawDiceRoll(WIN, game.currRoll)
                    n.send('dice')
            elif game.phase == 'turn':
                if game.currPlayer == player:
                    if not game.went:
                        pygame.mixer.music.pause()
                        playSound(WIN, game)

                        ans = playGame(game, WIN)
                        n.send(ans)
                    else:
                        print("Went")
                        if game.correct:
                            pygame.mixer.music.unpause()
                            drawMove(WIN, game)
                            n.send('move')
                        else:
                            n.send('turn')
                else:
                    drawTurn(WIN)
            
            elif game.phase == 'end':
                drawEnd(WIN, game)
                n.send('reset')
                n.close()
                menu_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
def menu_screen():
    run = True
    clock = pygame.time.Clock()
    pygame.mixer.music.play(-1)

    while run:
        clock.tick(FPS)
        WIN.fill((0,0,0))
        WIN.blit(back, (0,0))

        font = pygame.font.SysFont('comicsansms', 64)
        subfont = pygame.font.SysFont('comicsansms', 48)
        text = font.render('PitchPerfect.io', False, (255,255,255))
        subtext = subfont.render("Press t for tutorial, any other key to start", False, (255,255,255))
        centerRect = text.get_rect(center = (WIDTH/2, HEIGHT/2 - 175))
        subRect = subtext.get_rect(center = (WIDTH/2, HEIGHT/2 + 175))
        WIN.blit(text, centerRect)
        WIN.blit(subtext, subRect)
        pygame.display.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    pygame.mixer.music.pause()
                    tutorial(WIN)
                    pygame.mixer.music.unpause()
                else:
                    run = False
    pygame.time.wait(2500)
    main()

# while True:
#     menu_screen()
