from app import app
from flask import render_template, flash, redirect, url_for
#rendering function imported from Jinja2 template engine (bundled w/ Flask)
#flash imported to flash messages
#redirect imported to facilitate user redirects given certain conditions

from app.forms import LoginForm #import the form class which is instantiated by the login view function

@app.route('/')#using python deocorators to create function callback to URL route
@app.route('/index')
def index():
	user = {'username': 'Lucy'} #fake objects for testing
	collabs = [
		{
			'name': 'University of Lyon',
			'type': 'Student exchange',
			'level': 'Undergraduate',
			'city': 'Lyon',
			'country':'France',
			'contact': {'username': 'Conor'}
		},
		{
			'name': 'McGill University',
			'type': 'Student exchange',
			'level': 'Undergraduate',
			'city': 'Montreal',
			'country':'Canada',
			'contact': {'username': 'Clare'}
		},

			{
			'name': 'University of Texas at Austin',
			'type': 'Student exchange',
			'level': 'Postgraduate',
			'city': 'Austin',
			'country':'USA',
			'contact': {'username': 'Richard'}
		}
		]
	return render_template('index.html', title='Home', user=user, collabs=collabs)

@app.route('/login', methods=['GET', 'POST']) #GET and POST tell browser what to do with data
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for user {}, remember user={}'.format(
			form.userid.data, form.remember.data))
		return redirect(url_for('index')) #remove hard-coded URL link, replace with url_for function
	return render_template('login.html', title='Log in', form=form)