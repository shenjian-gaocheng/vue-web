from flask import Flask, request, g, make_response
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # ✅ 导入 CORS
import os
import logging
from datetime import datetime
import requests
import jwt
from functools import wraps
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone


logging.basicConfig(
    filename='stage_actions.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=['https://zty0322.top', 'http://localhost:5173'])
# 信任前 1 层反向代理（如 Nginx）转发的客户端地址
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': '使用格式：Bearer <token>'
    }
}
api = Api(app, prefix="/api", doc='/docs', authorizations=authorizations, security='Bearer Auth')
ns = api.namespace('', description='小周网站后端接口')

# 配置 SQLite 数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zhouty.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret-key'  # 用于生成 JWT Token
app.config['ADMIN_USERS'] = {'zhouty'}
db = SQLAlchemy(app)


def get_client_ip():
    """优先取反向代理头中的真实客户端 IP，最后回退到 remote_addr。"""
    x_forwarded_for = request.headers.get('X-Forwarded-For', '')
    if x_forwarded_for:
        real_ip = x_forwarded_for.split(',')[0].strip()
        if real_ip:
            return real_ip

    x_real_ip = request.headers.get('X-Real-IP', '').strip()
    if x_real_ip:
        return x_real_ip

    return request.remote_addr or 'unknown'

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
    stage_code = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(255))
    cut_url = db.Column(db.String(255))
    time = db.Column(db.String(255)) # 这里time指的是演出地点，而不是时间（使用了原来预留给时间的列）
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

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Text, nullable=False)
    detail = db.Column(db.Text, nullable=False)
    img = db.Column(db.Text, nullable=False)
    is_imp = db.Column(db.Boolean, nullable=False)

