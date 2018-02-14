import json
from Database import dbhandler
from Authentication import authenticator
from WAMP import packet
import jwt

class HandlePacket():

    def __init__(self, ):
        pass

    def handle_packet(self, message):

        token = packet.getToken(message)
        return_channel = authenticator.verify_token(token)
        if return_channel == False:
            return {'chan': return_channel, 'packet': packet.createPacket(packet.Type.ERROR, 0, "Token Invalid", 0)}

        type = packet.getType(message)
        packet_payload = packet.getPayload(message)

        if type == packet.Type.INIT_ROUTER:
            return {'chan': return_channel, 'packet': packet.createPacket(packet.Type.LOGIN, 0, "Init", 0)}
            pass
        elif type == packet.Type.LOGIN:
            print(login(packet_payload))
            pass
        elif type == packet.Type.REGISTER:
            print(register(packet_payload))
        elif type == packet.Type.ACTIVE_SENSORS:
            active_sensors(return_channel, message['payload'])
            pass
        elif type == packet.Type.REQUEST_ROUTERS:
            pass
        elif type == packet.Type.REQUEST_ROUTERS_SENSORS:
            pass
        elif type == packet.Type.SET_WIFI_CREDS:
            pass
        elif type == packet.Type.PING:
            ping(return_channel)
        else:
            print("invalid type")
            return
        return None

def update_sensors(router_id):
    db = dbhandler.DbHandler()
    result = db.get_router_sensors(router_id)
    payload_format = ["id","config"]
    payload = []
    for x in result[:]:
        payload.append(dict(zip(payload_format,x)))
    packet_to_send = packet.createPacket(packet.Type.UPDATE_SENSORS,0,payload,0)
    return packet_to_send

def update_script(router_id):
    db = dbhandler.DbHandler()
    result = db.get_script(router_id)
    payload_to_send = []
    for x in result[:]:
        payload_to_send.append(x[0])
    return packet.createPacket(packet.Type.UPDATE_SCRIPT,0,payload_to_send,0)

def active_sensors(router_id, sensors):
    print(sensors)
    db = dbhandler.DbHandler()
    for x in sensors[:]:
        db.init_sensor(x['id'], router_id)
    pass

def ping(router_id):
    db = dbhandler.DbHandler()
    db.update_router_status(router_id)
    print("ping: " + str(router_id))

def login(packet_payload):
    db = dbhandler.DbHandler()
    return db.login_user(packet_payload['username'], packet_payload['password'])

def register(packet_payload):
    db = dbhandler.DbHandler()
    return db.create_user(packet_payload['username'], packet_payload['password'])
