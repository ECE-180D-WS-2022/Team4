import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
<<<<<<< HEAD
        self.server = "192.168.1.66"
=======
        self.server = "192.168.1.89"
>>>>>>> 0b9416e3b51a6e0b337e3f5089feeb80fcbb9930
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p
    
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass
    
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*8))
        except socket.error as e:
            print(e)

    def close(self):
        self.client.close()
