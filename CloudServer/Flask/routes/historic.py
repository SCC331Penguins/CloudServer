from flask import request, jsonify, abort, Blueprint
from Database.dbhandler import DbHandler
from Database.change_handler import ChangeHandler
from functools import wraps
import config
import json
from Flask.Function import debug
from MQTT import packet
from Authentication import authenticator
from Handlers.notification_handler import send_notification
from Database.historic_handler import HistoricHandler

historic = Blueprint('historic',__name__)

@historic.route("/historic/save", methods=['POST'])
def historic_temp():
    parse_record(request.json)
    return jsonify(data=0), 200



def parse_record(json_string):
    router_id = json_string['router_id']
    sensors = json_string['sensors']
    for x in sensors[:]:
        print(x)
    pass

@historic.route("/historic/get_history", methods=['POST'])
def get_history():
    #id = authenticator.verify_token(request.json['token'])
    router_id = request.json['router_id']
    sensor_id = request.json['sensor_id']
    start = request.json['start']
    end = request.json['end']
    print(request.json)

    if start == 0 or end == 0:
        start = None
        end = None

    hh = HistoricHandler()

    if sensor_id == "ALL":
        data = {}
        db = DbHandler()
        sensors = db.get_router_sensors(router_id)

        for x in sensors[:]:
            s_id = x[0]
            res = hh.get_reading(router_id, s_id, start=start, end=end)
            print("Results: " + res);
            data.update({s_id:res})

        return jsonify(data=data)

    result = hh.get_reading(router_id, sensor_id, start=start, end=end)
    ret = {}
    ret.update({sensor_id:result})

    return jsonify(data=ret)

@historic.route("/history/test", methods=['POST'])
def test():
    send_notification("SCC33102_R01",{"title":"Notification","message":"Hey this is a message"})
    return jsonify(result=0),200