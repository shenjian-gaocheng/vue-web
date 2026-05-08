from flask_restx import Resource

from extensions import ns
from models import Portrait
from schemas import portrait_model


@ns.route('/portraits')
class PortraitList(Resource):
    @ns.marshal_list_with(portrait_model)
    @ns.doc(security=None)
    def get(self):
        return Portrait.query.all()