from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
import json
import config
from Database import dbhandler
from Database import change_handler
from threading import Thread
from WAMP.LiveData.live_data_server import LiveDataServer
from SimpleWebSocketServer import SimpleWebSocketServer

class Connection(ApplicationSession):

    def __init__(self, name, port=8080, host='localhost',path='/ws', realm="default", channels=[], procedures=[], handler=None):
        ApplicationSession.__init__(self,None)
        self.name = name
        self.host = host
        self.port = port
        self.path = path
        self.realm = realm
        db = dbhandler.DbHandler()
        res = db.get_router_channels();
        chan = []
        for x in res[:]:
            chan.append(x[0])
        self.channels = chan
        self.procedures = procedures
        self.handler = handler

        print( "ws://"+self.host+":"+str(self.port)+self.path)
        pass

    def connect(self):
        run = ApplicationRunner(
            u"ws://"+self.host+":"+str(self.port)+self.path,
            u""+self.realm
        )
        run.run(self)

    def onJoin(self, details):
        print('Connecting')
        print('s {}'.format(details))
        for chan in self.channels:
            self.subscribe(lambda d : self.onEvent(d,chan),chan)
            print(chan)
        Thread(target=self.startupChangeChecker).start()
        Thread(target=self.startLiveDataServer).start()
        pass

    def openPhoneSocket(self, uniqueid):
        print("Opening phone socket " + str(uniqueid))
        self.subscribe(lambda  d : self.onEvent(d,uniqueid),uniqueid)
        pass

    def startLiveDataServer(self):
        server = SimpleWebSocketServer(config.HOST, 8000, LiveDataServer)
        server.serveforever()

    def startupChangeChecker(self):
        ch = change_handler.ChangeHandler(self)
        ch.check_changes()

    def onEvent(self, msg=None, evt=None):
        print("Got message: {}".format(msg))
        if(self.handler):
            self.handler(evt, self.name, msg)
        pass
    
    def sendEvent(self, evt, message):
        self.publish(evt, message)
        pass