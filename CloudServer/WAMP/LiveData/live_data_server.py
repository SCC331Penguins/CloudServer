from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from WAMP.LiveData.bridge import Bridge

clients = []
bridges = []


class LiveDataServer(WebSocket):

    def handleMessage(self):
        print(self.data)
        self.data = dict(x.split('=') for x in self.data.split(','))
        self.sendMessage("Hiya")



def handleConnected(self):
    print(self.address, 'connected')
    for client in clients:
        client.sendMessage(self.address[0] + u' - connected')
    clients.append(self)
    print(clients)


def handleClose(self):
    print(self.address, 'closed')
