import models  # noqa: F401 — registers SQLAlchemy models before db.create_all()
from extensions import app, db

from routes import admin_routes
from routes import auth_routes
from routes import event_routes
from routes import health_routes
from routes import knowledge_routes
from routes import portrait_routes
from routes import stage_routes
from routes import teammate_routes


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)