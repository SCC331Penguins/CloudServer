from .connection import *
import config
from Handlers import message_handler
from Database import change_handler
import zerorpc
from threading import Thread

class WAMP:

    def __init__(self):
        self.connections = [];
        self.connection = Connection('local',handler=self.handleMessage)
        self.connection.connect();
        pass

    def run(self):
        return "HEY RPC"

    def handleMessage(self, channel, conName, message):
        m = message_handler.HandlePacket()
        return_chann = m.handle_packet(message)
        if return_chann != None:
            self.connection.sendEvent(return_chann['chan'],return_chann['packet'])
        pass
