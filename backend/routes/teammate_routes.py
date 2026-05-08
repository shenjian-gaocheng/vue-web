from flask_restx import Resource

from extensions import ns
from models import Teammate
from schemas import teammate_model


@ns.route('/teammates')
class TeammateList(Resource):
    @ns.marshal_list_with(teammate_model)
    def get(self):
        return Teammate.query.all()