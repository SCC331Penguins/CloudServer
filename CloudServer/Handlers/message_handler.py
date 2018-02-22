import json
from Database import dbhandler
from Authentication import authenticator
from MQTT import packet
from datetime import datetime
from Database.historic_handler import HistoricHandler
import calendar

class MessageHandler():

    def __init__(self, message):
        self.message = message
        self.handle_packet()

    def handle_packet(self):

        id = self.message.getId()
        type = self.message.getType()
        message_payload = self.message.getPayload()
        topic = self.message.getTopic()

        if type == packet.Type.ACTIVE_SENSORS:
            self.active_sensors(id, message_payload)
            pass
        elif type == packet.Type.REQUEST_ROUTERS:
            pass
        elif type == packet.Type.REQUEST_ROUTERS_SENSORS:
            pass
        elif type == packet.Type.SET_WIFI_CREDS:
            pass
        elif type == packet.Type.PING:
            self.ping(id)
        elif type == packet.Type.SAVE_THL:
            self.parse_record(message_payload)
        else:
            print("invalid type")
            return
        return None

    def parse_record(self, json_string):
        router_id = json_string['router_id']
        sensors = json_string['sensors']
        d = datetime.utcnow()
        unixtime = calendar.timegm(d.utctimetuple())
        hist = HistoricHandler()
        for x in sensors[:]:
            hist.record_reading(unixtime, router_id, x)

    def update_sensors(self, router_id):
        db = dbhandler.DbHandler()
        result = db.get_router_sensors(router_id)
        payload_format = ["id", "config"]
        payload = []
        for x in result[:]:
            payload.append(dict(zip(payload_format, x)))
        packet_to_send = packet.createPacket(packet.Type.UPDATE_SENSORS, 0, payload, 0)
        print(packet_to_send)
        return packet_to_send

    def update_script(self, router_id):
        db = dbhandler.DbHandler()
        result = db.get_script(router_id)
        payload_to_send = []
        for x in result[:]:
            payload_to_send.append(x[0])
        return packet.createPacket(packet.Type.UPDATE_SCRIPT, 0, payload_to_send, 0)

    def active_sensors(self, router_id, sensors):
        print(sensors)
        db = dbhandler.DbHandler()
        for x in sensors[:]:
            db.init_sensor(x['id'], router_id)
        pass

    def ping(self, router_id):
        db = dbhandler.DbHandler()
        db.update_router_status(router_id)
        print("ping: " + str(router_id))