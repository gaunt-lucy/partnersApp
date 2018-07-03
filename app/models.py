from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash #password hash function provided by Werkzeug package (Flask dependency)
from flask_login import UserMixin #implements required methods and properties for flask_login to work with the User model

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	passwordhash = db.Column(db.String(128))
	collabs = db.relationship('Partner', backref='col_owner', lazy='dynamic')

	def __repr__(self):
		return '<User {}>'.format(self.userid)

	def set_password(self, password):
		self.passwordhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.passwordhash, password)

class Partner(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True)
	ptype = db.Column(db.String(128))
	city = db.Column(db.String(128))
	country = db.Column(db.String(128))
	contact = db.Column(db.String(128))
	owner = db.Column(db.Integer, db.ForeignKey('user.id'))
	#created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

	def __repr__(self):
		return '<Partner: {}>'.format(self.name)