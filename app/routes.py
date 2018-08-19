from app import app, db
from datetime import datetime, date
from flask import render_template, flash, redirect, url_for, request, session
from werkzeug.urls import url_parse
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import func
import json
#rendering function imported from Jinja2 template engine (bundled w/ Flask)
#flash imported to flash messages
#redirect imported to facilitate user redirects given certain conditions

from app.forms import EditPartnerForm, BrowseForm, SearchForm, AddVisit, LoginForm, RegistrationForm, NewPartnerForm, AddAgreementForm, EnterMobility, AddVisitReport#import the form classes
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Partner, Agreement, Visit, Report, Country, OrgType, AgreeType, Mobility

@app.route('/')#using python deocorators to create function callback to URL route
@app.route('/landing')
def landing():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	return render_template('landing.html')

@app.route('/testindex')
def testindex():

	return render_template('testindex.html', title='Home')

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

		user = User(email=form.email.data, fname=form.fname.data, sname=form.sname.data)
		user.set_password(form.password.data)
		user.create_userid(form.fname.data, form.sname.data)
		db.session.add(user)
		db.session.commit()
		flash('User registration successful.')
		return redirect(url_for('login'))

	return render_template('register.html', title='Register', form=form)

@app.route('/newpartner', methods=['GET', 'POST'])
def newpartner():

	countries = Country.query.all()
	options = [(str(c.iso), c.name) for c in countries]

	form = NewPartnerForm()
	form.country.choices = options

	if form.validate_on_submit():
		partner = Partner(name=form.name.data, offname=form.offname.data, ptype=form.ptype.data, city=form.city.data, owner=current_user.id, country=form.country.data)
		db.session.add(partner)
		db.session.commit()
		flash('New partner added.')
		return redirect(url_for('index'))
	
	return render_template('newpartner.html', title='Add partner', form=form)

# @app.route('/dashboard/<userid>')
# @login_required
# def dashboard(userid):
# 	user = User.query.filter_by(userid=userid).first_or_404()
# 	collabs = [
# 		{
# 			'name': 'McGill University',
# 			'offname': 'McGill University',
# 			'id': '1',
# 			'ptype': 'University',
# 			'city': 'Montreal',
# 			'country':'Canada',
# 			'contact': {'userid': 'Clare Herbert'},
# 			'owner': 'Richard Jones',
# 			'created_date': '01 September 2012'
# 		},
# 		{
# 			'name': 'University of Lyon',
# 			'offname': 'Université de Lyon',
# 			'id': '2',
# 			'ptype': 'University',
# 			'city': 'Lyon',
# 			'country':'France',
# 			'contact': {'userid': 'Laura Smith'},
# 			'owner': 'Julia Dawson',
# 			'created_date': '01 September 2011'
# 		},

# 			{
# 			'name': 'UTexas Austin',
# 			'offname': 'University of Texas at Austin',
# 			'id': '3',
# 			'ptype': 'University',
# 			'city': 'Austin, Texas',
# 			'country':'USA',
# 			'contact': {'userid': 'Angela Vaughn'},
# 			'owner': 'Lucy Gaunt',
# 			'created_date': '01 September 2009'
# 		}
# 		]


# 	return render_template('dashboard.html', title='Dashboard', user=user, collabs=collabs)

@app.route('/partner/<id>')
def partner(id):
	partner = Partner.query.filter_by(id=id).first_or_404()

	user = User.query.filter_by(id=partner.owner).first_or_404()

	agrees = Agreement.query.filter_by(partner=partner.id).all()

	visits = Visit.query.filter_by(partner=partner.id).all()

	#mobilities = db.session.query(Mobility.session, Mobility.totalin, Mobility.totalout).group_by(Mobility.session).all()

	#mobdata = db.session.query(Mobility.session,func.sum(Mobility.totalin), func.sum(Mobility.totalout)).group_by(Mobility.session).all()
	# data = []
	# for m in mobdata:
	#  	#data.append(str(m[0]))
	#  	data.append(float(m[1]))
	#  	data.append(float(m[2]))
	
	# data.insert(0,'Outbound')
	# data.insert(0,'Inbound')
	# data.insert(0,'Year')

	data = [2, 3, 4, 5, 6, 6, 7]

	return render_template('partner.html', agrees=agrees, partner=partner, user=user, visits=visits, data=data)

