from flask import request, jsonify, abort, Blueprint
from Database.dbhandler import DbHandler
from Database.change_handler import ChangeHandler
from functools import wraps
import config
import json
from Flask.Function import debug
from MQTT import packet
from Authentication import authenticator
import uuid

api = Blueprint('api',__name__)

@api.route("/api/requestLiveData", methods=['POST'])
def request_live_data():
    if authenticator.verify_token(request.json['token']) == False: return
    topic_name = str(uuid.uuid4())
    db = DbHandler()
    db.new_channel(request.json['router_id'], topic_name)
    ch = ChangeHandler(None)
    ch.new_change(request.json['router_id'], packet.Type.NEW_CHANNEL)
    return jsonify(topic_name=topic_name), 200

@api.route("/api/gettoken", methods=['GET'])
def get_token():
    return jsonify(authenticator.generate_token("SCC33102_R01"))