 ## Melody Simon-says prototype ##
import os
import random
modes = ['Keyboard', 'Camera', 'Speech', 'IMU']

class Game:
    def __init__(self, id):
        self.boardH = 5
        self.boardW = 5
        self.board = self.makeBoard(self.boardH, self.boardW)
        self.currPlayer = 0
        self.rolled = False
        self.phase = 'board'
        self.went = False
        self.correct = False
        self.ready = False
        self.id = id
        self.numPlayers = 2
        self.spots = [0, 0]
        self.currAnswer = ''
        self.currRoll = 0
        self.currMode = 'Keyboard'
        self.sol = ''
        self.melody = [0]
        self.winner = 0
        self.oldSpot= 0
        

    def makeBoard(self, h, w):
        board = [[0 for i in range(h)] for j in range(w)]
        for i in range(h):
            for j in range(w):
                board[i][j] = random.randint(1, 3)
        return(board)
    

    def newRoll(self, num):
        print("NEWROLL " + num)
        num = int(num)
        self.currRoll = num
        self.rolled = True
        if self.spots[self.currPlayer] + self.currRoll < self.boardH*self.boardW:
            self.currMode = modes[self.board[(self.spots[self.currPlayer])//self.boardH][(self.spots[self.currPlayer])%self.boardH]]
        # else:
        #     self.currMode = modes[self.board[self.boardH-1][self.boardW-1]]
        self.makeSound(self.currMode)
    

    def makeSound(self, mode):
        lastnum = 7
        self.sol = ''
        self.melody = [0 for i in range(self.currRoll)]
        for i in range(self.currRoll):
            self.melody[i] = random.randint(0, 6) # 6 is number of sounds
            while self.melody[i] == lastnum:    #Note can't be played consecutively
                self.melody[i] = random.randint(0,6)
            lastnum = self.melody[i]
            self.sol += str(self.melody[i])
        if mode == 'Keyboard' or mode == 'IMU':
            relation = [0 for i in range(self.currRoll - 1)]
            for i in range(self.currRoll - 1):
                relation[i] = self.melody[i+1] - self.melody[i]
            self.sol = ''
            for i in range(len(relation)):
                if relation[i] < 0:
                    self.sol += 'v'
                elif relation[i] == 0:
                    self.sol += '>'
                elif relation[i] > 0:
                    self.sol += '^'

        print(self.melody)
        print(self.sol)


    def nextPhase(self, phase):
        if phase == 'board':
            print('dice')
            self.phase = 'dice'

        if phase == 'dice':
            print('turn')
            self.phase = 'turn'
  
        if phase == 'turn':
            print('resetting')
            self.reset()
            self.phase = 'board'
        
        if phase == 'end':
            self.phase = 'end'
        
    def getPhase(self):
        return(self.phase)

    def move(self):
        self.oldSpot = self.spots[self.currPlayer]
        self.spots[self.currPlayer] += self.currRoll
        if self.spots[self.currPlayer] >= self.boardH*self.boardW - 1:
            self.phase = 'end'
            self.winner = self.currPlayer
        self.correct = False

    def reset(self):
        self.rolled = False
        self.went = False
        self.correct = False
        self.currPlayer = (self.currPlayer+1)%self.numPlayers

    def newGame(self):
        self.rolled = False
        self.went = False
        self.correct = False
        self.currPlayer = 0
            

    def check(self, ans):
        if ans == self.sol:
            self.correct = True
            print("Correct!")
        else:
            print("Wrong")
        self.went = True

    def setCorrect(self, correct):
        self.correct = correct

    def getAns(self, player):
        return(self.answers[player])

    def connected(self):
        return self.ready
    
    def setMode(self, mode):
        self.currMode = mode

    def setRoll(self, num):
        self.currRoll = num
        self.makeSound(self.currMode)
