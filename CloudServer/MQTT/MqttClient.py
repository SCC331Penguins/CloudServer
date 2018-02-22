from flask import json
from twisted.application.internet import ClientService, backoffPolicy
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks


class MQTTService(ClientService):
    def __init__(self, endpoint, factory):
        ClientService.__init__(self, endpoint, factory, retryPolicy=backoffPolicy())
        self.cb = None
        self.updateScripts = None
        self.channels = ['SCC33102_R01']

    def startService(self):
        self.whenConnected().addCallback(self.connectToBroker)
        ClientService.startService(self)

    @inlineCallbacks
    def connectToBroker(self, protocol):
        self.protocol                 = protocol
        self.protocol.onPublish       = self.onPublish
        self.protocol.onDisconnection = self.onDisconnection
        self.protocol.setWindowSize(1)
        try:
            yield self.protocol.connect('', keepalive=60)
            yield self.subscribe()
        except Exception as e:
            print(e)
        else:
            self.sendMsg(64,{'MAC':'AC:CF:23:A1:FB:38','type':'Lights','command':'allLightsOff'},topic="SCC33102_R01")

    def subscribe(self):
        for channel in self.channels:
            self.protocol.subscribe(channel, 1 )

    def set_broadcast(self, cb, scripts):
        self.updateScripts = scripts
        self.cb = cb

    def sendMsg(self, typeInt, payload, topic=None, msgObject={}):
        msgObject[u'type'] = typeInt
        msgObject[u'payload'] = payload
        #msgObject[u'token'] = self.token
        self.publish(topic,json.dumps(msgObject,ensure_ascii=False).encode())

    def onPublish(self, topic, payload, qos, dup, retain, msgId):
        print(payload)
        print(str(payload))
        msg = json.loads(str(payload))
        print(type(msg))

    def publish(self, topic, msg, q=1):
        self.protocol.publish(topic=topic, qos=1, message=msg)

    def onDisconnection(self, reason):
        self.whenConnected().addCallback(self.connectToBroker)
