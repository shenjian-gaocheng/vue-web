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
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(255))
    cut_url = db.Column(db.String(255))

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
    'cut_url': fields.String(description='cut回放链接')
})

@ns.route('/stages')
class StageList(Resource):
    @ns.marshal_list_with(stage_model)
    def get(self):
        """获取所有演出记录"""
        return Stage.query.all()

    # @ns.expect(stage_model)
    # def post(self):
    #     """添加一条新的演出记录"""
    #     data = request.json
    #     try:
    #         date_obj = datetime.strptime(data['date'], "%Y-%m-%d").date()
    #     except ValueError:
    #         return {"error": "日期格式应为 YYYY-MM-DD"}, 400

    #     stage = Stage(
    #         session=int(data['session']),
    #         date=date_obj,
    #         type=data['type'],
    #         title=data['title'],
    #         url=data['url'],
    #         cut_url=data['cut_url'],
    #     )
    #     db.session.add(stage)
    #     db.session.commit()
    #     return {"message": "演出记录已添加"}, 201
    

# @ns.route('/stages/batch')
# class StageBatch(Resource):
#     @ns.expect([stage_model])  # 注意：接收列表
#     def post(self):
#         """批量添加演出记录"""
#         data_list = request.json

#         if not isinstance(data_list, list):
#             return {"error": "请求体应为 JSON 数组"}, 400

#         stages = []
#         for i, data in enumerate(data_list):
#             try:
#                 date_obj = datetime.strptime(data['date'], "%Y-%m-%d").date()
#                 stage = Stage(
#                     session=int(data['session']),
#                     date=date_obj,
#                     type=data['type'],
#                     title=data['title'],
#                     url=data['url'],
#                     cut_url=data['cut_url'],
#                 )
#                 stages.append(stage)
#             except (KeyError, ValueError) as e:
#                 return {"error": f"第 {i+1} 条数据有误: {str(e)}"}, 400

#         db.session.add_all(stages)
#         db.session.commit()

#         return {"message": f"成功添加 {len(stages)} 条演出记录"}, 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)