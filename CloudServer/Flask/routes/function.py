from flask import request, jsonify, abort, Blueprint
from Database.dbhandler import DbHandler
from Database.change_handler import ChangeHandler
from functools import wraps
import config
import json
from Flask.Function import debug
from MQTT import packet
from Authentication import authenticator

function = Blueprint('function',__name__)

@function.route("/function/ping", methods=['POST'])
def function_ping():
    return jsonify()

@function.route("/function/update_token", methods=['POST'])
@authenticator.verify_flask_token
def open_socket():
    db = DbHandler()
    db.update_phone_token(request.json["token"],request.json["token_phone"])
    return jsonify()