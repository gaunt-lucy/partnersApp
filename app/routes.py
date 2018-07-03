from app import app
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
#rendering function imported from Jinja2 template engine (bundled w/ Flask)
#flash imported to flash messages
#redirect imported to facilitate user redirects given certain conditions

from app.forms import LoginForm #import the form class which is instantiated by the login view function
from flask_login import current_user, login_user, logout_user
from app.models import User

@app.route('/')#using python deocorators to create function callback to URL route
@app.route('/index')
@login_required
def index():
	user = {'userid': 'Lucy'} #fake objects for testing
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
	return render_template('index.html', title='Home', user=user, collabs=collabs)

@app.route('/login', methods=['GET', 'POST']) #GET and POST tell browser what to do with data
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = LoginForm()

	if form.validate_on_submit():
		uesr = User.query.filter_by(userid=form.userid.data).first()
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