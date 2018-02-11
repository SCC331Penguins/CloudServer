from flask import request, jsonify, abort, Blueprint
from Database.dbhandler import DbHandler
from Database.change_handler import ChangeHandler
from functools import wraps
import config
import json
from WAMP import packet
from Authentication import authenticator

function = Blueprint('function',__name__)

@function.route("/function/ping", methods=['POST'])
def function_ping():
    return jsonify()

@function.route("/function/update_token", methods=['POST'])
def open_socket():
    db = ChangeHandler(None)
    db.new_change(request.json['id'], packet.Type.OPEN_SOCKET)
    return jsonify()