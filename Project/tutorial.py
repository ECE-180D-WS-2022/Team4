import pygame
import game
import Client


WIDTH, HEIGHT = 1400, 800
FPS = 60
msgTime = 3000
pygame.font.init()
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.mixer.music.load("Archive/skating.wav")
pygame.mixer.music.set_volume(0.7)

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

    game.setRoll(3)

    pygame.mixer.music.play(-1)
    # msg = 'Welcome to PitchPerfect.io!'
    # drawMsg(WIN, msg)
    
    # msg = 'Traverse through the board to win.'
    # drawMsg(WIN, msg, 'Board')

    # msg = 'Roll a die and win the corresponding minigame to move.'
    # drawMsg(WIN, msg, 'Board')

    # msg = 'Minigame mode depends on the color of your current spot.'
    # drawMsg(WIN, msg, 'Board')

    # msg = 'Minigame length is your die roll.'
    # drawMsg(WIN, msg, 'Dice')

    # msg = "Now let's try each minigame!"
    # drawMsg(WIN, msg)

    # msg = "Minigames start with a melody, remember each note."
    # drawMsg(WIN, msg, 'Keyboard')
    
    # game.setMode('Camera')
    # pygame.mixer.music.pause()
    # Client.playSound(WIN, game)

    # msg = "Copy the melody on the keyboard with your index finger."
    # drawMsg(WIN, msg, 'Keyboard')

    # ans = Client.playGame(game, WIN)
    # pygame.mixer.music.unpause()
    # game.check(ans)
    # if game.correct:
    #     msg = "Correct!"
    # else:
    #     msg = "Incorrect."
    # drawMsg(WIN, msg)

    # msg = "Now say the military alphabet name of each note."
    # drawMsg(WIN, msg, 'Keyboard')

    # msg = "Say one letter, then wait for the display to say the next."
    # drawMsg(WIN, msg, 'Keyboard')

    # game.reset()
    # game.setMode('Speech')
    # pygame.mixer.music.pause()
    # Client.playSound(WIN, game)
    # ans = Client.playGame(game, WIN)
    # pygame.mixer.music.unpause()
    # game.check(ans)
    # if game.correct:
    #     msg = "Correct!"
    # else:
    #     msg = "Incorrect."
    # drawMsg(WIN, msg)

    # msg = "Now try following the pitch by moving the controller."
    # drawMsg(WIN, msg)

    # msg = "If a note is higher than the previous note, rotate upward."
    # drawMsg(WIN, msg)

    msg = "If a note is lower than the previous note, rotate downward."
    drawMsg(WIN, msg)

    game.reset()
    game.updateSol()
    game.setMode('IMU')
    pygame.mixer.music.pause()
    Client.playSound(WIN, game)
    ans = Client.playGame(game, WIN)
    pygame.mixer.music.unpause()
    game.check(ans)
    if game.correct:
        msg = "Correct!"
    else:
        msg = "Incorrect."
    drawMsg(WIN, msg)

    msg = "Have fun playing!"
    drawMsg(WIN, msg)
    pygame.mixer.music.stop()
