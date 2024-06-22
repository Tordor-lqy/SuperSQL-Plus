import jwt
import datetime
from config import jwt_config


def create_jwt(payload):
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    return jwt.encode(payload, jwt_config['secretkey'], algorithm='HS256')


def parse_jwt(token):
    try:
        payload = jwt.decode(token, jwt_config['secretkey'], algorithms='HS256')
    except jwt.ExpiredSignatureError:
        return False, "令牌过期"
    except jwt.InvalidTokenError:
        return False, "非法的令牌"
    return True, payload
