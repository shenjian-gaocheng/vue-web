from functools import wraps

from flask import g, request
import jwt

from extensions import app


def get_client_ip():
    x_forwarded_for = request.headers.get('X-Forwarded-For', '')
    if x_forwarded_for:
        real_ip = x_forwarded_for.split(',')[0].strip()
        if real_ip:
            return real_ip

    x_real_ip = request.headers.get('X-Real-IP', '').strip()
    if x_real_ip:
        return x_real_ip

    return request.remote_addr or 'unknown'


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token_zty')
        if not token:
            return {'message': '未登录或会话已过期'}, 401
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            g.username = payload.get('username')
        except jwt.ExpiredSignatureError:
            return {'message': 'Token已过期'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Token无效'}, 401
        return func(*args, **kwargs)

    return decorated
