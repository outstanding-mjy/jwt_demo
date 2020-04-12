import jwt
import datetime

from jwt_demo import settings


def create_token(payload, timeout=1):
    salt =settings.SECRET_KEY
    #构造header
    headers ={
    'typ': ' jwt',
    'alg': 'HS256'
    }

    #构造payload
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta (minutes=timeout)  # 超时时间
    token = jwt.encode (payload=payload, key=salt, algorithm="HS256", headers=headers).decode('utf-8')
    return token