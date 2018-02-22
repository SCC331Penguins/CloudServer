from flask import request, jsonify, abort, Blueprint
from Database.dbhandler import DbHandler
from Database.change_handler import ChangeHandler
from functools import wraps
import config
import json
from MQTT import packet
from Authentication import authenticator

router = Blueprint('router',__name__)

@router.route("/router/get_router", methods=['POST'])
def get_router():
    db = DbHandler()
    result = db.get_users_router(request.json['token'])
    return jsonify(result), 200

@router.route("/router/claim_router", methods=['POST'])
def claim_router():
    db = DbHandler()
    res = db.register_router(authenticator.verify_token(request.json['token']), request.json['router_id'])
    return jsonify(result=res), 200

@router.route("/router/test", methods=['POST'])
def test():
    db = DbHandler()
    result = db.get_users_router(request.json['token'])
    return jsonify(result), 200

@router.route("/router/set_script", methods=['POST'])
def set_script():
    db = DbHandler()
    print(request.json)
    result = db.record_script(request.json["router_id"], request.json['script'])
    if result == 1:
        dbh = ChangeHandler(None)
        dbh.new_change(request.json["router_id"], packet.Type.UPDATE_SCRIPT)
        return jsonify(), 200
    return jsonify(), 406

@router.route("/router/get_actuators", methods=['POST'])
def get_actuators():
    db = DbHandler()
    res = db.get_actuators(request.json['router_id'])
    return jsonify(res), 200