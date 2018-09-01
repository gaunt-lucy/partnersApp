from flask import app
from app. models import User, Partner, Mobility, Country, AgreeType, OrgType, AcademicYear

User.bulk_add_users()
User.adminuser()
Country.insert_countries()
Partner.bulk_add_partners()
AgreeType.add_types()
OrgType.add_types()
AcademicYear.add_years()
Mobility.insert_mobs()
