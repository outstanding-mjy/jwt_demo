from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import UserInfo
import uuid
from api.extensions.auth import JwtQueryParamsAuthentication
from api.utils.jwt_auth import create_token

class LoginView(APIView):
    '''
    用户登录
    '''

    def post(self, request, *args, **kwargs):
        user = request.data.get('username')
        password = request.data.get('password')
        user_obj = UserInfo.objects.filter(username=user, password=password).first()
        if not user_obj:
            return Response({'code': 1000, 'error': '用户名或密码错误'})

        random_str = str(uuid.uuid4())
        user_obj.token = random_str
        user_obj.save()

        return Response({'code': 1001, 'data': random_str})


class OrderView(APIView):
    def get(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        if not token:
            return Response({'code': 2000, 'error': '登录成功之后才能访问'})

        user_object = UserInfo.objects.filter(token=token).first()
        if not user_object:
            return Response({'code': 2000, 'error': 'token无效'})

        return Response('订单列表')


class ProLoginView(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        user = request.data.get('username')
        password = request.data.get('password')
        user_obj = UserInfo.objects.filter(username=user, password=password).first()
        if not user_obj:
            return Response({'code': 1000, 'error': '用户名或密码错误'})

        token = create_token({"id": user_obj.id, "name": user_obj.username})

        return Response({'code': 1001, 'data': token})


class ProOrderView(APIView):

    def get(self, request, *args, **kwargs):
        print(request.user)
        return Response('订单列表')


