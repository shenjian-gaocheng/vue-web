from flask_restx import Resource

from extensions import ns
from models import Event
from schemas import event_model


@ns.route('/events')
class EventList(Resource):
    @ns.marshal_list_with(event_model)
    @ns.doc(security=None)
    def get(self):
        return Event.query.all()