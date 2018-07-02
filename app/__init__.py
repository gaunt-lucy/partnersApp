from flask import Flask

app = Flask(__name__)

from app import routes #imported at the bottom to resolve circular import issue