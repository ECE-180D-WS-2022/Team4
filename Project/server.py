from ctypes import sizeof
import socket
import sys
from _thread import *
import pickle
from game import Game

server = "131.179.36.39"
port = 5555
rolls = ['zero', 'one', 'two', 'three', 'four', 'five', 'six']
modes = ['Keyboard', 'IMU', 'Camera', 'Speech']
phases = ['board', 'turn', 'end']

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0

def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()
            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.newGame()
                    elif data in phases:
                        game.nextPhase(data)
                    elif data == "move":
                        game.move()
                    elif data in rolls:
                        game.nextPhase('dice')
                        game.newRoll(data)
                    elif data != "get":
                        game.check(data)
                    # elif data != "get":
                    #     mode, ans = data.split(' ', 1)
                    #     game.check(p, ans, mode)
                    conn.sendall(pickle.dumps(game))
                    
            else:
                break
        except:
            break
    print("Lost Connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount%2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
