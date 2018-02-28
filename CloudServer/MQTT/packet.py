from enum import Enum
import jwt

class Type(object):
    #ROUTER
    INIT_ROUTER = 1
    UPDATE_SENSORS = "UPDSEN"
    ACTIVE_SENSORS = "ACTSEN"
    SET_WIFI_CREDS = "WIFICR"
    #PHONE
    LOGIN = 4
    REGISTER = 5
    REQUEST_ROUTERS = 6
    REQUEST_ROUTERS_SENSORS = 7
    UPDATE_SENSORS_PHONE = 22
    UPDATE_SCRIPT = "UPDSCR"
    OPEN_SOCKET = 101
    #MISC
    ERROR = 404
    PING = "PING"
    SAVE_DATA = "DATA"
    NEW_CHANNEL = "NCHAN"
    REG_ACTUATOR = "REGACT"
    NOTIFICATION = "NOTIF"

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