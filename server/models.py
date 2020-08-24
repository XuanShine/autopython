from . import db

class RaspberryPi(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    ip_address = db.Column(db.String(128))