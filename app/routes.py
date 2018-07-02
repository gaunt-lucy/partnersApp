from app import app
from flask import render_template #rendering function imported from Jinja2 template engine (bundled w/ Flask)

@app.route('/')#using python deocorators to create function callback to URL route
@app.route('/index')
def index():
	user = {'username': 'Lucy'} #fake objects for testing
	collabs = [
		{
			'name': 'University of Lyon',
			'city': 'Lyon',
			'country':'France',
			'contact': {'username': 'Conor'}
		},
		{
			'name': 'McGill University',
			'city': 'Montreal',
			'country':'Canada',
			'contact': {'username': 'Clare'}
		}
		]
	return render_template('index.html', title='Home', user=user, collabs=collabs)
