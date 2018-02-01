from enum import Enum
import jwt

class Type(object):
    #ROUTER
    INIT_ROUTER = 1
    UPDATE_SENSORS = 20
    ACTIVE_SENSORS = 21
    SET_WIFI_CREDS = 3
    #PHONE
    LOGIN = 40
    LOGIN_RESPONSE = 41
    REGISTER = 50
    REGISTER_RESPONSE = 51
    REQUEST_ROUTERS = 6
    REQUEST_ROUTERS_SENSORS = 7
    UPDATE_SENSORS_PHONE = 22
    #MISC
    ERROR = 404
    PING = 100

def createPacket(type, token, payload, source):
    return {"token": token, "type":type, "payload":payload, "source":source}

def getType(packet):
    return packet["type"]

def getToken(packet):
    return packet['token']

def getPayload(packet):
    return packet["payload"]

def getSource(packet):
    return packet["source"]