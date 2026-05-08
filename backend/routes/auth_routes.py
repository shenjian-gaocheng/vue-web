from datetime import datetime
from datetime import timedelta
from datetime import timezone

import jwt
import logging
from flask import make_response
from flask import request
from flask_restx import Resource

from auth_utils import get_client_ip
from extensions import app, ns
from models import User
from schemas import user_model


@ns.route('/login')
class Login(Resource):
    @ns.expect(user_model)
    @ns.doc(security=None)
    def post(self):
        data = request.json or {}
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return {'message': '用户名或密码错误'}, 401

        expiration = datetime.now(timezone.utc) + timedelta(days=1)
        payload = {'username': username, 'exp': expiration}
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        logging.info(f'用户: {username} 成功登录了系统，IP: {get_client_ip()}')

        resp = make_response({'message': '登录成功'})
        resp.set_cookie(
            'token_zty',
            token,
            httponly=True,
            secure=True,
            samesite='Strict',
            max_age=86400
        )
        return resp


@ns.route('/verify')
class TokenVerify(Resource):
    @ns.doc(security=None)
    def get(self):
        token = request.cookies.get('token_zty')
        if not token:
            return {'message': '未登录'}, 401
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            return {'message': 'Token有效'}, 200
        except jwt.ExpiredSignatureError:
            return {'message': 'Token已过期'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Token无效'}, 401


@ns.route('/logout')
class Logout(Resource):
    @ns.doc(security=None)
    def post(self):
        resp = make_response({'message': '已退出登录'})
        resp.set_cookie('token_zty', '', httponly=True, secure=True, samesite='Strict', max_age=0)
        return resp