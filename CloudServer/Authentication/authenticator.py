from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask import request
from functools import wraps
import config
import jwt

def generate_token(id):
    try:
        payload = {'id': id}
        return (jwt.encode(payload,config.SHARED_SECRET_KEY,algorithm="HS256")).decode("utf-8")
    except Exception as e:
        print(e)
        return

def verify_token(token):
    try:
        payload = jwt.decode(token, config.SHARED_SECRET_KEY)
        return payload['id']
    except jwt.InvalidTokenError:
        return False

def verify_flask_token(f):
    @wraps(f)
    def token(*args, **kwargs):
        token_req = request.json['token']
        try:
            jwt.decode(token_req, config.SHARED_SECRET_KEY)
        except Exception:
            return False
        return f(*args,**kwargs)
    return token