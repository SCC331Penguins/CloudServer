from flask import request, jsonify, abort, Blueprint
from Database.dbhandler import DbHandler
from Database.change_handler import ChangeHandler
from functools import wraps
import config
import json
from WAMP import packet
from Authentication import authenticator

router = Blueprint('router',__name__)

@router.route("/router/get_router", methods=['POST'])
def get_router():
    db = DbHandler()
    result = db.get_users_router(request.json['token'])
    return jsonify(result)

@router.route("/router/test", methods=['POST'])
def test():
    db = DbHandler()
    result = db.get_users_router(request.json['token'])
    return jsonify(result)