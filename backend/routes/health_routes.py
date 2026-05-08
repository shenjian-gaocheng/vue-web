from flask_restx import Resource

from extensions import db, ns


@ns.route('/health')
class Health(Resource):
    @ns.doc(security=None)
    def get(self):
        try:
            db.session.execute(db.text('SELECT 1'))
            return {'status': 'ok', 'db': 'connected'}
        except Exception as error:
            return {'status': 'error', 'db': str(error)}, 500