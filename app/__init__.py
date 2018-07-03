from flask import Flask
from config import Config #read the configuration settings
#Todo: untrack the config file from Github
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)#intialise database object instance
migrate = Migrate(app, db)#initialise migration engine instance

from app import routes, models #imported at the bottom to resolve circular import issue