import unittest
from datetime import datetime, timedelta
from app import app, db
from app.models import User, Partner, Agreement

class TestUserModel(unittest.TestCase):
	def setUpEnv(self):
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def TestPasswordHash(self):
		u = User(userid='Olivia')
		u.set_password('cat')
		self.assertFalse(u.check_password('dog'))
		self.assertTrue(u.cehck_password('cat'))

	