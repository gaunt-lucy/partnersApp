from flask import app
from app. models import User, Partner, Mobility, Country, AgreeType, OrgType

#User.bulk_add_users()
Country.insert_countries()
Partner.bulk_add_partners()
AgreeType.add_types()
OrgType.add_types()
#Mobility.insert_mobs()
