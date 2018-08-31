from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, PasswordField, BooleanField, SubmitField, SelectField, FloatField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Optional, InputRequired
from wtforms.fields.html5 import DateField
from app.models import User, Partner

class LoginForm(FlaskForm):
	userid = StringField('User ID', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Log in')

class RegistrationForm(FlaskForm):
	#userid = StringField('User ID', validators=[DataRequired()])
	fname = StringField('First name', validators=[DataRequired()])
	sname = StringField('Surname', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Re-enter password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

## is this still in use? 
	def validate_userid(self, userid):
		user = User.query.filter_by(userid=userid.data).first()
		if user is not None:
			raise ValidationError('Please choose a different userid.')
## is this still in use?
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Email address is already registered.')

class RequestResetPasswordForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Request password reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class NewPartnerForm(FlaskForm):
	typechoices = [('HEI', 'University'), ('NGO', 'Non-government organisation'), ('RES', 'Research centre'), ('GOV', 'Government organisation')]

	name = StringField('Partner name', validators=[DataRequired()])
	offname = StringField('Official name', validators=[DataRequired()])
	ptype = SelectField(u'Organisation type', choices=typechoices, validators=[DataRequired()])
	country = SelectField(u'Country', validators=[DataRequired()])
	city = StringField('Town/city', validators=[DataRequired()])
	submit = SubmitField('Add new partner')


class AddAgreementForm(FlaskForm):
	# partners = Partner.query.all()
	# name = []
	# ids = []
	# for p in partners:
	# 	name.append(p.name)
	# 	ids.append(str(p.id))
	# partners = zip(ids, name)


	typechoices = [('Student exchange', 'Student exchange'), ('STAX', 'Staff exchange'), \
	('RESE', 'Research collaboration'), ('GOVE', 'Government organisation'), \
	('ERAS', 'Erasmus student exchange'), ('ERST', 'Erasmus staff exchange')]

	#selectPartner = SelectField(u'Partner organisation', validators=[DataRequired()])
	atype = SelectField(u'Agreement type', choices=typechoices, validators=[DataRequired()])
	startdate = DateField(u'Select start date')
	enddate = DateField(u'Select end date')
	submit = SubmitField('Add new agreement')

class EnterMobility(FlaskForm):
	# typechoices = [('STUX', 'Student exchange'), ('STAX', 'Staff exchange'), \
	# ('RESE', 'Research collaboration'), ('GOVE', 'Government organisation'), \
	# ('ERAS', 'Erasmus student exchange'), ('ERST', 'Erasmus staff exchange')]

	yearoption = [('2010', '2010/11'), ('2011', '2011/12'), ('2012', '2012/13'), ('2013', '2013/14'), ('2014', '2014/15'), \
	('2015', '2015/16'), ('2016', '2016/17'), ('2017', '2017/18'), ('2018', '2018/19')]

	typelevel = [('Undergraduate', 'Undergraduate'), ('Postgraduate Taught', 'Postgraduate Taught'), ('Postgraduate Research', 'Postgraduate Research'), \
	('Academic staff', 'Academic staff'), ('Professional services staff', 'Professional services staff')]

	def validate_total(form, field):
		if field.data%0.5 != 0:
			raise ValidationError('Partial mobilities may not be more or less than 0.5FTE - please adjust total.')
	session = SelectField(u'Select session', choices=yearoption, validators=[DataRequired()])
	mobilitytype = SelectField(u'Mobility type', validators=[DataRequired()])
	#agreement = SelectField(u'Agreement (if relevant)', coerce=int, validators=[Optional()])
	level = SelectField(u'Select type/level', choices=typelevel, validators=[DataRequired()])
	totalout = FloatField(u'Enter total outbound mobilities (in FTE)', validators=[InputRequired(), validate_total])
	totalin = FloatField(u'Enter total inbound mobilities (in FTE)', validators=[InputRequired(), validate_total])
	submit = SubmitField('Add mobilities')

class AddVisit(FlaskForm):
	typechoices = [('Research', 'Research (inc. conferences)'), ('Monitoring', 'Mobility monitoring'), \
	('Institutional', 'Institutional visit'), ('Other', 'Other')]

	start_date = DateField('Visit start date', validators=[DataRequired()])
	end_date = DateField('Visit end date', validators=[DataRequired()])
	vtype = SelectField(u'Visit type', choices=typechoices, validators=[DataRequired()])
	#leadcontact = StringField('Lead contact name', validators=[DataRequired()])
	#report = StringField('Visit report', validators=[DataRequired()])

	submit = SubmitField('Add visit')

class AddVisitReport(FlaskForm):

	report = TextAreaField('Enter visit report', render_kw={"rows":20, "cols": 8})

	submit = SubmitField('Add visit')

class SearchForm(FlaskForm):
	
	text_search = StringField('Search by organisation name', validators=[Optional()])
	search = SubmitField('Search')
	
# class BrowseForm(FlaskForm):

# 	typechoices = [('',''),('HEI', 'University'), ('NGO', 'Non-government organisation'), ('RES', 'Research centre'), ('GOV', 'Government organisation')]
# 	countrychoices = [('',''),('AF', 'Afghanistan'), ('AX', 'Aland Islands'), ('AL', 'Albania'), ('DZ', 'Algeria'), \
# 	('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'), \
# 	('AG', 'Antigua and Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'), \
# 	('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), \
# 	('BY', 'Belarus'), ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BT', 'Bhutan'), \
# 	('BO', 'Bolivia'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BV', 'Bouvet Island'), ('BR', 'Brazil'), \
# 	('VG', 'British Virgin Islands'), ('IO', 'British Indian Ocean Territory'), ('BN', 'Brunei Darussalam'), \
# 	('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), \
# 	('CA', 'Canada'), ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), \
# 	('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('HK', 'Hong Kong, SAR China'), ('MO', 'Macao, SAR China'), \
# 	('CX', 'Christmas Island'), ('CC', 'Cocos (Keeling) Islands'), ('CO', 'Colombia'), ('KM', 'Comoros'), \
# 	('CG', 'Congo (Brazzaville)'), ('CD', 'Congo, (Kinshasa)'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), \
# 	('CI', 'Côte dIvoire'), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), \
# 	('DK', 'Denmark'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), \
# 	('EG', 'Egypt'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'), \
# 	('ET', 'Ethiopia'), ('FK', 'Falkland Islands (Malvinas)'), ('FO', 'Faroe Islands'), ('FJ', 'Fiji'), ('FI', 'Finland'), \
# 	('FR', 'France'), ('GF', 'French Guyana'), ('PF', 'French Polynesia'), ('TF', 'French Southern Territories'), ('GA', 'Gabon'), \
# 	('GM', 'Gambia'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GR', 'Greece'), ('GL', 'Greenland'), ('GD', 'Grenada'), ('GP', 'Guadeloupe'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GG', 'Guernsey'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HM', 'Heard and Mcdonald Islands'), ('VA', 'Holy See (Vatican City State)'), ('HN', 'Honduras'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran, Islamic Republic of'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IM', 'Isle of Man'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'), ('JP', 'Japan'), ('JE', 'Jersey'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KI', 'Kiribati'), ('KP', 'Korea (North)'), ('KR', 'Korea (South)'), ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', 'Lao PDR'), ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'), ('LY', 'Libya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MK', 'Macedonia, Republic of'), ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MH', 'Marshall Islands'), ('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('YT', 'Mayotte'), ('MX', 'Mexico'), ('FM', 'Micronesia, Federated States of'), ('MD', 'Moldova'), ('MC', 'Monaco'), ('MN', 'Mongolia'), ('ME', 'Montenegro'), ('MS', 'Montserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), ('MM', 'Myanmar'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('AN', 'Netherlands Antilles'), ('NC', 'New Caledonia'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'), ('NF', 'Norfolk Island'), ('MP', 'Northern Mariana Islands'), ('NO', 'Norway'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PW', 'Palau'), ('PS', 'Palestinian Territory'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PN', 'Pitcairn'), ('PL', 'Poland'), ('PT', 'Portugal'), ('PR', 'Puerto Rico'), ('QA', 'Qatar'), ('RE', 'Réunion'), ('RO', 'Romania'), ('RU', 'Russian Federation'), ('RW', 'Rwanda'), ('BL', 'Saint-Barthélemy'), ('SH', 'Saint Helena'), ('KN', 'Saint Kitts and Nevis'), ('LC', 'Saint Lucia'), ('MF', 'Saint-Martin (French part)'), ('PM', 'Saint Pierre and Miquelon'), ('VC', 'Saint Vincent and Grenadines'), ('WS', 'Samoa'), ('SM', 'San Marino'), ('ST', 'Sao Tome and Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'), ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), ('SO', 'Somalia'), ('ZA', 'South Africa'), ('GS', 'South Georgia and the South Sandwich Islands'), ('SS', 'South Sudan'), ('ES', 'Spain'), ('LK', 'Sri Lanka'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SJ', 'Svalbard and Jan Mayen Islands'), ('SZ', 'Swaziland'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SY', 'Syrian Arab Republic (Syria)'), ('TW', 'Taiwan, Republic of China'), ('TJ', 'Tajikistan'), ('TZ', 'Tanzania, United Republic of'), ('TH', 'Thailand'), ('TL', 'Timor-Leste'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), ('TC', 'Turks and Caicos Islands'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'), ('GB', 'United Kingdom'), ('US', 'United States of America'), ('UM', 'US Minor Outlying Islands'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VE', 'Venezuela (Bolivarian Republic)'), ('VN', 'Viet Nam'), ('VI', 'Virgin Islands, US'), ('WF', 'Wallis and Futuna Islands'), ('EH', 'Western Sahara'), ('YE', 'Yemen'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe')]
# 	country_filter = SelectField('Filter by country', choices=countrychoices, validators=[Optional()])
# 	org_filter = SelectField('Filter by organisation type', choices=typechoices, validators=[Optional()])

# 	submit = SubmitField('Filter')

class EditPartnerForm(FlaskForm):
	typechoices = [('HEI', 'University'), ('NGO', 'Non-government organisation'), ('RES', 'Research centre'), ('GOV', 'Government organisation')]

	name = StringField('Partner name', validators=[Optional()])
	offname = StringField('Official name', validators=[Optional()])
	ptype = SelectField(u'Organisation type', choices=typechoices, validators=[Optional()])
	country = SelectField(u'Country', validators=[Optional()])
	city = StringField('Town/city', validators=[Optional()])
	submit = SubmitField('Update details')