from modules.db import create_connecter
from conf import settings


db = create_connecter(**settings['database'])


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128))
    password = db.Column(db.String(128))
    jwt = db.Column(db.String(512))
    github_sid = db.Column(db.String(128))
    github_access_token = db.Column(db.String(256)) 
