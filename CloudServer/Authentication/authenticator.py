from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import config
import jwt

def generate_token(id):
    try:
        payload = {'id': id}
        return jwt.encode(payload,config.SHARED_SECRET_KEY,algorithm="HS256")
    except Exception as e:
        print(e)
        return

def verify_token(token):
    try:
        payload = jwt.decode(token, "scc331sharedsecretkey")
        return payload['id']
    except jwt.InvalidTokenError:
        return False