@app.route('/addagree/<id>', methods=['GET', 'POST'])
def addagree(id):

	partner = Partner.query.filter_by(id=id).first_or_404()

	partners = Partner.query.all()
	options = [(str(p.id), p.name) for p in partners]

	form = AddAgreementForm(request.form)

	if form.validate_on_submit():
		p = Partner.query.filter_by(id=id).first()

		agreement = Agreement(partner=p.id, atype=form.atype.data, start_date=form.startdate.data, end_date=form.enddate.data)
		db.session.add(agreement)
		db.session.commit()
		flash('Agreement added.')
		return redirect(url_for('partner', id=id))

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
	partner = Partner.query.filter_by(id=1).first_or_404()
	#if/else for choices
	agreements = Agreement.query.all()
	mobtypes = AgreeType.query.all()
	agreementoptions = [(a.id, (str(a.atype)+': '+str(a.start_date.year)+'-'+str(a.end_date.year))) for a in agreements]
	mobilityoptions = [(m.code, m.name) for m in mobtypes]

	form = EnterMobility()
	form.agreement.choices = agreementoptions
	form.mobilitytype.choices = mobilityoptions

	if form.validate_on_submit():
		mobility = Mobility(mobilitytype=form.mobilitytype.data, partner=partner.id, level=form.level.data,\
			session=form.session.data, totalin=form.totalin.data, totalout=form.totalout.data)
		if form.agreement.data:
			mobility.agreement = form.agreement.data
		db.session.add(mobility)
		db.session.commit()
		flash('Mobility data added')

		return redirect(url_for('partner', id=partner.id))

	return render_template('addmobility.html', form=form, partner=partner, agreements=agreements)

@app.route('/mobilitydata/<id>')
def mobilitydata(id):
	partner = Partner.query.filter_by(id=id).first_or_404()
	
	mobilities = Mobility.query.filter_by(partner=id).all()

	agreetypes = AgreeType.query.all()

	return render_template('mobilitydata.html', partner=partner, agreetypes=agreetypes, mobilities=mobilities)

@app.route('/addvisit/<id>', methods=['GET', 'POST'])
def addvisit(id):

	partner = Partner.query.filter_by(id=id).first_or_404()

	form = AddVisit()

	if form.validate_on_submit():
		p = Partner.query.filter_by(id=id).first()

		visit = Visit(partner=p.id, vtype=form.vtype.data, start_date=form.start_date.data, end_date=form.end_date.data)
		db.session.add(visit)
		db.session.commit()
		flash('Visit record added.')
		
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
		if form.text_search.data:
			partners = Partner.query.filter(Partner.name.like(wildcard+form.text_search.data+wildcard)).all()
			session['partners'] = serialise(partners)

		else:
			partners = Partner.query.all()
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

	author = current_user.sname+', '+current_user.fname

	if form.validate_on_submit():
		report = Report(content=form.report.data, visit_id=id, author=author)
		db.session.add(report)
		db.session.commit()
		flash('Visit report added.')
		return redirect(url_for('visitdetails', id=partner.id))

	return render_template('addreport.html', form=form, visit=visit, partner=partner)

@app.route('/editpartner/<id>', methods=['GET', 'POST'])
@login_required
def editpartner(id):

	countries = Country.query.all()
	options = [(str(c.iso), c.name) for c in countries]

	form = EditPartnerForm()
	form.country.choices = options
	partner = Partner.query.filter_by(id=id).first_or_404()

	if form.validate_on_submit():
		partner.name = form.name.data
		partner.offname = form.offname.data
		partner.ptype = form.ptype.data
		partner.country = form.country.data
		partner.city = form.city.data
		partner.last_updated = datetime.now().date()
		partner.updated_by = current_user.id
		db.session.add(partner)
		db.session.commit()
		flash ('Partner details updated.')
		return redirect(url_for('partner', id=id))

	form.name.data = partner.name
	form.offname.data = partner.offname
	form.ptype.data = partner.ptype
	form.country.data = partner.country
	form.city.data = partner.city

	return render_template('editpartner.html', form=form)

@app.route('/reportdetails/<id>', methods=['GET', 'POST'])
@login_required
def reportdetails(id):

	reports = Report.query.filter_by(visit_id=id).all()

	visit = Visit.query.filter_by(id=id).first()

	partner = Partner.query.filter_by(id=visit.partner).first()
		
	return render_template('reportdetails.html', reports=reports, visit=visit, partner=partner)

@app.route('/report/<id>', methods=['GET', 'POST'])
@login_required
def viewreport(id):

	report = Report.query.filter_by(id=id).first()

	visit = Visit.query.filter_by(id=report.visit_id).first()

	partner = Partner.query.filter_by(id=visit.partner).first()
		
	return render_template('report.html', report=report, visit=visit, partner=partner)