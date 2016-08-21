from modules.db import get_sqlalchemy_db


db = get_sqlalchemy_db()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128))
    password = db.Column(db.String(128))
    jwt = db.Column(db.String(512))
