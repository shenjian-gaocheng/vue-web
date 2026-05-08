import os

from flask import g
from flask import request
from flask_restx import Resource

from auth_utils import token_required
from extensions import BASE_DIR, app, ns


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
            os.path.join(BASE_DIR, 'stage_actions.log')
        ]

        log_path = next((path for path in log_candidates if os.path.exists(path)), None)
        if not log_path:
            return {'message': '找不到日志文件', 'logs': [], 'count': 0}, 404

        matched = []
        try:
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line in file:
                    if '用户:' in line:
                        matched.append(line.strip())
        except OSError as error:
            return {'message': f'读取日志失败: {str(error)}', 'logs': [], 'count': 0}, 500

        matched = matched[-limit:]
        return {
            'count': len(matched),
            'limit': limit,
            'log_file': log_path,
            'logs': matched
        }, 200