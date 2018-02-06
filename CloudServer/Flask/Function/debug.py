from config import DEBUG
from functools import wraps
from flask import request

def debug_json(f):
    @wraps(f)
    def debug(*args,**kwargs):
        if DEBUG == True:
            print(request.json)
        return f(*args, **kwargs)
    return debug