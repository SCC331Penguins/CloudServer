from flask import request, jsonify, abort, Blueprint
from Database.dbhandler import DbHandler
from Database.change_handler import ChangeHandler
from functools import wraps
import config
import json
from Flask.Function import debug
from WAMP import packet
from Authentication import authenticator
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