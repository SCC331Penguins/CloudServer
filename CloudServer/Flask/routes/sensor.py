from flask import request, jsonify, abort, Blueprint
from Database.dbhandler import DbHandler
from Database.change_handler import ChangeHandler
from functools import wraps
import config
import json
from WAMP import packet
from Authentication import authenticator

sensor = Blueprint('sensor',__name__)

@sensor.route('/sensor/set_config', methods=['POST'])
def set_sensor_config():
    #TODO: Parse json
    payload_parse = request.json['payload']
    router_id = payload_parse['router_id']
    sensors = payload_parse['sensors']
    for x in sensors[:]:
        db = DbHandler()
        db.set_sensor_mode(x['id'],x['config'])
    ch = ChangeHandler(None)
    ch.new_change(router_id, packet.Type.UPDATE_SENSORS)
    return jsonify(payload=sensors)

@sensor.route('/sensor/get_sensors', methods=['POST'])
@authenticator.verify_flask_token
def get_sensor_config():
    db = DbHandler()
    resp = db.get_router_sensors(request.json['router_id'])
    return jsonify(resp)