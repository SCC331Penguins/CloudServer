import paho.mqtt.client as mqtt
from threading import Thread
from Database.dbhandler import DbHandler
from flask import jsonify
from datetime import datetime
import calendar
import config
import json
import time
from Handlers.message_parser import MessageParser
from Handlers.message_handler import MessageHandler
from Database.change_handler import ChangeHandler

class MQQTClient():

    def __init__(self):
        print("Initiating MQTT Client")
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        db = DbHandler()
        self.channels = db.get_router_channels()
        print(self.channels)
        self.last_message = ""
        self.last_topic = ""
        self.last_message_time = 0

    def connect(self, ip, port=1883):
        print("Connecting...")
        self.client.connect(config.BROKER, port)
        self.subscribe()
        Thread(target=self.start_loop).start()
        Thread(target=self.launch_batch_change_handler).start()

    def launch_batch_change_handler(self):
        ch = ChangeHandler(self)
        ch.check_changes()

    def start_loop(self):
        print("Looping...")
        self.client.loop_forever()

    def on_message(self, client, userdata, message):
        print(message.payload)
        if self.check_repeat(message) == True: return
        string = message.payload.decode("utf-8")
        json_acceptable_string = string.replace("'", "\"")
        payload = json.loads(json_acceptable_string)
        message_parsed = MessageParser(message.topic, payload)
        #Check if valid token
        if message_parsed.getId() == False:
            return
        print(message.topic + ", " + str(message.payload))
        Thread(target=self.handle_message,args=(message_parsed,)).start()

    def handle_message(self, message):
        MessageHandler(message)

    def check_repeat(self, message):
        millis = int(round(time.time() * 1000))
        if message.payload == self.last_message \
                and message.topic == self.last_topic \
                    and millis - self.last_message_time < 100: return True
        return False

    def publish(self,topic, message):
        self.client.publish(topic, message)

    def subscribe(self, topic=None):
        if topic == None:
            for x in self.channels[:]:
                self.client.subscribe(x[0]);
            print("Subscribed to Routers: " + str(self.channels))
            return
        self.client.subscribe(topic)
        print("Subscribed to : " + topic)

    def send_message(self, typeInt, payload, topic=None, msgObject={}):
        self.last_message = json.dumps(msgObject,ensure_ascii=False).encode()
        self.last_topic = topic
        millis = int(round(time.time() * 1000))
        self.last_message_time = millis
        print(str(json.dumps(payload,ensure_ascii=False).encode()))
        self.publish(topic,json.dumps(payload,ensure_ascii=False).encode())

    def on_connect(self, client, flags, userdata, rc):
        print("Connected to MQTT Broker: ", config.BROKER)

    def on_disconnect(self):
        pass

