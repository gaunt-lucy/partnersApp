from app import app, db
from flask import render_template, flash, redirect, url_for, request, session
from werkzeug.urls import url_parse
#rendering function imported from Jinja2 template engine (bundled w/ Flask)
#flash imported to flash messages
#redirect imported to facilitate user redirects given certain conditions

from app.forms import LoginForm, RegistrationForm, NewPartnerForm, AddAgreementForm, EnterMobility #import the form classes
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Partner, Agreement

@app.route('/')#using python deocorators to create function callback to URL route
@app.route('/index')
@login_required
def index():
	#user = {'userid': 'Lucy'} #fake objects for testing
	collabs = [
		{
			'name': 'University of Lyon',
			'type': 'Student exchange',
			'level': 'Undergraduate',
			'city': 'Lyon',
			'country':'France',
			'contact': {'userid': 'Conor'}
		},
		{
			'name': 'McGill University',
			'type': 'Student exchange',
			'level': 'Undergraduate',
			'city': 'Montreal',
			'country':'Canada',
			'contact': {'userid': 'Clare'}
		},

			{
			'name': 'University of Texas at Austin',
			'type': 'Student exchange',
			'level': 'Postgraduate',
			'city': 'Austin',
			'country':'USA',
			'contact': {'userid': 'Richard'}
		}
		]
	return render_template('index.html', title='Home', collabs=collabs)

@app.route('/login', methods=['GET', 'POST']) #GET and POST tell browser what to do with data
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(userid=form.userid.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid userid or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)

	return render_template('login.html', title='Log in', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(userid=form.userid.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('User registration successful.')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/newpartner', methods=['GET', 'POST'])
def newpartner():

	form = NewPartnerForm()

	if form.validate_on_submit():
		partner = Partner(name=form.name.data, offname=form.offname.data, ptype=form.ptype.data, city=form.city.data, owner=current_user.id, country=form.country.data)
		db.session.add(partner)
		db.session.commit()
		flash('New partner added.')
		return redirect(url_for('index'))
	
	return render_template('newpartner.html', title='Add partner', form=form)

@app.route('/dashboard/<userid>')
@login_required
def dashboard(userid):
	user = User.query.filter_by(userid=userid).first_or_404()
	collabs = [
		{
			'name': 'McGill University',
			'offname': 'McGill University',
			'id': 12,
			'ptype': 'University',
			'city': 'Montreal',
			'country':'Canada',
			'contact': {'userid': 'Clare Herbert'},
			'owner': 'Richard Jones',
			'created_date': '01 September 2012'
		},
		{
			'name': 'University of Lyon',
			'offname': 'Université de Lyon',
			'id': 13,
			'ptype': 'University',
			'city': 'Lyon',
			'country':'France',
			'contact': {'userid': 'Laura Smith'},
			'owner': 'Julia Dawson',
			'created_date': '01 September 2011'
		},

			{
			'name': 'UTexas Austin',
			'offname': 'University of Texas at Austin',
			'id': 14,
			'ptype': 'University',
			'city': 'Austin, Texas',
			'country':'USA',
			'contact': {'userid': 'Angela Vaughn'},
			'owner': 'Lucy Gaunt',
			'created_date': '01 September 2009'
		}
		]
	return render_template('dashboard.html', user=user, collabs=collabs)

@app.route('/partner')
def partner():
	collab = {'name': 'McGill University',
			'offname': 'McGill University',
			'ptype': 'University',
			'city': 'Montreal',
			'country':'Canada',
			'contact': {'userid': 'Clare Amie'},
			'owner': 'Richard Jones',
			'created_date': '01 September 2012'} 
	agrees = [{'id': 'MCGI01', 'atype': 'Student exchange', 'status': 'Active'},
			{'id': 'MCGI02', 'atype': 'Dual degree', 'status': 'Active'},
			{'id': 'MCGI04', 'atype': 'Research MOU', 'status': 'Active'}]


	return render_template('partner.html', collab=collab, agrees=agrees)

@app.route('/addagree', methods=['GET', 'POST'])
def addagree():
	partners = Partner.query.all()
	options = [(str(p.id), p.name) for p in partners]
	# pts = [(1, 'Hogwarts School of Witchcraft and Wizardry'), (2, 'University of Pennsylvania'), ('3', 'Mollie Grant')]

	form = AddAgreementForm(request.form)
	form.selectPartner.choices = options

	if form.validate_on_submit():
		p = Partner.query.filter_by(id=form.selectPartner.data).first()

		agreement = Agreement(partner=p.id, atype=form.atype.data, start_date=form.startdate.data, end_date=form.enddate.data)
		db.session.add(agreement)
		db.session.commit()
		
		return redirect(url_for('testview'))

	return render_template('addagree.html', form=form)


@app.route('/testview')
def testview():
		
	return render_template('testview.html')

@app.route('/addmobility', methods=['GET', 'POST'])
def addmobility():

	form = EnterMobility()

	partner = 'University of California'
	atype = 'Student exchange'

	if form.validate_on_submit():
		return redirect(url_for('testview'))

	return render_template('addmobility.html', form=form, partner=partner, atype=atype)