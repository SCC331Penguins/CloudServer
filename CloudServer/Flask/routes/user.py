from flask import request, jsonify, abort, Blueprint
from Database.dbhandler import DbHandler
from functools import wraps
import config
from Authentication import authenticator
from Flask.Function.debug import debug_json

user = Blueprint('user',__name__)

@user.route('/user/login', methods=['POST'])
@debug_json
def login():
    username = request.json['username']
    password = request.json['password']
    dbHandler = DbHandler()
    result = dbHandler.login_user(username, password=password)
    print(result[0][1])
    if result[0][0] == True:
        return jsonify(logged_in=result[0][0], token=result[0][1]), 200
    return jsonify(logged_in=result[0][0], message=result[0][1]), 200

@user.route('/user/register', methods=['POST'])
@debug_json
def register():
    username = request.json['username']
    password = request.json['password']
    dbHandler = DbHandler()
    message = dbHandler.create_user(username, password)
    return jsonify(message), 201

@user.route('/test', methods=['POST'])
def test():
    resp = request.json['username']
    db = DbHandler()
    return jsonify(result=db.get_router_sensors("SCC33102_R01"), data=resp)
