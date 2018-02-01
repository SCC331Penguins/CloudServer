from flask import request, jsonify, abort, Blueprint
from Database.dbhandler import DbHandler
from functools import wraps
import config
from Authentication import authenticator

user = Blueprint('user',__name__)

@user.route('/user/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    dbHandler = DbHandler()
    result = dbHandler.login_user(username, password=password)
    if result[0][0] == True:
        return jsonify(logged_in=result[0][0], token=result[0][1]), 201
    return jsonify(logged_in=result[0][0], message=result[0][1]), 201

@user.route('/user/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    dbHandler = DbHandler()
    message = dbHandler.create_user(username, password)
    return jsonify(message), 201

@user.route('/test', methods=['POST'])
def test():
    db = DbHandler()
    return jsonify(result=db.get_router_status("SCC33102_R01"))
