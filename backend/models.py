from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from extensions import db


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
    time = db.Column(db.String(255))
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
