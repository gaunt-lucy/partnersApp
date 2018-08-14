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
	reports = db.relationship('Report', backref='report_author', lazy='dynamic')

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
	last_updated = db.Column(db.Date, index=True)
	updated_by = db.Column(db.Integer)
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
	author = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Report: {}>'.format(self.content)

class Mobility(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	agreement = db.Column(db.Integer, db.ForeignKey('agreement.id'))
	mobilitytype = db.Column(db.String, db.ForeignKey('agree_type.code'))
	partner = db.Column(db.Integer, db.ForeignKey('partner.id'))
	level = db.Column(db.String)
	session = db.Column(db.Integer)
	#direction = db.Column(db.String)
	totalout = db.Column(db.Float)
	totalin = db.Column(db.Float)

class Country(db.Model):
	iso = db.Column(db.String, primary_key=True)
	name = db.Column(db.String)

	@staticmethod
	def insert_countries():
		countryvals = [('AF', 'Afghanistan'), ('AX', 'Aland Islands'), ('AL', 'Albania'), ('DZ', 'Algeria'), \
		('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'), \
		('AG', 'Antigua and Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'), \
		('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), \
		('BY', 'Belarus'), ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BT', 'Bhutan'), \
		('BO', 'Bolivia'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BV', 'Bouvet Island'), ('BR', 'Brazil'), \
		('VG', 'British Virgin Islands'), ('IO', 'British Indian Ocean Territory'), ('BN', 'Brunei Darussalam'), \
		('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), \
		('CA', 'Canada'), ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), \
		('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('HK', 'Hong Kong, SAR China'), ('MO', 'Macao, SAR China'), \
		('CX', 'Christmas Island'), ('CC', 'Cocos (Keeling) Islands'), ('CO', 'Colombia'), ('KM', 'Comoros'), \
		('CG', 'Congo (Brazzaville)'), ('CD', 'Congo, (Kinshasa)'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), \
		('CI', 'Côte dIvoire'), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), \
		('DK', 'Denmark'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), \
		('EG', 'Egypt'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'), \
		('ET', 'Ethiopia'), ('FK', 'Falkland Islands (Malvinas)'), ('FO', 'Faroe Islands'), ('FJ', 'Fiji'), ('FI', 'Finland'), \
		('FR', 'France'), ('GF', 'French Guyana'), ('PF', 'French Polynesia'), ('TF', 'French Southern Territories'), ('GA', 'Gabon'), \
		('GM', 'Gambia'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GR', 'Greece'), ('GL', 'Greenland'), \
		('GD', 'Grenada'), ('GP', 'Guadeloupe'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GG', 'Guernsey'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), \
		('GY', 'Guyana'), ('HT', 'Haiti'), ('HM', 'Heard and Mcdonald Islands'), ('VA', 'Holy See (Vatican City State)'), ('HN', 'Honduras'), \
		('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran, Islamic Republic of'), ('IQ', 'Iraq'), \
		('IE', 'Ireland'), ('IM', 'Isle of Man'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'), ('JP', 'Japan'), ('JE', 'Jersey'), \
		('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KI', 'Kiribati'), ('KP', 'Korea (North)'), ('KR', 'Korea (South)'), \
		('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', 'Lao PDR'), ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'), \
		('LY', 'Libya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MK', 'Macedonia, Republic of'), \
		('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MH', 'Marshall Islands'), \
		('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('YT', 'Mayotte'), ('MX', 'Mexico'), ('FM', 'Micronesia, Federated States of'), \
		('MD', 'Moldova'), ('MC', 'Monaco'), ('MN', 'Mongolia'), ('ME', 'Montenegro'), ('MS', 'Montserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), \
		('MM', 'Myanmar'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('AN', 'Netherlands Antilles'), \
		('NC', 'New Caledonia'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'), \
		('NF', 'Norfolk Island'), ('MP', 'Northern Mariana Islands'), ('NO', 'Norway'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PW', 'Palau'), \
		('PS', 'Palestinian Territory'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), \
		('PN', 'Pitcairn'), ('PL', 'Poland'), ('PT', 'Portugal'), ('PR', 'Puerto Rico'), ('QA', 'Qatar'), ('RE', 'Réunion'), ('RO', 'Romania'), \
		('RU', 'Russian Federation'), ('RW', 'Rwanda'), ('BL', 'Saint-Barthélemy'), ('SH', 'Saint Helena'), ('KN', 'Saint Kitts and Nevis'), \
		('LC', 'Saint Lucia'), ('MF', 'Saint-Martin (French part)'), ('PM', 'Saint Pierre and Miquelon'), ('VC', 'Saint Vincent and Grenadines'), \
		('WS', 'Samoa'), ('SM', 'San Marino'), ('ST', 'Sao Tome and Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'), ('RS', 'Serbia'), \
		('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), \
		('SO', 'Somalia'), ('ZA', 'South Africa'), ('GS', 'South Georgia and the South Sandwich Islands'), ('SS', 'South Sudan'), \
		('ES', 'Spain'), ('LK', 'Sri Lanka'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SJ', 'Svalbard and Jan Mayen Islands'), \
		('SZ', 'Swaziland'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SY', 'Syrian Arab Republic (Syria)'), ('TW', 'Taiwan, Republic of China'), \
		('TJ', 'Tajikistan'), ('TZ', 'Tanzania, United Republic of'), ('TH', 'Thailand'), ('TL', 'Timor-Leste'), ('TG', 'Togo'), \
		('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), \
		('TC', 'Turks and Caicos Islands'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'), \
		('GB', 'United Kingdom'), ('US', 'United States of America'), ('UM', 'US Minor Outlying Islands'), ('UY', 'Uruguay'), \
		('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VE', 'Venezuela (Bolivarian Republic)'), ('VN', 'Viet Nam'), \
		('VI', 'Virgin Islands, US'), ('WF', 'Wallis and Futuna Islands'), ('EH', 'Western Sahara'), ('YE', 'Yemen'), \
		('ZM', 'Zambia'), ('ZW', 'Zimbabwe')]

		for c in countryvals:
			country = Country.query.filter_by(iso=c[0]).first()
			if country is None:
				country = Country(iso=c[0])
			country.name = c[1]
			db.session.add(country)
		db.session.commit()

class OrgType(db.Model):
	code = db.Column(db.String, primary_key=True)
	name = db.Column(db.String)

	@staticmethod
	def add_types():
		types = [('HEI', 'University'), ('NGO', 'Non-government organisation'), ('RES', 'Research centre'), ('GOV', 'Government organisation')]
		for t in types:
			orgtype = OrgType.query.filter_by(code=t[0]).first()
			if orgtype is None:
				orgtype = OrgType(code=t[0])
			orgtype.name = t[1]
			db.session.add(orgtype)
		db.session.commit()

class AgreeType(db.Model):
	code = db.Column(db.String, primary_key=True)
	name = db.Column(db.String)
	mobility = db.relationship('Mobility', backref='mobility_type', lazy='dynamic')

	@staticmethod
	def add_types():
		types = [('STUX', 'Student exchange'), ('STAX', 'Staff exchange'), \
		('RESE', 'Research collaboration'), ('GOVE', 'Government organisation'), \
		('ERAS', 'Erasmus student exchange'), ('ERST', 'Erasmus staff exchange')]

		for t in types:
			agreetype = AgreeType.query.filter_by(code=t[0]).first()
			if agreetype is None:
				agreetype = AgreeType(code=t[0])
			agreetype.name = t[1]
			db.session.add(agreetype)
		db.session.commit()