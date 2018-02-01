from WAMP import *
from Database.change_handler import ChangeHandler
import multiprocessing
from autobahn.twisted.websocket import WebSocketServerFactory
from twisted.internet import reactor
from threading import Thread

ServerInstance = None

class Server:

    def __init__(self):
        self.WAMP = WAMP();
        pass
    def startupWAMP(self):
        pass
    def startupHTTP(self):
        pass
    def stopWAMP(self):
        pass
    def stopHTTP(self):
        pass

if __name__ == '__main__':
    ServerInstance = Server()

def getServer():
    return ServerInstance