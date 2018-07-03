import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object): #config class defines configuration settings for the application as variables
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'cat-on-keyboard'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False