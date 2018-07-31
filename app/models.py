from app import db, login
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash #password hash function provided by Werkzeug package (Flask dependency)
from flask_login import UserMixin #implements required methods and properties for flask_login to work with the User model


class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.String(64), index=True, unique=True)
	fname = db.Column(db.String(64), index=True)
	sname = db.Column(db.String(64), index=True)
	email = db.Column(db.String(120), index=True, unique=True)
	#role = db.Column(db.Integer, db.ForeignKey('role.id'))
	passwordhash = db.Column(db.String(128))
	collabs = db.relationship('Partner', backref='col_owner', lazy='dynamic')

	def __repr__(self):
		return '<User {}>'.format(self.fname)

	def set_password(self, password):
		self.passwordhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.passwordhash, password)

	@login.user_loader
	def load_user(id):
		return User.query.get(int(id))

class Partner(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), index=True, unique=True)
	offname = db.Column(db.String(80), index=True)
	ptype = db.Column(db.String(128))
	city = db.Column(db.String(128))
	country = db.Column(db.String(128))
	contact = db.Column(db.String(64))
	owner = db.Column(db.Integer, db.ForeignKey('user.id'))
	created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	agreement = db.relationship('Agreement', backref='partner_org', lazy='dynamic')
	visit = db.relationship('Visit', backref='visit_ref', lazy='dynamic')

	def __repr__(self):
		return '<Partner: {}>'.format(self.name)

class Agreement(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	partner = db.Column(db.Integer, db.ForeignKey('partner.id'))
	atype = db.Column(db.String(64))
	level = db.Column(db.String(64))
	start_date = db.Column(db.Date, index=True)
	end_date = db.Column(db.Date, index=True)

	def __repr__(self):
		return '<Agreement no: {}>'.format(self.id)

class Visit(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	partner = db.Column(db.Integer, db.ForeignKey('partner.id'))
	vtype = db.Column(db.String(64))
	start_date = db.Column(db.Date, index=True)
	end_date = db.Column(db.Date, index=True)
	status = db.Column(db.String)
	report = db.relationship('Report', backref='visit_report', lazy='dynamic')

	def __repr__(self):
		return '<Visit report no: {}>'.format(self.id)


class Report(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String)
	visit_id = db.Column(db.Integer, db.ForeignKey('visit.id'))

	def __repr__(self):
		return '<Report: {}>'.format(self.content)
	