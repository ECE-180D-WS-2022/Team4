import speech_recognition as sr
import pygame


WIDTH, HEIGHT = 1400, 800


letters = {'alpha': 'A', 'bravo': 'B', 'charlie': 'C', 'delta': 'D', 'echo': 'E', 'foxtrot': 'F', 'golf': 'G'}
H = 50

def drawSpeechLegend(WIN):
    font = pygame.font.SysFont('comicsansms', 24)
    txtVar = font.render("A = Alpha", True, (255,255,255))
    WIN.blit(txtVar, (20,0))
    
    txtVar = font.render("B = Bravo", True, (255,255,255))
    WIN.blit(txtVar, (20, H))
    
    txtVar = font.render("C = Charlie", True, (255,255,255))
    WIN.blit(txtVar, (20,2*H))
    
    txtVar = font.render("D = Delta", True, (255,255,255))
    WIN.blit(txtVar, (20,3*H))
    
    txtVar = font.render("E = Echo", True, (255,255,255))
    WIN.blit(txtVar, (20,4*H))

    txtVar = font.render("F = Foxtrot", True, (255,255,255))
    WIN.blit(txtVar, (20,5*H))
    
    txtVar = font.render("G = Golf", True, (255,255,255))
    WIN.blit(txtVar, (20,6*H))
    
    txtVar = font.render("Stop", True, (255,255,255))
    WIN.blit(txtVar, (20, 7*H))
    
    txtVar = font.render("Redo", True, (255,255,255))
    WIN.blit(txtVar, (20, 8*H))
    
    pygame.display.update()
    
    

def speechRecognition(WIN):
    WIN.fill((0,0,0))
    font = pygame.font.SysFont('comicsansms', 35)
    text = font.render('Calibrating...', True, (255,255,255))
    WIN.blit(text, text.get_rect(center = (WIDTH/2, HEIGHT/2)))
    pygame.display.update()
    pygame.time.delay(2000)

    r = sr.Recognizer()
    m = sr.Microphone()
    
    run = True
    answer = '' #answer in number form
    #with m as source: r.adjust_for_ambient_noise(source)
    with m as source: r.energy_threshold = 5000
    with m as source: r.pause_threshold = 1
    WIN.fill((0,0,0))
    text = font.render("Ready!", True, (255,255,255))
    WIN.blit(text, text.get_rect(center = (WIDTH/2, HEIGHT/2)))
    pygame.display.update()

    while run:
        WIN.fill((0,0,0))
        drawSpeechLegend(WIN)
        with m as source: audio = r.listen(source)
        try:
            # recognize speech using Google Speech Recognition
            i = r.recognize_google(audio)
            # value is the variable here
            
            #speech_input_list = value.split()   #separates speech input into a list of words
            
            #User input library
            if(i == 'alpha' or i == 'Alpha'):
                answer = answer + '0'
            elif(i == 'bravo' or i == 'Bravo'):
                answer = answer + '1'
            elif(i == 'charlie' or i == 'Charlie' or i == 'Charmy' or i == 'charmy' or i == 'Carly' or i == 'carlie'):
                answer = answer + '2'
            elif(i == 'delta' or i == 'Delta'):
                answer = answer + '3'
            elif(i == 'echo' or i == 'Echo'):
                answer = answer + '4'
            elif(i == 'foxtrot' or i == 'Foxtrot'):
                answer = answer + '5'
            elif(i == 'golf' or i == 'Golf'):
                answer = answer + '6'
            elif(i == 'stop' or i == 'Stop'):     #stop word (ends user speech turn)
                run = False
            elif(i == 'Redo' or i == 'redo'):     #Redo word(Redo previous word)
                answer = answer[:-1]
                
                
                
            #window drawing
            if i.lower() in letters:
                txt = letters[i.lower()]
            else:
                txt = i
            text = font.render(txt, True, (255,255,255))
            WIN.blit(text, text.get_rect(center = (WIDTH/2, HEIGHT/2)))
            pygame.display.update()
            pygame.time.delay(1000)
        
            
    #speech Recognition errors
        except sr.UnknownValueError:
            run = False
        except sr.RequestError as e:
            return "Uh oh! Couldn't request results from Google Speech Recognition service; {0}"
    return answer
