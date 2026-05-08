from flask_restx import fields

from extensions import api


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

knowledge_chat_model = api.model('KnowledgeChatRequest', {
    'question': fields.String(required=True, description='用户问题'),
    'top_k': fields.Integer(required=False, description='最多召回的知识片段数，默认 5'),
})
