from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from jwt import exceptions
import jwt

from jwt_demo import settings


class JwtQueryParamsAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get(' token')
        # 1.切割
        # 2.解密第二段/判断过期
        # 3.验证第三段合法性

        salt = settings.SECRET_KEY
        try:
            payload = jwt.decode(token, salt, True)
        except exceptions.ExpiredSignatureError:
            raise AuthenticationFailed({'code': 1003, 'error': 'token已失效'})
        except jwt.DecodeError:
            raise AuthenticationFailed({'code': 1003, 'error': 'token认证失败'})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({'code': 1003, 'error': '非法的token'})
        # 三种操作
        # 抛出异常，后续不再执行
        # return 元祖(1，2) request.user 返回第一个值 request.auth返回第二个值
        # None
        return (payload, token)


