from mqtt.client.factory import MQTTFactory
from twisted.internet import reactor
from twisted.internet.endpoints import clientFromString
from MQTT.MttqClientResolve import MQQTClient
import config

class MqttStart():

    def __init__(self):
        self.run_resolve()

    def run_resolve(self):
        self.mqtt_client = MQQTClient()
        self.mqtt_client.connect(config.HOST)

if __name__ == '__main__':
    g = MqttStart()
