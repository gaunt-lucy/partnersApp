import unittest
from datetime import datetime, timedelta
from app import app, db
from app.models import User, Partner, Agreement

class TestUserModel(unittest.TestCase):
	def setUp(self):
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_password(self):
		u = User(userid='Olivia')
		u.set_password('cat')
		self.assertFalse(u.check_password('dog'))
		self.assertTrue(u.check_password('cat'))


class TestAddData(unittest.TestCase):
	def setUp(self):
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_partner(self):
		now = datetime.utcnow()
		p1 = Partner(id=1, name='University of Somewhere', ptype='HEI', city='Gotham',\
			owner='Lucy')
		p2 = Partner(id=2, name='University of Other', ptype='HEI', city='Oz',\
			owner='Jim', created_date=now)
		db.session.add(p1)
		db.session.add(p2)
		db.session.commit()
		m1 = Partner.query.filter_by(name=p1.name).first()
		m2 = Partner.query.filter_by(name=p2.name).first()

		self.assertEqual(p1, m1)
		self.assertEqual(p2, m2)

	def test_agreement(self):
		a1 = Agreement(id=1, partner='1', atype='EXCH')
		a2 = Agreement(id=2, partner='2', atype='GOVE')
		db.session.add(a1)
		db.session.add(a2)
		db.session.commit()
		m1 = Partner.query.filter_by(id=a1.id).first()
		m2 = Partner.query.filter_by(id=a2.id).first()

if __name__ == '__main__':
    unittest.main(verbosity=2)