class Portrait(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ver_yearmonth = db.Column(db.Integer, nullable=False)
    ver_code = db.Column(db.String(100), nullable=False)
    name = db.Column(db.Text, nullable=False)

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
    'stage_code': fields.String(required=True, description='演出代码'),
    'title': fields.String(required=True, description='演出名称'),
    'url': fields.String(description='完整回放链接'),
    'cut_url': fields.String(description='cut回放链接'),
    'time': fields.String(description='演出地点'),
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

event_model = api.model('Event', {
    'id': fields.String(description='大事记id'),
    'date': fields.String(required=True, description='大事记日期，格式 YYYYMMDD'),
    'title': fields.String(required=True, description='大事记标题'),
    'detail': fields.String(description='大事记详情'),
    'img': fields.String(required=True, description='大事记图片链接'),
    'is_imp': fields.Boolean(required=True, description='是否为重要事件'),
})

portrait_model = api.model('Portrait', {
    'id': fields.String(description='公式照id'),
    'ver_yearmonth': fields.String(required=True, description='公式照版本年月，格式 YYYYMM'),
    'ver_code': fields.String(required=True, description='公式照版本代号'),
    'name': fields.String(required=True, description='公式照名称'),
})

# 登录：设置 HttpOnly Cookie
@ns.route('/login')
class Login(Resource):
    @ns.expect(user_model)
    @ns.doc(security=None)
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return {'message': '用户名或密码错误'}, 401

        expiration = datetime.now(timezone.utc) + timedelta(days=1)
        payload = {'username': username, 'exp': expiration}
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        logging.info(f"用户: {username} 成功登录了系统，IP: {get_client_ip()}")

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


# 验证 token（从 Cookie 读取）
def token_required(f):
    @wraps(f)
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
        return f(*args, **kwargs)
    return decorated


# 验证登录状态
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


# 退出登录：清除 Cookie
@ns.route('/logout')
class Logout(Resource):
    @ns.doc(security=None)
    def post(self):
        resp = make_response({'message': '已退出登录'})
        resp.set_cookie('token_zty', '', httponly=True, secure=True, samesite='Strict', max_age=0)
        return resp


@ns.route('/admin/logs')
class AdminLogs(Resource):
    @token_required
    def get(self):
        if g.username not in app.config['ADMIN_USERS']:
            return {'message': '没有权限访问管理员日志'}, 403

        limit = request.args.get('limit', default=200, type=int)
        if limit is None:
            limit = 200
        limit = max(1, min(limit, 1000))

        log_candidates = [
            '/var/www/vue-web/backend/stage_actions.log',
            os.path.join(os.path.dirname(__file__), 'stage_actions.log')
        ]

        log_path = next((p for p in log_candidates if os.path.exists(p)), None)
        if not log_path:
            return {'message': '找不到日志文件', 'logs': [], 'count': 0}, 404

        matched = []
        try:
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if '用户:' in line:
                        matched.append(line.strip())
        except OSError as e:
            return {'message': f'读取日志失败: {str(e)}', 'logs': [], 'count': 0}, 500

        matched = matched[-limit:]
        return {
            'count': len(matched),
            'limit': limit,
            'log_file': log_path,
            'logs': matched
        }, 200


@ns.route('/teammates')
class TeammateList(Resource):
    @ns.marshal_list_with(teammate_model)
    def get(self):
        """获取所有队友"""
        return Teammate.query.all()
    
    # @ns.expect(teammate_model)
    # @token_required
    # def post(self):
    #     """添加一条新的队友信息"""
    #     data = request.json

    #     def to_bool(val):
    #         if isinstance(val, bool):
    #             return val
    #         if isinstance(val, str):
    #             return val.lower() == 'true'
    #         return False  # 默认 fallback

    #     teammate = Teammate(
    #         snh_id=int(data['snh_id']),
    #         name=data['name'],
    #         is_teamsii=to_bool(data['is_teamsii']),
    #         is_teamnew=to_bool(data['is_teamnew']),
    #         is_active=to_bool(data['is_active']),
    #         url=data['url'],
    #         note=data['note'],
    #     )
    #     db.session.add(teammate)
    #     db.session.commit()

    #     logging.info(f"用户: {g.username} 添加队友记录: {data['name']}，IP: {request.remote_addr}")
    #     return {"message": "队友记录已添加"}, 201
    

# @ns.route('/teammates/batch')
# class TeammateBatch(Resource):
#     @ns.expect([teammate_model])  # 注意：接收列表
#     @token_required
#     def post(self):
#         """批量添加演出记录"""
#         data_list = request.json

#         def to_bool(val):
#             if isinstance(val, bool):
#                 return val
#             if isinstance(val, str):
#                 return val.lower() == 'true'
#             return False  # 默认 fallback

#         teammates = []
#         for i, data in enumerate(data_list):
#             try:
#                 teammate = Teammate(
#                     snh_id=int(data['snh_id']),
#                     name=data['name'],
#                     is_teamsii=to_bool(data['is_teamsii']),
#                     is_teamnew=to_bool(data['is_teamnew']),
#                     is_active=to_bool(data['is_active']),
#                     url=data['url'],
#                     note=data['note'],
#                 )
#                 teammates.append(teammate)
#             except (KeyError, ValueError) as e:
#                 return {"error": f"第 {i+1} 条数据有误: {str(e)}"}, 400

#         db.session.add_all(teammates)
#         db.session.commit()

#         logging.info(f"用户: {g.username} 添加 {len(teammates)} 条队友记录，IP: {request.remote_addr}")
#         return {"message": f"成功添加 {len(teammates)} 条队友记录"}, 201

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
            stage_code=data['stage_code'],
            title=data['title'],
            url=data['url'],
            cut_url=data['cut_url'],
            time=data['time'],
            is_stage=data['is_stage'],
            is_end=data['is_end'],
        )
        db.session.add(stage)
        db.session.commit()

        logging.info(f"用户: {g.username} 添加演出记录: {data['session']} {data['title']}，IP: {get_client_ip()}")
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
            stage.stage_code = data['stage_code']
            stage.title = data['title']
            stage.url = data['url']
            stage.cut_url = data['cut_url']
            stage.time = data['time']
            stage.is_stage = data['is_stage']
            stage.is_end = data['is_end']

            db.session.commit()

            logging.info(f"用户: {g.username} 更新演出记录: {data['session']} {data['title']}，IP: {get_client_ip()}")
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
                    stage_code=data['stage_code'],
                    title=data['title'],
                    url=data['url'],
                    cut_url=data['cut_url'],
                    is_stage=data['is_stage'],
                    is_end=data['is_end'],
                    time=data['time'],
                )
                stages.append(stage)
            except (KeyError, ValueError) as e:
                return {"error": f"第 {i+1} 条数据有误: {str(e)}"}, 400

        db.session.add_all(stages)
        db.session.commit()

        logging.info(f"用户: {g.username} 添加 {len(stages)} 条演出记录，IP: {get_client_ip()}")
        return {"message": f"成功添加 {len(stages)} 条演出记录"}, 201

@ns.route('/events')
class EventList(Resource):
    @ns.marshal_list_with(event_model)
    @ns.doc(security=None)
    def get(self):
        """获取所有大事记记录"""
        return Event.query.all()
    
@ns.route('/portraits')
class PortraitList(Resource):
    @ns.marshal_list_with(portrait_model)
    @ns.doc(security=None)
    def get(self):
        """获取所有公式照记录"""
        return Portrait.query.all()
    
# 健康检查接口
@ns.route('/health')
class Health(Resource):
    @ns.doc(security=None)
    def get(self):
        """检查API和数据库连接状态"""
        try:
            db.session.execute(db.text('SELECT 1'))
            return {'status': 'ok', 'db': 'connected'}
        except Exception as e:
            return {'status': 'error', 'db': str(e)}, 500

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=False)
    # app.run(host="0.0.0.0", port=5000, debug=False)