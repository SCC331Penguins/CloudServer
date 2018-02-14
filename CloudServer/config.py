from flask import request
from functools import wraps

DEBUG = True                        #Change to false if printing json requests is to be turned off
HOST = '192.168.1.73'              #IP for the flask server to run on
SHARED_SECRET_KEY = 'scc331sharedsecretkey'      #Server secret key
DATABASE_NAME = 'database.sqlite3'  #Database name
CHANGE_DATABASE_NAME = 'changes.sqlite3'  #Database name
TOKEN_EXPIRE = 999999

#Error types
ERROR_LOGIN_ATTEMPT = "lOGIN"
ERROR_INVALID_ROUTER = "INVRO"
ERROR_INVALID_SENSOR = "INVSE"
ERROR_UNAUTHORISED_ACCESS = "UAUTH"

FCM_SERVER_API = "AAAAmg2JIFk:APA91bFAeucUqBmbLwCQYdb91mOmuFgYXYa8fa_hGpODnM7r5cugEMdlllk0p4MOglh7gGc0LHL0xqFprfAHBRnbKW7zo0Vo5GkyeauPpopskjfRw_3co8K96NTYrptWrLwW76w60Uk9"

def debug_route(f):
    @wraps(f)
    def print_request(*args, **kwargs):
        if DEBUG == True:
            print(request.json)
        return f(*args, **kwargs)
    return print_request