from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # ✅ 导入 CORS
from datetime import datetime
import requests

app = Flask(__name__)
CORS(app)
api = Api(app, doc='/docs')
ns = api.namespace('api', description='周童玥网站接口')

# 配置 SQLite 数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zhouty.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 定义数据模型
class Stage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(255))
    cut_url = db.Column(db.String(255))
    is_stage = db.Column(db.Boolean, nullable=False)
    is_end = db.Column(db.Boolean, nullable=False)


class Teammate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    snh_id = db.Column(db.Integer)
    name = db.Column(db.String(100), nullable=False)
    is_teamsii = db.Column(db.Boolean, nullable=False)
    is_teamnew = db.Column(db.Boolean, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    url = db.Column(db.String(255))
    note = db.Column(db.String(255))

# 自动创建表
with app.app_context():
    db.create_all()

# 定义用于 Swagger 的模型（用于输入验证 & 文档）
stage_model = api.model('Stage', {
    'session': fields.String(required=True, description='演出场次'),
    'date': fields.String(required=True, description='演出日期，格式 YYYY-MM-DD'),
    'type': fields.String(required=True, description='演出类型'),
    'title': fields.String(required=True, description='演出名称'),
    'url': fields.String(description='完整回放链接'),
    'cut_url': fields.String(description='cut回放链接'),
    'is_stage': fields.Boolean(required=True, description='是否为公演'),
    'is_end': fields.Boolean(required=True, description='是否结束'),
})

teammate_model = api.model('Teammate', {
    'snh_id': fields.String(required=True, description='SNH48官网id'),
    'name': fields.String(required=True, description='姓名'),
    'is_teamsii': fields.Boolean(required=True, description='是否为s队成员'),
    'is_teamnew': fields.Boolean(required=True, description='是否为新生'),
    'is_active': fields.Boolean(required=True, description='是否活跃'),
    'url': fields.String(description='预留链接'),
    'note': fields.String(description='备注')
})

@ns.route('/teammates')
class TeammateList(Resource):
    @ns.marshal_list_with(teammate_model)
    def get(self):
        """获取所有队友"""
        return Teammate.query.all()

@ns.route('/stages')
class StageList(Resource):
    @ns.marshal_list_with(stage_model)
    def get(self):
        """获取所有演出记录"""
        return Stage.query.all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)