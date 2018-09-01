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

class EditUserDetailsForm(FlaskForm):
	fname = StringField('First name', validators=[DataRequired()])
	sname = StringField('Surname', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Update')

class RequestResetPasswordForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Request password reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset password')

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

	#yearoption = [('2010', '2010/11'), ('2011', '2011/12'), ('2012', '2012/13'), ('2013', '2013/14'), ('2014', '2014/15'), \
	#('2015', '2015/16'), ('2016', '2016/17'), ('2017', '2017/18'), ('2018', '2018/19')]

	typelevel = [('Undergraduate', 'Undergraduate'), ('Postgraduate Taught', 'Postgraduate Taught'), ('Postgraduate Research', 'Postgraduate Research'), \
	('Academic staff', 'Academic staff'), ('Professional services staff', 'Professional services staff')]

	def validate_total(form, field):
		if field.data%0.5 != 0:
			raise ValidationError('Partial mobilities may not be more or less than 0.5FTE - please adjust total.')
	session = SelectField(u'Select session', validators=[DataRequired()])
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
	
class EditPartnerForm(FlaskForm):
	typechoices = [('HEI', 'University'), ('NGO', 'Non-government organisation'), ('RES', 'Research centre'), ('GOV', 'Government organisation')]

	name = StringField('Partner name', validators=[Optional()])
	offname = StringField('Official name', validators=[Optional()])
	ptype = SelectField(u'Organisation type', choices=typechoices, validators=[Optional()])
	country = SelectField(u'Country', validators=[Optional()])
	city = StringField('Town/city', validators=[Optional()])
	submit = SubmitField('Update details')