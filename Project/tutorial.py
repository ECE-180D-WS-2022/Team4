import pygame
import game
import Client


WIDTH, HEIGHT = 1400, 800
FPS = 60
msgTime = 3000
pygame.font.init()
game = game.Game(1)

def drawMsg(WIN, msg, background = ''):
    WIN.fill((0,0,0))
    font = pygame.font.SysFont('comicsansms', 48)
    text = font.render(msg, False, (255,255,255))
    if background == 'Board':
        Client.drawBoardGrid(game, 1)
        rect = text.get_rect(center = (WIDTH/2, HEIGHT/2 + 300))
    elif background == 'Keyboard':
        Client.drawSound(WIN, -1)
        rect = text.get_rect(center = (WIDTH/2, HEIGHT/2 + 250))
    elif background == 'Dice':
        diceRect = Client.D3.get_rect(center = (WIDTH/2, Client.TEXT_HEIGHT))
        WIN.blit(Client.D3, diceRect)
        rect = text.get_rect(center = (WIDTH/2, HEIGHT/2))
    else: 
        rect = text.get_rect(center = (WIDTH/2, HEIGHT/2))

    WIN.blit(text, rect)
    pygame.display.update()
    Client.checkQuit()
    pygame.time.delay(msgTime)


def tutorial(WIN):

    msg = 'Welcome to PitchPerfect.io!'
    drawMsg(WIN, msg)
    
    msg = 'Traverse through the board to win.'
    drawMsg(WIN, msg, 'Board')

    msg = 'Roll a die and win the corresponding minigame to move.'
    drawMsg(WIN, msg, 'Board')

    msg = 'Minigame mode depends on the color of your current spot.'
    drawMsg(WIN, msg, 'Board')

    msg = 'Minigame length is your die roll.'
    drawMsg(WIN, msg, 'Dice')

    msg = "Now let's try each minigame!"
    drawMsg(WIN, msg)

    msg = "Minigames start with a melody, remember each note."
    drawMsg(WIN, msg, 'Keyboard')
    
    game.setMode('Camera')
    game.setRoll(3)
    Client.playSound(WIN, game)

    msg = "Copy the melody on the keyboard with your index finger."
    drawMsg(WIN, msg, 'Keyboard')

    ans = Client.playGame(game, WIN)
    game.check(ans)
    if game.correct:
        msg = "Correct!"
    else:
        msg = "Incorrect."
    drawMsg(WIN, msg)

    msg = "Now say the military alphabet name of each note."
    drawMsg(WIN, msg, 'Keyboard')

    game.setMode('Speech')
    Client.playSound(WIN, game)
    ans = Client.playGame(game, WIN)
    game.check(ans)
    if game.correct:
        msg = "Correct!"
    else:
        msg = "Incorrect."
    drawMsg(WIN, msg)

    msg = "Have fun playing!"
    drawMsg(WIN, msg)
