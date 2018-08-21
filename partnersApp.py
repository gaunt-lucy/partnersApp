from app import app, db #define Flask application instance
from app.models import User, Partner, Visit, Report, Country, OrgType, Mobility

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Partner': Partner, 'Mobility': Mobility, 'Country': Country, 'Visit': Visit, 'OrgType': OrgType}

