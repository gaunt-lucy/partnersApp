from flask import Flask
from config import Config #read the configuration settings

app = Flask(__name__)
app.config.from_object(Config)

from app import routes #imported at the bottom to resolve circular import issue