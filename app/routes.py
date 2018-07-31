from app import app, db
from flask import render_template, flash, redirect, url_for, request, session
from werkzeug.urls import url_parse
#rendering function imported from Jinja2 template engine (bundled w/ Flask)
#flash imported to flash messages
#redirect imported to facilitate user redirects given certain conditions

from app.forms import SearchForm, AddVisit, LoginForm, RegistrationForm, NewPartnerForm, AddAgreementForm, EnterMobility, AddVisitReport#import the form classes
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Partner, Agreement, Visit, Report

@app.route('/landing')
def landing():
	return render_template('landing.html')

@app.route('/')#using python deocorators to create function callback to URL route
@app.route('/index')
@login_required
def index():

	return render_template('index.html', title='Home')



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
		#user = User(userid=form.userid.data, email=form.email.data)
		user = User(userid=form.email.data, fname=form.fname.data, sname=form.sname.data, email=form.email.data)
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
			'id': '1',
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
			'id': '2',
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
			'id': '3',
			'ptype': 'University',
			'city': 'Austin, Texas',
			'country':'USA',
			'contact': {'userid': 'Angela Vaughn'},
			'owner': 'Lucy Gaunt',
			'created_date': '01 September 2009'
		}
		]


	return render_template('dashboard.html', title='Dashboard', user=user, collabs=collabs)

@app.route('/partner/<id>')
def partner(id):
	partner = Partner.query.filter_by(id=id).first_or_404()

	user = User.query.filter_by(id=partner.owner).first_or_404()

	agrees = Agreement.query.filter_by(partner=partner.id).all()

	visits = Visit.query.filter_by(partner=partner.id).all()


	return render_template('partner.html', agrees=agrees, partner=partner, user=user, visits=visits)

@app.route('/addagree/<id>', methods=['GET', 'POST'])
def addagree(id):

	partner = Partner.query.filter_by(id=id).first_or_404()

	partners = Partner.query.all()
	options = [(str(p.id), p.name) for p in partners]

	form = AddAgreementForm(request.form)
	#form.selectPartner.choices = options

	if form.validate_on_submit():
		p = Partner.query.filter_by(id=id).first()

		agreement = Agreement(partner=p.id, atype=form.atype.data, start_date=form.startdate.data, end_date=form.enddate.data)
		db.session.add(agreement)
		db.session.commit()
		
		return redirect(url_for('testview'))

	return render_template('addagree.html', form=form, partner=partner)

@app.route('/agreementdetails/<id>')
def viewagrees(id):

	partner = Partner.query.filter_by(id=id).first_or_404()

	agrees = Agreement.query.filter_by(partner=partner.id).all()

	return render_template('agreementdetails.html', agrees=agrees, partner=partner)

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


@app.route('/addvisit/<id>', methods=['GET', 'POST'])
def addvisit(id):

	partner = Partner.query.filter_by(id=id).first_or_404()

	form = AddVisit()

	if form.validate_on_submit():
		p = Partner.query.filter_by(id=id).first()

		visit = Visit(partner=p.id, vtype=form.vtype.data, start_date=form.start_date.data, end_date=form.end_date.data)
		db.session.add(visit)
		db.session.commit()
		
		return redirect(url_for('partner', id=partner.id)) 

	return render_template('addvisit.html', form=form, partner=partner)

@app.route('/visitdetails/<id>')
def visitdetails(id):

	partner = Partner.query.filter_by(id=id).first_or_404()

	visits = Visit.query.filter_by(partner=partner.id).all()

	reports = Report.query.filter_by(visit_id=id).all()

	return render_template('visitdetails.html', visits=visits, partner=partner, reports=reports)


## pack up a list of partners to be saved as user session value
def serialise(partners):
		ids = []
		for partner in partners:
			ids.append(partner.id)

		return ids

## unpack up a list of partners from ids saved in user session value
def deserialise(ids):
	partners = []
	for i in ids: 
		partners.append(Partner.query.filter_by(id=i).first())

	return partners

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
	form = SearchForm()
	wildcard = '%'

	if form.validate_on_submit():
		partners = Partner.query.filter(Partner.name.like(wildcard+form.text_search.data+wildcard)).all()
		session['partners'] = serialise(partners)

		return redirect(url_for('results'))

	return render_template('search.html', form=form)

@app.route('/results', methods=['GET', 'POST'])
@login_required
def results():

	form = SearchForm()
	wildcard = '%'
	partners = deserialise(session['partners'])

	if form.validate_on_submit():
		partners = Partner.query.filter(Partner.name.like(wildcard+form.text_search.data+wildcard)).all()
		session['partners'] = serialise(partners)

		return redirect(url_for('results'))

		
	return render_template('results.html', form=form, partners=partners)

@app.route('/addreport/<id>', methods=['GET', 'POST'])
@login_required
def addreport(id):

	form = AddVisitReport()

	visit = Visit.query.filter_by(id=id).first()

	partner = Partner.query.filter_by(id=visit.partner).first()

	# if form.validate_on_submit():
	# 	report = Report(content=form.report.data, visit_id=id)
	# 	db.session.add(report)
	# 	db.session.commit()
	# 	redirect (url_for('visitdetails', id=id))

	return render_template('addreport.html', form=form, visit=visit, partner=partner)