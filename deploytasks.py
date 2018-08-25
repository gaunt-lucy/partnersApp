from flask import app
from app. models import User, Partner, Mobility, Country, AgreeType, OrgType

User.bulk_add_users()
Partner.bulk_add_partners()
Mobility.insert_mobs()
Country.insert_countries()
AgreeType.add_types()
OrgType.add_types()