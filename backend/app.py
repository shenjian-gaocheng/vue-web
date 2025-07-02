from flask import Flask, request, g
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # ✅ 导入 CORS
import logging
from datetime import datetime
import requests
import jwt
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone


logging.basicConfig(
    filename='stage_actions.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

app = Flask(__name__)
CORS(app, supports_credentials=True)

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': '使用格式：Bearer <token>'
    }
}
api = Api(app, prefix="/api", doc='/api/docs', authorizations=authorizations, security='Bearer Auth')
ns = api.namespace('', description='明星接口')

# 配置 SQLite 数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zhouty.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret-key'  # 用于生成 JWT Token
db = SQLAlchemy(app)

# 定义数据模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Stage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(100), nullable=False)
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
user_model = api.model('User', {
    'username': fields.String(required=True, description='用户名'),
    'password': fields.String(required=True, description='密码'),
})

stage_model = api.model('Stage', {
    'id': fields.String(description='演出id'),
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

# 登录并返回token
@ns.route('/login')
class Login(Resource):
    @ns.expect(user_model)
    @ns.doc(security=None)
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')  # 明文密码
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hash, password):
            return {'message': '用户名或密码错误'}, 401

        # 设置过期时间为1小时
        expiration = datetime.now(timezone.utc) + timedelta(days=1)
        payload = {
            'username': username,
            'exp': expiration
        }

        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        logging.info(f"用户: {username} 成功登录了系统，IP: {request.remote_addr}")
        return {'token': token}
    

# 验证token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return {'message': '缺少或格式错误的Token'}, 401

        token = auth_header.split(' ')[1]  # 提取 "Bearer token" 的 token 部分

        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            g.username = payload.get("username")

            # ✅ 打印调试 token 过期时间
            print("exp时间戳：", payload['exp'])
            print("过期时间：", datetime.fromtimestamp(payload['exp'], tz=timezone.utc))
        except jwt.ExpiredSignatureError:
            return {'message': 'Token已过期'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Token无效'}, 401

        return f(*args, **kwargs)
    return decorated

# 验证token
@ns.route('/verify')
class TokenVerify(Resource):
    @token_required
    def get(self):
        return {'message': 'Token 有效'}, 200


@ns.route('/teammates')
class TeammateList(Resource):
    @ns.marshal_list_with(teammate_model)
    def get(self):
        """获取所有队友"""
        return Teammate.query.all()
    
    @ns.expect(teammate_model)
    @token_required
    def post(self):
        """添加一条新的队友信息"""
        data = request.json

        def to_bool(val):
            if isinstance(val, bool):
                return val
            if isinstance(val, str):
                return val.lower() == 'true'
            return False  # 默认 fallback

        teammate = Teammate(
            snh_id=int(data['snh_id']),
            name=data['name'],
            is_teamsii=to_bool(data['is_teamsii']),
            is_teamnew=to_bool(data['is_teamnew']),
            is_active=to_bool(data['is_active']),
            url=data['url'],
            note=data['note'],
        )
        db.session.add(teammate)
        db.session.commit()

        logging.info(f"用户: {g.username} 添加队友记录: {data['name']}，IP: {request.remote_addr}")
        return {"message": "队友记录已添加"}, 201
    

@ns.route('/teammates/batch')
class TeammateBatch(Resource):
    @ns.expect([teammate_model])  # 注意：接收列表
    @token_required
    def post(self):
        """批量添加演出记录"""
        data_list = request.json

        def to_bool(val):
            if isinstance(val, bool):
                return val
            if isinstance(val, str):
                return val.lower() == 'true'
            return False  # 默认 fallback

        teammates = []
        for i, data in enumerate(data_list):
            try:
                teammate = Teammate(
                    snh_id=int(data['snh_id']),
                    name=data['name'],
                    is_teamsii=to_bool(data['is_teamsii']),
                    is_teamnew=to_bool(data['is_teamnew']),
                    is_active=to_bool(data['is_active']),
                    url=data['url'],
                    note=data['note'],
                )
                teammates.append(teammate)
            except (KeyError, ValueError) as e:
                return {"error": f"第 {i+1} 条数据有误: {str(e)}"}, 400

        db.session.add_all(teammates)
        db.session.commit()

        logging.info(f"用户: {g.username} 添加 {len(teammates)} 条队友记录，IP: {request.remote_addr}")
        return {"message": f"成功添加 {len(teammates)} 条队友记录"}, 201

@ns.route('/stages')
class StageList(Resource):
    @ns.marshal_list_with(stage_model)
    @ns.doc(security=None)
    def get(self):
        """获取所有演出记录"""
        return Stage.query.all()

    @ns.expect(stage_model)
    @token_required
    def post(self):
        """添加一条新的演出记录"""
        data = request.json
        # try:
        #     date_obj = datetime.strptime(data['date'], "%Y-%m-%d").date()
        # except ValueError:
        #     return {"error": "日期格式应为 YYYY-MM-DD"}, 400

        stage = Stage(
            session=int(data['session']),
            date=data['date'],
            type=data['type'],
            title=data['title'],
            url=data['url'],
            cut_url=data['cut_url'],
            is_stage=data['is_stage'],
            is_end=data['is_end'],
        )
        db.session.add(stage)
        db.session.commit()

        logging.info(f"用户: {g.username} 添加演出记录: {data['session']}，IP: {request.remote_addr}")
        return {"message": "演出记录已添加"}, 201
    

@ns.route('/stages/<int:id>')
class StageItem(Resource):
    @ns.expect(stage_model)
    @token_required
    def put(self, id):
        """更新特定 ID 的演出记录"""
        data = request.json
        stage = db.session.get(Stage, id)

        if not stage:
            return {"error": "找不到该演出记录"}, 404

        try:
            stage.session = int(data['session'])
            stage.date = data['date']
            stage.type = data['type']
            stage.title = data['title']
            stage.url = data['url']
            stage.cut_url = data['cut_url']
            stage.is_stage = data['is_stage']
            stage.is_end = data['is_end']

            db.session.commit()

            logging.info(f"用户: {g.username} 更新演出记录: {data['session']}，IP: {request.remote_addr}")
            return {"message": "演出记录已更新"}, 200
        except (KeyError, ValueError) as e:
            print(str(e))
            return {"error": f"更新失败: {str(e)}"}, 400
    

@ns.route('/stages/batch')
class StageBatch(Resource):
    @ns.expect([stage_model])  # 注意：接收列表
    @token_required
    def post(self):
        """批量添加演出记录"""
        data_list = request.json

        if not isinstance(data_list, list):
            return {"error": "请求体应为 JSON 数组"}, 400

        stages = []
        for i, data in enumerate(data_list):
            try:
                date_obj = datetime.strptime(data['date'], "%Y-%m-%d").date()
                stage = Stage(
                    session=int(data['session']),
                    date=date_obj,
                    type=data['type'],
                    title=data['title'],
                    url=data['url'],
                    cut_url=data['cut_url'],
                    is_stage=data['is_stage'],
                    is_end=data['is_end'],
                )
                stages.append(stage)
            except (KeyError, ValueError) as e:
                return {"error": f"第 {i+1} 条数据有误: {str(e)}"}, 400

        db.session.add_all(stages)
        db.session.commit()

        logging.info(f"用户: {g.username} 添加 {len(stages)} 条演出记录，IP: {request.remote_addr}")
        return {"message": f"成功添加 {len(stages)} 条演出记录"}, 201


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=False)