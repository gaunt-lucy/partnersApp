from app import app, db #define Flask application instance
from app.models import User, Partner, Visit, Report, Country, OrgType

##@app.shell_context_processor
##def make_shell_context():
##	return {'db': db, 'User': User, 'Partner': Partner}

