import logging
import os

from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix


logging.basicConfig(
    filename='stage_actions.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=['https://zty0322.top', 'http://localhost:5173'])
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zhouty.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret-key'
app.config['ADMIN_USERS'] = {'zhouty'}

db = SQLAlchemy(app)

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': '使用格式：Bearer <token>'
    }
}
api = Api(app, prefix='/api', doc='/docs', authorizations=authorizations, security='Bearer Auth')
ns = api.namespace('', description='小周网站后端接口')
