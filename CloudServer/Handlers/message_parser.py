from Authentication import authenticator

class MessageParser():

    def __init__(self,topic, payload):
        self.topic = topic
        self.raw_payload = payload;
        self.parse()

    def parse(self):
        self.type = self.raw_payload['type']
        self.parsed_payload = self.raw_payload['payload']
        self.token = authenticator.verify_token(self.raw_payload['token'])

    def getType(self):
        return self.type

    def getPayload(self):
        return self.parsed_payload

    def getId(self):
        return self.token

    def getTopic(self):
        return self.topic