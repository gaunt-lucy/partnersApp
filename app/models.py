from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    passwordhash = db.Column(db.String(128))
    collabs = db.relationship('Collaboration', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)    

class Partner(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True)
	ptype = db.Column(db.String(128))
	city = db.Column(db.String(128))
	country = db.Column(db.String(128))
	contact = db.Column(db.String(128))
	owner = db.Column(db.Integer, db.ForeignKey('user.id'))
	created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

	def __repr__(self):
		return '<Partner: {}>'.format(self.name)    