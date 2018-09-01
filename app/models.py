from app import app, db, login
from datetime import datetime, date
from time import time
import jwt
from werkzeug.security import generate_password_hash, check_password_hash #password hash function provided by Werkzeug package (Flask dependency)
from flask_login import UserMixin #implements required methods and properties for flask_login to work with the User model
from random import randint


class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.String(64), index=True, unique=True)
	fname = db.Column(db.String(64), index=True)
	sname = db.Column(db.String(64), index=True)
	email = db.Column(db.String(120), index=True, unique=True)
	role = db.Column(db.String)
	passwordhash = db.Column(db.String(128))
	collabs = db.relationship('Partner', backref='col_owner', lazy='dynamic')
	reports = db.relationship('Report', backref='report_author', lazy='dynamic')

	def __repr__(self):
		return '<User {}>'.format(self.fname)

	def set_password(self, password):
		self.passwordhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.passwordhash, password)

	def create_userid(self, fname, sname):
		self.userid = (sname+fname[0]).lower()

	def set_admin(self):
		self.role = 'Admin'
		db.session.commit()

	def is_admin(self):
		if self.role == 'Admin':
			return True
		else:
			return False

	##code attributed to Miguel Grinberg, 'Flask Web Development', 2014
	def get_reset_password_token(self, expires_in=600):
		return jwt.encode(
			{'reset_password': self.id, 'exp': time() + expires_in},
			app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

	##code attributed to Miguel Grinberg, 'Flask Web Development', 2014
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password'] 
		except:
			return
		return User.query.get(id)

	def adminuser():
		user = User.query.filter_by(email="lucygaunt@ed.ac.uk")
		u = User(fname="Lucy", sname="Duff", role="Admin", email="lucyduff@ed.ac.uk")
		u.set_password('cat')
		u.create_userid("Lucy","Duff")
		db.session.add(u)
		db.session.commit()

	@staticmethod	
	def bulk_add_users():
		users = [ ("Thibaut","Kemmer","tkemmer0@accuweather.com"),\
				("Lucy","Gaunt","tkemmer0@unseen.ac.uk"),\
				("Michael","Cumberland","mcumberland1@unseen.ac.uk"),\
				("Lyndsey","Mingaye","lmingaye2@unseen.ac.uk"),\
				("Hobart","Carek","hcarek3@unseen.ac.uk"),\
				("Orren","Weedon","oweedon4@unseen.ac.uk"),\
				("Crichton","Crottagh","ccrottagh5@unseen.ac.uk"),\
				("Ki","Disney","kdisney6@unseen.ac.uk"),\
				("Jennica","Waggett","jwaggett7@unseen.ac.uk"),\
				("Vergil","Edds","vedds8@unseen.ac.uk"),\
				("Glenda","Fesby","gfesby9@unseen.ac.uk"),\
				("Rafaelia","Youel","ryouela@unseen.ac.uk"),\
				("Brena","Burchess","bburchessb@unseen.ac.uk"),\
				("Carmelia","Scrange","cscrangec@unseen.ac.uk"),\
				("Elisabeth","Chitty","echittyd@unseen.ac.uk"),\
				("Valina","Seelbach","vseelbache@unseen.ac.uk"),\
				("Estrellita","Preto","epretof@unseen.ac.uk"),\
				("Dylan","Anfonsi","danfonsig@unseen.ac.uk"),\
				("Osborn","Brozsset","obrozsseth@unseen.ac.uk"),\
				("Camellia","Tarling","ctarlingi@unseen.ac.uk"),\
				("Donaugh","Seary","dsearyj@unseen.ac.uk"),\
				("Manny","Grenshields","mgrenshieldsk@unseen.ac.uk"),\
				("Ange","Tuttiett","atuttiettl@unseen.ac.uk"),\
				("Wilie","Devonshire","wdevonshirem@unseen.ac.uk"),\
				("Omero","Grundey","ogrundeyn@unseen.ac.uk"),\
				("Geneva","Bonsul","gbonsulo@unseen.ac.uk"),\
				("Dell","Sandell","dsandellp@unseen.ac.uk"),\
				("Carol","Poxton","cpoxtonq@unseen.ac.uk"),\
				("Lazaro","MacMechan","lmacmechanr@unseen.ac.uk"),\
				("Marthena","Smalley","msmalleys@unseen.ac.uk"),\
				("Pace","Monckman","pmonckmant@unseen.ac.uk"),\
				("Colin","Le Jean","clejeanu@unseen.ac.uk"),\
				("Burl","Derrington","bderrington@unseen.ac.uk"),\
				("Courtnay","Stockall","cstockallw@unseen.ac.uk"),\
				("Creigh","Giacomozzo","cgiacomozzox@unseen.ac.uk"),\
				("Vita","Sinnie","vsinniey@unseen.ac.uk"),\
				("Lynnelle","Adamovitz","ladamovitzz@unseen.ac.uk"),\
				("Nicholas","Hamblyn","nhamblyn10@unseen.ac.uk"),\
				("Xavier","Ludlow","xludlow11@unseen.ac.uk"),\
				("Chrotoem","Roistone","croistone12@unseen.ac.uk"),\
				("Shirlee","Spykings","sspykings13@unseen.ac.uk"),\
				("Buiron","Faldoe","bfaldoe14@unseen.ac.uk"),\
				("Pru","Darey","pdarey15@unseen.ac.uk"),\
				("Deborah","Grange","dgrange16@unseen.ac.uk"),\
				("Don","Stolte","dstolte17@unseen.ac.uk"),\
				("Florance","Kliemke","@unseen.ac.uk"),\
				("Agnesse","Merfin","amerfin19@unseen.ac.uk"),\
				("Amy","Jadczak","ajadczak1a@unseen.ac.uk"),\
				("Tania","Juorio","tjuorio1b@unseen.ac.uk"),\
				("Muhammad","Ast","mast1c@unseen.ac.uk"),\
				("Dalston","Alexsandrowicz","dalexsandrowicz1d@unseen.ac.uk"),\
				("Nickola","Lauridsen","nlauridsen1e@unseen.ac.uk"),\
				("Margette","Van Arsdalen","mvanarsdalen1f@unseen.ac.uk"),\
				("Kahlil","Sprowles","ksprowles1g@unseen.ac.uk"),\
				("Marcel","Allridge","mallridge1h@unseen.ac.uk"),\
				("Shaughn","Behninck","sbehninck1i@unseen.ac.uk"),\
				("Caitrin","Gribbell","cgribbell1j@unseen.ac.uk"),\
				("Enrika","Keningley","ekeningley1k@unseen.ac.uk"),\
				("Dennis","Dempsey","ddempsey1l@unseen.ac.uk"),\
				("Michaelina","Simes","msimes1m@unseen.ac.uk"),\
				("Stanly","Gonnin","sgonnin1n@unseen.ac.uk"),\
				("Vikky","Strother","vstrother1o@unseen.ac.uk"),\
				("Melesa","Antonignetti","mantonignetti1p@unseen.ac.uk"),\
				("Jana","Lande","jlande1q@unseen.ac.uk"),\
				("Penny","Scholefield","pscholefield1r@unseen.ac.uk"),\
				("Tyler","Cussins","tcussins1s@unseen.ac.uk"),\
				("Zed","Benka","zbenka1t@unseen.ac.uk"),\
				("Nils","Goretti","ngoretti1u@unseen.ac.uk"),\
				("Cchaddie","Ewert","cewert1v@unseen.ac.uk"),\
				("Marlo","Abberley","mabberley1w@unseen.ac.uk"),\
				("Leila","McKune","lmckune1x@unseen.ac.uk"),\
				("Blondy","Rocca","brocca1y@unseen.ac.uk"),\
				("Stillman","Sreenan","ssreenan1z@unseen.ac.uk"),\
				("Andrew","Dimitriou","adimitriou20@unseen.ac.uk"),\
				("Monika","Lillistone","mlillistone21@unseen.ac.uk"),\
				("Ebonee","Stanmore","estanmore22@unseen.ac.uk"),\
				("Jerrine","Pickavant","jpickavant23@unseen.ac.uk"),\
				("Dun","Cow","dcow24@unseen.ac.uk"),\
				("Skipper","Cannaway","scannaway25@unseen.ac.uk"),\
				("Fabiano","Alcott","falcott26@unseen.ac.uk"),\
				("Quentin","Watters","qwatters27@unseen.ac.uk"),\
				("Simone","Longmire","slongmire28@unseen.ac.uk"),\
				("Fonz","McGunley","fmcgunley29@unseen.ac.uk"),\
				("Augustine","Gurrado","agurrado2a@unseen.ac.uk"),\
				("Aurel","Briant","abriant2b@unseen.ac.uk"),\
				("Addia","Lowles","alowles2c@unseen.ac.uk"),\
				("Jerad","Wilkisson","jwilkisson2d@unseen.ac.uk"),\
				("Crystal","Mochar","cmochar2e@unseen.ac.uk"),\
				("Hildegaard","Halsall","hhalsall2f@unseen.ac.uk"),\
				("Anissa","Rames","arames2g@unseen.ac.uk"),\
				("Krystle","Timmens","ktimmens2h@unseen.ac.uk"),\
				("Chan","Willmott","cwillmott2i@unseen.ac.uk"),\
				("Jodi","Elph","jelph2j@unseen.ac.uk"),\
				("Blisse","Esposi","besposi2k@unseen.ac.uk"),\
				("Jarred","Rosbotham","jrosbotham2l@unseen.ac.uk"),\
				("Nancie","Bugdall","nbugdall2m@unseen.ac.uk"),\
				("Cathleen","Hunnisett","chunnisett2n@unseen.ac.uk"),\
				("Maurise","Reboul","mreboul2o@unseen.ac.uk"),\
				("Emmaline","Venard","evenard2p@unseen.ac.uk"),\
				("Miltie","Scamwell","mscamwell2q@unseen.ac.uk"),\
				("Aida","Ivankovic","aivankovic2r@unseen.ac.uk")]
	
		for u in users:
			user = User.query.filter_by(email=u[2]).first()
			if user == None:
				user = User(fname=u[0], sname=u[1], email=u[2])
				user.set_password('cat')
				user.create_userid(u[0], u[1])
				db.session.add(user)
				
		db.session.commit()


	@login.user_loader
	def load_user(id):
		return User.query.get(int(id))

class Partner(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), index=True, unique=True)
	offname = db.Column(db.String(200), index=True)
	ptype = db.Column(db.String(128))
	city = db.Column(db.String(128))
	country = db.Column(db.String(128), db.ForeignKey('country.iso'))
	contact = db.Column(db.String(64))
	owner = db.Column(db.Integer, db.ForeignKey('user.id'))
	created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	last_updated = db.Column(db.Date, index=True)
	updated_by = db.Column(db.Integer)
	agreement = db.relationship('Agreement', backref='partner_org', lazy='dynamic')
	visit = db.relationship('Visit', backref='visit_ref', lazy='dynamic')

	def __repr__(self):
		return '<Partner: {}>'.format(self.name)
		
	## Add test data for initial setup ## 
	@staticmethod
	def bulk_add_partners():
		partners = [ ("Yerevan State University", "Yerevan State University", "HEI", "AM", "Yerevan", "24", datetime.today()),\
					("Universidad del Cine", "Universidad del Cine", "HEI", "AR", "Buenos Aires", "57", datetime.today()),\
					("University of Melbourne", "University of Melbourne", "HEI", "AU", "Melbourne", "69", datetime.today()),\
					("University of Western Australia", "University of Western Australia", "HEI", "AU", "Sydney", "53", datetime.today()),\
					("University of Sydney", "University of Sydney", "HEI", "AU", "Sydney", "99", datetime.today()),\
					("Linz Teaching College", "Linz Teaching College", "HEI", "AU", "Linz", "14", datetime.today()),\
					("Salzburg University", "Salzburg University", "HEI", "AU", "Salzburg", "57", datetime.today()),\
					("Australian National University", "Australian National University", "HEI", "AU", "Sydney", "7", datetime.today()),\
					("Griffith University", "Griffith University", "HEI", "AU", "Sydney", "90", datetime.today()),\
					("University of Adelaide", "University of Adelaide", "HEI", "AU", "Adelaide", "85", datetime.today()),\
					("Innsbruck University", "Innsbruck University", "HEI", "AU", "Innsubruck", "74", datetime.today()),\
					("IMC University of Applies Sciences Krems", "IMC University of Applies Sciences Krems", "HEI", "AU", "Krems", "99", datetime.today()),\
					("Vienna University of Economics and Business", "Vienna University of Economics and Business", "HEI", "AU", "Vienna", "67", datetime.today()),\
					("University of Vienna", "University of Vienna", "HEI", "AU", "Vienna", "77", datetime.today()),\
					("UL Brussels", "UL Brussels", "HEI", "BE", "Brussels", "87", datetime.today()),\
					("University of Maryland", "University of Maryland", "HEI", "BE", "Brussels", "10", datetime.today()),\
					("Ghent University, Lund University", "Ghent University, Lund University", "HEI", "BE", "Ghent", "80", datetime.today()),\
					("LERU ", "LERU ", "NGO", "BE", "Leuven", "2", datetime.today()),\
					("UL Brussels", "UL Brussels", "HEI", "BE", "Brussels", "49", datetime.today()),\
					("Antwerp University", "Antwerp University", "HEI", "BE", "Antwerp", "32", datetime.today()),\
					("Haute Ecole de Namur-Liège-Luxembourg", "Haute Ecole de Namur-Liège-Luxembourg", "HEI", "BE", "Luxembourg", "82", datetime.today()),\
					("Katholieke Universiteit Leuven", "Katholieke Universiteit Leuven", "HEI", "BE", "Leuven", "89", datetime.today()),\
					("LUCA School of Arts", "LUCA School of Arts", "HEI", "BE", "Schaerbeek", "78", datetime.today()),\
					("Universite Catolique De Louvain", "Universite Catolique De Louvain", "HEI", "BE", "Louvain", "81", datetime.today()),\
					("UFSC, UNEF / LENEP Macae, Unicamp, UFRJ", "UFSC, UNEF / LENEP Macae, Unicamp, UFRJ", "HEI", "BR", "Florianópolis", "22", datetime.today()),\
					("UFRGS", "UFRGS", "NGO", "BR", "Rio de Janiero", "80", datetime.today()),\
					("Universidade Federal de Mato Grosso", "Universidade Federal de Mato Grosso", "HEI", "BR", "Mato Grosso", "65", datetime.today()),\
					("Universidade Federal da Grande Dourados", "Universidade Federal da Grande Dourados", "HEI", "BR", "Grande Dourados", "27", datetime.today()),\
					("Unicamp", "Unicamp", "HEI", "BR", "Rio de Janiero", "54", datetime.today()),\
					("Universidade Federal de Santa Catarina", "Universidade Federal de Santa Catarina", "HEI", "BR", "Florianópolis", "79", datetime.today()),\
					("UNESP Rio Claro", "UNESP Rio Claro", "NGO", "BR", "Florianópolis", "11", datetime.today()),\
					("University of Toronto", "University of Toronto", "HEI", "CA", "Toronto", "25", datetime.today()),\
					("Trent University", "Trent University", "HEI", "CA", "Trent", "68", datetime.today()),\
					("Queen's University, Kingtson, Ontario", "Queen's University, Kingtson, Ontario", "HEI", "CA", "Kingston", "42", datetime.today()),\
					("University of British Columbia", "University of British Columbia", "HEI", "CA", "Vancouver", "2", datetime.today()),\
					("McGill University", "McGill University", "HEI", "CA", "Montreal", "13", datetime.today()),\
					("McGill University", "McGill University", "HEI", "CA", "Montreal", "43", datetime.today()),\
					("European Organisation for Nuclear Research (CERN)", "European Organisation for Nuclear Research (CERN)", "RES", "CH", "Lucerne", "64", datetime.today()),\
					("University of Lucerne", "University of Lucerne", "HEI", "CH", "Lucerne", "58", datetime.today()),\
					("Lucerne University of Applied Sciences and Arts", "Lucerne University of Applied Sciences and Arts", "HEI", "CH", "Lucerne", "51", datetime.today()),\
					("Université de Genève", "Université de Genève", "HEI", "CH", "Geneva", "35", datetime.today()),\
					("Lausanne EPFL", "Lausanne EPFL", "HEI", "CH", "Lausanne", "55", datetime.today()),\
					("ETH Zurich", "ETH Zurich", "HEI", "CH", "Zurich", "26", datetime.today()),\
					("Scuola Universitaria Professionale della Svizzera Italiana", "Scuola Universitaria Professionale della Svizzera Italiana", "HEI", "CH", "Manno", "8", datetime.today()),\
					("Universität Basel", "Universität Basel", "HEI", "CH", "Basel", "62", datetime.today()),\
					("Fundacion Chile", "Fundacion Chile", "HEI", "CL", "Santiago", "27", datetime.today()),\
					("Pontificia Universidad Catolica de Chile", "Pontificia Universidad Catolica de Chile", "HEI", "CL", "Santiago", "5", datetime.today()),\
					("National Commission for Scientific and Technological Research (CONICYT)", "National Commission for Scientific and Technological Research (CONICYT)", "RES", "CL", "Santiago", "101", datetime.today()),\
					("Huawei Technologies", "Huawei Technologies", "RES", "CN", "Peking", "55", datetime.today()),\
					("Dalian University of Technology", "Dalian University of Technology", "HEI", "CN", "Dalian", "33", datetime.today()),\
					("Shenzhen University", "Shenzhen University", "HEI", "CN", "Shenzhen", "93", datetime.today()),\
					("China Beijing Environmental Exchange", "China Beijing Environmental Exchange", "NGO", "CN", "Beijing", "2", datetime.today()),\
					("Donghua University", "Donghua University", "HEI", "CN", "Shanghai", "44", datetime.today()),\
					("National Supercomputer Centre Guangzhou", "National Supercomputer Centre Guangzhou", "NGO", "CN", "Guangzhou", "43", datetime.today()),\
					("Nanjing University of Aeronautics and Astronautics", "Nanjing University of Aeronautics and Astronautics", "HEI", "CN", "Nanjing", "50", datetime.today()),\
					("Peking University", "Peking University", "HEI", "CN", "Peking", "101", datetime.today()),\
					("Peking University", "Peking University", "HEI", "CN", "Peking", "58", datetime.today()),\
					("Peking University", "Peking University", "HEI", "CN", "Peking", "50", datetime.today()),\
					("Shanghai Jiao Tong University", "Shanghai Jiao Tong University", "HEI", "CN", "Shanghai", "9", datetime.today()),\
					("Jilin University", "Jilin University", "HEI", "CN", "Jilin", "57", datetime.today()),\
					("October Literature Institute of Beijing Publishing Group", "October Literature Institute of Beijing Publishing Group", "NGO", "CN", "Beijing", "6", datetime.today()),\
					("Fudan University", "Fudan University", "HEI", "CN", "Fudan", "48", datetime.today()),\
					("Chinese Academy of Governance", "Chinese Academy of Governance", "GOV", "CN", "Beijing", "52", datetime.today()),\
					("Donghua University", "Donghua University", "HEI", "CN", "Shanghai", "60", datetime.today()),\
					("China Graduate School of Theology", "China Graduate School of Theology", "HEI", "CN", "Shanghai", "101", datetime.today()),\
					("Shandong University", "Shandong University", "HEI", "CN", "Shandong", "9", datetime.today()),\
					("Shanghai University of Finance and Economics ", "Shanghai University of Finance and Economics ", "HEI", "CN", "Shanghai", "9", datetime.today()),\
					("Shanghai Jiao Tong University", "Shanghai Jiao Tong University", "HEI", "CN", "Shanghai", "50", datetime.today()),\
					("Huazhong University of Science and Technology", "Huazhong University of Science and Technology", "HEI", "CN", "Huazhong", "101", datetime.today()),\
					("Fudan University", "Fudan University", "HEI", "CN", "Fudan", "51", datetime.today()),\
					("Liaoning Shihua University, Fushin", "Liaoning Shihua University, Fushin", "HEI", "CN", "Fushin", "38", datetime.today()),\
					("Tianjin University", "Tianjin University", "HEI", "CN", "Tianjin", "42", datetime.today()),\
					("Harbin Engineering University", "Harbin Engineering University", "HEI", "CN", "Harbin", "50", datetime.today()),\
					("Nanjing University of Aeronautics and Astronautics", "Nanjing University of Aeronautics and Astronautics", "HEI", "CN", "Nanjing", "79", datetime.today()),\
					("North China Electric Power University", "North China Electric Power University", "HEI", "CN", "Beijing", "10", datetime.today()),\
					("Dalian University of Technology", "Dalian University of Technology", "HEI", "CN", "Dalian", "5", datetime.today()),\
					("Dalian University of Technology", "Dalian University of Technology", "HEI", "CN", "Dalian", "5", datetime.today()),\
					("South China University of Technology, Guangzhou", "South China University of Technology, Guangzhou", "HEI", "CN", "Guangzhou", "81", datetime.today()),\
					("Beihang University", "Beihang University", "HEI", "CN", "Beihang", "101", datetime.today()),\
					("Peking University", "Peking University", "HEI", "CN", "Peking", "101", datetime.today()),\
					("China Agricultural University", "China Agricultural University", "HEI", "CN", "Peking", "25", datetime.today()),\
					("East China University of Science and Technology", "East China University of Science and Technology", "HEI", "CN", "Beijing", "43", datetime.today()),\
					("China Scholarships Council", "China Scholarships Council", "NGO", "CN", "Shanghai", "13", datetime.today()),\
					("Nanjing University", "Nanjing University", "HEI", "CN", "Nanjing", "78", datetime.today()),\
					("Renmin University of China", "Renmin University of China", "HEI", "CN", "Renmin", "30", datetime.today()),\
					("Liaoning Shihua University, Fushin", "Liaoning Shihua University, Fushin", "HEI", "CN", "Fushin", "69", datetime.today()),\
					("University of  Hong Kong", "University of  Hong Kong", "HEI", "HK", "Hong Kong", "20", datetime.today()),\
					("Fudan University", "Fudan University", "HEI", "CN", "Fudan", "25", datetime.today()),\
					("Peking University", "Peking University", "HEI", "CN", "Peking", "101", datetime.today()),\
					("Universidad del Rosario", "Universidad del Rosario", "HEI", "CO", "Bogotá", "66", datetime.today()),\
					("National University of Colombia", "National University of Colombia", "HEI", "CO", "Bogotá", "88", datetime.today()),\
					("COLFUTURO", "COLFUTURO", "NGO", "CO", "Bogotá", "37", datetime.today()),\
					("Agricultural Research Institute, Cyprus", "Agricultural Research Institute, Cyprus", "RES", "CY", "Nicosia", "30", datetime.today()),\
					("Cyprus University", "Cyprus University", "HEI", "CY", "Nicosia", "99", datetime.today()),\
					("Charles Universitry Prague", "Charles Universitry Prague", "HEI", "CZ", "Prague", "20", datetime.today()),\
					("University of Economics, Prague", "University of Economics, Prague", "HEI", "CZ", "Prague", "26", datetime.today()),\
					("Academy of Arts, Architecture & Design in Prague", "Academy of Arts, Architecture & Design in Prague", "HEI", "CZ", "Prague", "67", datetime.today()),\
					("Johannes Gutenberg Universitaet, Mainz", "Johannes Gutenberg Universitaet, Mainz", "HEI", "DE", "Mainz", "93", datetime.today()),\
					("Georg-August-Universität Göttingen", "Georg-August-Universität Göttingen", "HEI", "DE", "Gottingen", "62", datetime.today()),\
					("Technical University of Munich", "Technical University of Munich", "HEI", "DE", "Munich", "50", datetime.today()),\
					("National Centre for Biological Sciences, KTH Royal Institute of Technology", "National Centre for Biological Sciences, KTH Royal Institute of Technology", "HEI", "DE", "Cologne", "99", datetime.today()),\
					("Leiden University", "Leiden University", "HEI", "NL", "Leiden", "93", datetime.today()),\
					("Ludwig-Maximillians University Munich", "Ludwig-Maximillians University Munich", "HEI", "DE", "Munich", "14", datetime.today()),\
					("Saarland University", "Saarland University", "HEI", "DE", "Saarbrücken", "82", datetime.today()),\
					("Trier University", "Trier University", "HEI", "DE", "Trier", "3", datetime.today()),\
					("Augsburg University", "Augsburg University", "HEI", "DE", "Augsburg", "58", datetime.today()),\
					("Bayreuth University", "Bayreuth University", "HEI", "DE", "Bayreuth", "8", datetime.today()),\
					("Bielefeld University", "Bielefeld University", "HEI", "DE", "Bielefeld", "16", datetime.today()),\
					("University of Cologne", "University of Cologne", "HEI", "DE", "Cologne", "85", datetime.today()),\
					("Freiburg University", "Freiburg University", "HEI", "DE", "Freiburg", "45", datetime.today()),\
					("Freie University Berlin", "Freie University Berlin", "HEI", "DE", "Berlin", "32", datetime.today()),\
					("Heidelberg University", "Heidelberg University", "HEI", "DE", "Heidelberg", "54", datetime.today()),\
					("Leipzig University", "Leipzig University", "HEI", "DE", "Leipzig", "57", datetime.today()),\
					("Universität Mannheim", "Universität Mannheim", "HEI", "DE", "Mannheim", "72", datetime.today()),\
					("University of Cologne", "University of Cologne", "HEI", "DE", "Cologne", "40", datetime.today()),\
					("Hochschule fur Technik Stuttgart", "Hochschule fur Technik Stuttgart", "HEI", "DE", "Stuttgart", "66", datetime.today()),\
					("Leibniz University Hannover", "Leibniz University Hannover", "HEI", "DE", "Hannover", "71", datetime.today()),\
					("Hochschule für Wirtschaft und Recht Berlin", "Hochschule für Wirtschaft und Recht Berlin", "HEI", "DE", "Berlin", "92", datetime.today()),\
					("Frankfurt School of Finance & Management", "Frankfurt School of Finance & Management", "HEI", "DE", "Frankfurt", "8", datetime.today()),\
					("Georg-August-Universität Göttingen", "Georg-August-Universität Göttingen", "HEI", "DE", "Gottingen", "63", datetime.today()),\
					("Technical University of Munich", "Technical University of Munich", "HEI", "DE", "Munich", "96", datetime.today()),\
					("Humboldt Universität Berlin", "Humboldt Universität Berlin", "HEI", "DE", "Berlin", "90", datetime.today()),\
					("TU Kaiserslautern", "TU Kaiserslautern", "HEI", "DE", "Kaiserslautern", "19", datetime.today()),\
					("TU Berlin", "TU Berlin", "HEI", "DE", "Berlin", "8", datetime.today()),\
					("Eberhard Karls Universität Tübingen", "Eberhard Karls Universität Tübingen", "HEI", "DE", "Tubingen", "30", datetime.today()),\
					("Berlin Weisensee School of Art", "Berlin Weisensee School of Art", "HEI", "DE", "Berlin", "30", datetime.today()),\
					("Academy of Fine Art, Munich", "Academy of Fine Art, Munich", "HEI", "DE", "Munich", "44", datetime.today()),\
					("Academy of Fine Art, ABK, Stuttgart", "Academy of Fine Art, ABK, Stuttgart", "HEI", "DE", "Stuttgart", "21", datetime.today()),\
					("Jacobs University Bremen", "Jacobs University Bremen", "HEI", "DE", "Bremen", "94", datetime.today()),\
					("Università Ca' Foscari Venezia", "Università Ca' Foscari Venezia", "HEI", "IT", "Venice", "95", datetime.today()),\
					("Staatliche Akademie der Bildenden Künste", "Staatliche Akademie der Bildenden Künste", "NGO", "DE", "Berlin", "100", datetime.today()),\
					("Copenhagen Business School", "Copenhagen Business School", "HEI", "DK", "Copenhagen", "8", datetime.today()),\
					("University of Copenhagen", "University of Copenhagen", "HEI", "DK", "Copenhagen", "32", datetime.today()),\
					("Danish Design School", "Danish Design School", "HEI", "DK", "Copenhagen", "9", datetime.today()),\
					("Royal Danish Academy of Fine Arts", "Royal Danish Academy of Fine Arts", "HEI", "DK", "Copenhagen", "3", datetime.today()),\
					("SENESCYT", "SENESCYT", "NGO", "EC", "Azogues", "65", datetime.today()),\
					("Ministry of Electricity and Renewabel Energy", "Ministry of Electricity and Renewabel Energy", "NGO", "EC", "Azogues", "29", datetime.today()),\
					("Estonian Academy of Arts", "Estonian Academy of Arts", "HEI", "EE", "Tartu", "56", datetime.today()),\
					("Tallinn University", "Tallinn University", "HEI", "EE", "Tallinn", "22", datetime.today()),\
					("Sociedad Para El Impulso del Talento", "Sociedad Para El Impulso del Talento", "NGO", "ES", "Seville", "50", datetime.today()),\
					("Granada University", "Granada University", "HEI", "ES", "Granada", "17", datetime.today()),\
					("CEU", "CEU", "NGO", "ES", "Seville", "48", datetime.today()),\
					("Alcala University", "Alcala University", "HEI", "ES", "Alcala", "5", datetime.today()),\
					("Granada University", "Granada University", "HEI", "ES", "Granada", "96", datetime.today()),\
					("Extremadura University", "Extremadura University", "HEI", "ES", "Extremadura", "50", datetime.today()),\
					("University Pompeu Fabra", "University Pompeu Fabra", "HEI", "ES", "Madrid", "83", datetime.today()),\
					("Barcelona ESADE", "Barcelona ESADE", "HEI", "ES", "Barcelona", "26", datetime.today()),\
					("UP Catalunya", "UP Catalunya", "HEI", "ES", "Barcelona", "50", datetime.today()),\
					("Valladolid University", "Valladolid University", "HEI", "ES", "Valladolid", "50", datetime.today()),\
					("Universidad Pontificia Comillas de Madrid", "Universidad Pontificia Comillas de Madrid", "HEI", "ES", "Comillas de Madrid", "58", datetime.today()),\
					("Alcala University", "Alcala University", "HEI", "ES", "Alcala", "65", datetime.today()),\
					("Alicante University", "Alicante University", "HEI", "ES", "Alicante", "90", datetime.today()),\
					("Almeria University", "Almeria University", "HEI", "ES", "Almeria", "38", datetime.today()),\
					("Cantabria University", "Cantabria University", "HEI", "ES", "Cantabria", "56", datetime.today()),\
					("Granada University", "Granada University", "HEI", "ES", "Granada", "16", datetime.today()),\
					("Madrid Complutense University", "Madrid Complutense University", "HEI", "ES", "University", "49", datetime.today()),\
					("Malaga University", "Malaga University", "HEI", "ES", "Malaga", "89", datetime.today()),\
					("Navarra University", "Navarra University", "HEI", "ES", "Navarra", "36", datetime.today()),\
					("Salamanca University", "Salamanca University", "HEI", "ES", "Salamanca", "19", datetime.today()),\
					("Seville University", "Seville University", "HEI", "ES", "Seville", "59", datetime.today()),\
					("Autonomous University of Barcelona", "Autonomous University of Barcelona", "HEI", "ES", "Barcelona", "26", datetime.today()),\
					("Universidad de Deusto", "Universidad de Deusto", "HEI", "ES", "Deusto", "89", datetime.today()),\
					("Rovira i Virgili University", "Rovira i Virgili University", "HEI", "ES", "Barcelona", "18", datetime.today()),\
					("Universidad CEU San Pablo", "Universidad CEU San Pablo", "HEI", "ES", "Barcelona", "36", datetime.today()),\
					("University of Helsinki", "University of Helsinki", "HEI", "FI", "Helsinki", "50", datetime.today()),\
					("Lahti University of Applied Sciences", "Lahti University of Applied Sciences", "HEI", "FI", "Lahti", "66", datetime.today()),\
					("Saimaa University of Applied Sciences", "Saimaa University of Applied Sciences", "HEI", "FI", "Saimaa", "40", datetime.today()),\
					("Institut Pasteur", "Institut Pasteur", "HEI", "FR", "Paris", "46", datetime.today()),\
					("Universite Joseph fourier Grenoble", "Universite Joseph fourier Grenoble", "HEI", "FR", "Grenoble", "94", datetime.today()),\
					("Ecole Nationale Supérieure des Mines de St Etienne", "Ecole Nationale Supérieure des Mines de St Etienne", "HEI", "FR", "St Etienne", "51", datetime.today()),\
					("Université de Franche-Comté", "Université de Franche-Comté, Besancon", "HEI", "FR", "Besancon", "14", datetime.today()),\
					("Université de Bourgogne", "Université de Bourgogne, Dijon", "HEI", "FR", "Dijon", "26", datetime.today()),\
					("Université de Bretagne Occidentale", "Université de Bretagne Occidentale, Brest", "HEI", "FR", "Brest", "101", datetime.today()),\
					("Ecole Nationale des Chartes", "Ecole Nationale des Chartes", "HEI", "FR", "Paris", "45", datetime.today()),\
					("EIVP Paris", "EIVP Paris", "HEI", "FR", "Paris", "68", datetime.today()),\
					("ENSC Lille", "ENSC Lille", "HEI", "FR", "Lille", "10", datetime.today()),\
					("ESSEC Business School, Paris", "ESSEC Business School, Paris", "HEI", "FR", "Paris", "52", datetime.today()),\
					("Université Pierre Mendes, Grenoble II", "Université Pierre Mendes, Grenoble II", "HEI", "FR", "Grenoble", "65", datetime.today()),\
					("Université Stendhal, Grenoble III", "Université Stendhal, Grenoble III", "HEI", "FR", "Grenoble", "50", datetime.today()),\
					("HEC Paris", "HEC Paris", "HEI", "FR", "HEC", "11", datetime.today()),\
					("IEP Grenoble", "IEP Grenoble", "HEI", "FR", "Grenoble", "93", datetime.today()),\
					("IEP Lyon", "IEP Lyon", "HEI", "FR", "Lyon", "53", datetime.today()),\
					("IEP Paris", "IEP Paris", "HEI", "FR", "Paris", "10", datetime.today()),\
					("IEP Rennes", "IEP Rennes", "HEI", "FR", "Rennes", "63", datetime.today()),\
					("Limoges University", "Limoges University", "HEI", "FR", "Limoges", "39", datetime.today()),\
					("Paris Dauphine University", "Paris Dauphine University", "HEI", "FR", "Paris", "63", datetime.today()),\
					("Paris I Pantheon Sorbonne", "Paris I Pantheon Sorbonne", "HEI", "FR", "Paris", "41", datetime.today()),\
					("Paris-Diderot Paris VII", "Paris-Diderot Paris VII", "HEI", "FR", "Paris", "98", datetime.today()),\
					("Université Pierre et Marie Curie, Paris", "Université Pierre et Marie Curie, Paris", "HEI", "FR", "Paris", "91", datetime.today()),\
					("Rouen Business School", "Rouen Business School", "HEI", "FR", "Rouen", "94", datetime.today()),\
					("Rouen University", "Rouen University", "HEI", "FR", "Rouen", "37", datetime.today()),\
					("Strasbourg University", "Strasbourg University", "HEI", "FR", "Strasbourg", "28", datetime.today()),\
					("Université de Toulouse II - Le Mirail", "Université de Toulouse II - Le Mirail", "HEI", "FR", "Toulouse", "72", datetime.today()),\
					("Tours Francois Rabelais University", "Tours Francois Rabelais University", "HEI", "FR", "Tours", "91", datetime.today()),\
					("Université Paris-Sorbonne (Paris IV)", "Université Paris-Sorbonne (Paris IV)", "HEI", "FR", "Paris", "73", datetime.today()),\
					("Université Paris Ouest - Nanterre La Défense", "Université Paris Ouest - Nanterre La Défense", "HEI", "FR", "Paris", "29", datetime.today()),\
					("Université Paris-Est Créteil Val-de-Marne", "Université Paris-Est Créteil Val-de-Marne", "HEI", "FR", "Paris", "99", datetime.today()),\
					("ISIT Paris", "ISIT Paris", "HEI", "FR", "Paris", "24", datetime.today()),\
					("Université Joseph Fourier, Grenoble I", "Université Joseph Fourier, Grenoble I", "HEI", "FR", "Grenoble", "81", datetime.today()),\
					("Université Paris 1 - Panthéon Sorbonne", "Université Paris 1 - Panthéon Sorbonne", "HEI", "FR", "Paris", "68", datetime.today()),\
					("Ecole Nationale Supérieure du Paysage, Versailles", "Ecole Nationale Supérieure du Paysage, Versailles", "HEI", "FR", "Versailles", "11", datetime.today()),\
					("Universite Paris", "Universite Paris", "HEI", "FR", "Paris", "89", datetime.today()),\
					("Ecole Nationale Supérieure des Arts Decoratifs (ENSAD)", "Ecole Nationale Supérieure des Arts Decoratifs (ENSAD) Paris", "HEI", "FR", "Paris", "38", datetime.today()),\
					("Haute école des arts du Rhin", "Haute école des arts du Rhin", "HEI", "FR", "Rhin", "12", datetime.today()),\
					("CUFR Jean-François Champollion", "CUFR Jean-François Champollion", "NGO", "FR", "Albi,", "20", datetime.today()),\
					("Euromed Marseille Ecole De Management", "Euromed Marseille Ecole De Management", "HEI", "FR", "Marseille", "60", datetime.today()),\
					("Université de Haute Alsace", "Université de Haute Alsace", "HEI", "FR", "Alsace", "85", datetime.today()),\
					("Aix-Marseille Université", "Aix-Marseille Université", "HEI", "FR", "Marseille", "27", datetime.today()),\
					("Université de Montpellier III", "Université de Montpellier III", "HEI", "FR", "Montpellier", "28", datetime.today()),\
					("University of Nantes", "University of Nantes", "HEI", "FR", "Nantes", "47", datetime.today()),\
					("Universite Sorbonne Nouvelle - Paris 3", "Universite Sorbonne Nouvelle - Paris 3", "HEI", "FR", "Paris", "69", datetime.today()),\
					("Arcadia University", "Arcadia University", "HEI", "GB", "London", "46", datetime.today()),\
					("Aristotle University of Thessaloniki", "Aristotle University of Thessaloniki", "HEI", "GR", "Athens", "67", datetime.today()),\
					("City University of Hong Kong", "City University of Hong Kong", "HEI", "HK", "Hong Kong", "31", datetime.today()),\
					("Government of Hong Kong", "Government of Hong Kong Special Administrative Region of the PRC", "GOV", "HK", "Hong Kong", "48", datetime.today()),\
					("Kadoorie Farm and Botanic Garden Corporation", "Kadoorie Farm and Botanic Garden Corporation", "NGO", "HK", "Hong Kong", "85", datetime.today()),\
					("Brown University", "Brown University", "HEI", "HK", "Hong Kong", "71", datetime.today()),\
					("Pazmany Peter Catholic University", "Pazmany Peter Catholic University", "HEI", "HU", "Budapest", "22", datetime.today()),\
					("University of Szeged", "University of Szeged", "HEI", "HU", "Budapest", "12", datetime.today()),\
					("Hungarian Academy of Fine Art, Budapest", "Hungarian Academy of Fine Art, Budapest", "HEI", "HU", "Budapest", "34", datetime.today()),\
					("Corvinus University of Budapest", "Corvinus University of Budapest", "HEI", "HU", "Budapest", "23", datetime.today()),\
					("University College Dublin", "University College Dublin", "HEI", "IE", "Dublin", "11", datetime.today()),\
					("University College Cork", "University College Cork", "HEI", "IE", "Cork", "52", datetime.today()),\
					("University College Dublin", "University College Dublin", "HEI", "IE", "Dublin", "35", datetime.today()),\
					("Hebrew University Medical Centre", "Hebrew University of Jerusalem, Hebrew University Medical Centre", "HEI", "IL", "Jerusalem", "4", datetime.today()),\
					("The National Centre for Biological Sciences (NCBS)", "The National Centre for Biological Sciences (NCBS)", "NGO", "IN", "Mumbai", "57", datetime.today()),\
					("Indian Institute of Technology Madras", "Indian Institute of Technology Madras", "HEI", "IN", "Mumbai", "101", datetime.today()),\
					("Indian Institute of Technology, Bombay", "Indian Institute of Technology, Bombay", "HEI", "IN", "Mumbai", "42", datetime.today()),\
					("Commonwealth Veterinary Association", "Commonwealth Veterinary Association", "NGO", "IN", "Mumbai", "84", datetime.today()),\
					("Indian Council of Agricultural Research", "Indian Council of Agricultural Research", "RES", "IN", "Mumbai", "37", datetime.today()),\
					("ESSO-National Institute of Ocean Technology", "National Institute of Ocean Technology, Min. of Earth Sciences, Govt. of India", "GOV", "IN", "Mumbai", "42", datetime.today()),\
					("Anna University", "Anna University", "HEI", "IN", "Mumbai", "92", datetime.today()),\
					("Indian Institute of Ahmedabad", "Indian Institute of Ahmedabad", "HEI", "IN", "Mumbai", "52", datetime.today()),\
					("Tata Institute of Social Science", "Tata Institute of Social Science", "HEI", "IN", "Mumbai", "81", datetime.today()),\
					("SRM University", "SRM University", "HEI", "IN", "Mumbai", "66", datetime.today()),\
					("VIT University", "VIT University", "HEI", "IN", "Mumbai", "44", datetime.today()),\
					("NCBS", "NCBS", "NGO", "IN", "Mumbai", "19", datetime.today()),\
					("British Education Centre", "British Education Centre", "NGO", "IN", "Mumbai", "8", datetime.today()),\
					("Wellspring Healthcare Private Ltd.", "Wellspring Healthcare Private Ltd.", "NGO", "IN", "Mumbai", "16", datetime.today()),\
					("The Karta Initiative", "The Karta Initiative", "NGO", "IN", "Mumbai", "39", datetime.today()),\
					("Somaiya Vidyavihar", "Somaiya Vidyavihar", "NGO", "IN", "Mumbai", "88", datetime.today()),\
					("Jadavpur University", "Jadavpur University", "HEI", "IN", "Mumbai", "11", datetime.today()),\
					("Presidency University", "Presidency University", "HEI", "IN", "Mumbai", "44", datetime.today()),\
					("Salaam Baalak Trust", "Salaam Baalak Trust", "NGO", "IN", "Mumbai", "79", datetime.today()),\
					("Indian Institute for Financial Management Research", "Indian Institute for Financial Management Research", "RES", "IN", "Mumbai", "64", datetime.today()),\
					("Anna University", "Anna University", "HEI", "IN", "Mumbai", "18", datetime.today()),\
					("PES University ", "PES University ", "HEI", "IN", "Mumbai", "50", datetime.today()),\
					("University of Delhi", "University of Delhi", "HEI", "IN", "Delhi", "55", datetime.today()),\
					("Christian Medical College Vellore", "Christian Medical College Vellore", "HEI", "IN", "Delhi", "98", datetime.today()),\
					("Veterinary Council of India", "Veterinary Council of India", "HEI", "IN", "Delhi", "38", datetime.today()),\
					("The Institute for Research in Reproduction", "Indian Institute for Research in Reproduction", "RES", "IN", "Delhi", "41", datetime.today()),\
					("Srishti School of Art Design and Technology", "Srishti School of Art Design and Technology", "NGO", "IN", "Delhi", "35", datetime.today()),\
					("United Theological College", "United Theological College", "HEI", "IN", "Delhi", "94", datetime.today()),\
					("University of Iceland", "University of Iceland", "HEI", "IS", "Reykjavik", "53", datetime.today()),\
					("Iceland Academy of the Arts", "Iceland Academy of the Arts", "HEI", "IS", "Reykjavik", "97", datetime.today()),\
					("Università degli Studi di Cagliari", "Università degli Studi di Cagliari", "HEI", "IT", "Cagliari", "50", datetime.today()),\
					("University of Naples", "University of Naples", "HEI", "IT", "Naples", "15", datetime.today()),\
					("Bologna University", "Bologna University", "HEI", "IT", "Bologna", "17", datetime.today()),\
					("Milan University", "Milan University", "HEI", "IT", "Milan", "87", datetime.today()),\
					("Milano Bocconi Commercial University", "Milano Bocconi Commercial University", "HEI", "IT", "Milan", "94", datetime.today()),\
					("Sapienza University of Rome", "Sapienza University of Rome", "HEI", "IT", "Rome", "66", datetime.today()),\
					("Trento University", "Trento University", "HEI", "IT", "Trento", "11", datetime.today()),\
					("Verona University", "Verona University", "HEI", "IT", "Verona", "18", datetime.today()),\
					("Università di Napoli L¿Orientale", "Università di Napoli L¿Orientale", "HEI", "IT", "Naples", "75", datetime.today()),\
					("Universita' di Catania", "Universita' di Catania", "HEI", "IT", "Catania", "37", datetime.today()),\
					("Università degli studi di Firenze", "Università degli studi di Firenze", "HEI", "IT", "Florence", "69", datetime.today()),\
					("University of Macerata", "University of Macerata", "HEI", "IT", "Macerata", "100", datetime.today()),\
					("Università Ca' Foscari Venezia", "Università Ca' Foscari Venezia", "HEI", "IT", "Venice", "55", datetime.today()),\
					("Siena University", "Siena University", "HEI", "IT", "Siena", "5", datetime.today()),\
					("Università di Genova", "Università di Genova", "HEI", "IT", "Genova", "20", datetime.today()),\
					("Conservatorio Di Musica Niccolò Paganini", "Conservatorio Di Musica Niccolò Paganini", "HEI", "IT", "Milan", "93", datetime.today()),\
					("Universita di Roma Tre", "Universita di Roma Tre", "HEI", "IT", "Rome", "76", datetime.today()),\
					("Nagasaki University", "Nagasaki University", "HEI", "JP", "Nagasaki", "9", datetime.today()),\
					("Hiroshima University", "Hiroshima University", "HEI", "JP", "Hiroshima", "6", datetime.today()),\
					("Nagoya University", "Nagoya University", "HEI", "JP", "Nagoya", "70", datetime.today()),\
					("National Museum of Ethnology (Minpaku)", "National Museum of Ethnology (Minpaku)", "NGO", "JP", "Minpaku", "59", datetime.today()),\
					("Nagasaki University", "Nagasaki University", "HEI", "JP", "Nagasaki", "32", datetime.today()),\
					("REINKEI", "REINKEI", "NGO", "JP", "Tokyo", "54", datetime.today()),\
					("Osaka University", "Osaka University", "HEI", "JP", "Osaka", "97", datetime.today()),\
					("Keio University", "Keio University", "HEI", "JP", "Keio", "57", datetime.today()),\
					("Osaka University", "Osaka University", "HEI", "JP", "Osaka", "56", datetime.today()),\
					("University of Tokyo", "University of Tokyo", "HEI", "JP", "Tokyo", "53", datetime.today()),\
					("Waseda University", "Waseda University", "HEI", "JP", "Tokyo", "16", datetime.today()),\
					("International Christian University Tokyo", "International Christian University Tokyo", "HEI", "JP", "Tokyo", "13", datetime.today()),\
					("Hiko Mizuno College of Jewelry", "Hiko Mizuno College of Jewelry", "HEI", "JP", "Tokyo", "8", datetime.today()),\
					("Doshisha University", "Doshisha University", "HEI", "JP", "Doshisha", "23", datetime.today()),\
					("Kyoto University", "Kyoto University", "HEI", "JP", "Kyoto", "3", datetime.today()),\
					("Gakushuin University", "Gakushuin University", "HEI", "JP", "Gakushuin", "30", datetime.today()),\
					("Hokkaido University ", "Hokkaido University ", "HEI", "JP", "Hokkaido", "75", datetime.today()),\
					("International Christian University Tokyo", "International Christian University Tokyo", "HEI", "JP", "Tokyo", "67", datetime.today()),\
					("Okayama University", "Okayama University", "HEI", "JP", "Okayama", "80", datetime.today()),\
					("Kwansei Gakuin University", "Kwansei Gakuin University", "HEI", "JP", "Tokyo", "79", datetime.today()),\
					("Nanzan University", "Nanzan University", "HEI", "JP", "Nanzan", "87", datetime.today()),\
					("Ritsumeikan University", "Ritsumeikan University", "HEI", "JP", "Ritsumeikan", "100", datetime.today()),\
					("Seikei University", "Seikei University", "HEI", "JP", "Seikei", "83", datetime.today()),\
					("Sophia University", "Sophia University", "HEI", "JP", "Sophia", "73", datetime.today()),\
					("Tskuba University", "Tskuba University", "HEI", "JP", "Tskuba", "62", datetime.today()),\
					("Yokohama National University", "Yokohama National University", "HEI", "JP", "Yokohama", "48", datetime.today()),\
					("Kenyan Association of Independent International Schools", "Kenyan Association of Independent International Schools", "NGO", "KE", "Nairobi", "101", datetime.today()),\
					("Egerton University ", "Egerton University ", "HEI", "KE", "Nairobi", "60", datetime.today()),\
					("Hankuk University of Foreign Studies", "Hankuk University of Foreign Studies", "HEI", "KR", "Seoul", "41", datetime.today()),\
					("Kookmin University", "Kookmin University", "HEI", "KR", "Seoul", "95", datetime.today()),\
					("Korea University", "Korea University", "HEI", "KR", "Seoul", "51", datetime.today()),\
					("Konkuk University", "Konkuk University", "HEI", "KR", "Seoul", "43", datetime.today()),\
					("Vilnius Academy of Fine Arts", "Vilnius Academy of Fine Arts", "HEI", "LT", "Vilnius", "37", datetime.today()),\
					("The Ministry of Education and Science, Macedonia", "The Ministry of Education and Science, Macedonia", "NGO", "MK", "Skopje", "33", datetime.today()),\
					("University of Malta", "University of Malta", "HEI", "MT", "Valletta", "42", datetime.today()),\
					("University of Malta", "University of Malta", "HEI", "MT", "Valletta", "83", datetime.today()),\
					("Lilongwe University of Agriculture & Nataural Resources", "Lilongwe University of Agriculture & Nataural Resources", "HEI", "MW", "Lilongwe", "52", datetime.today()),\
					("Royal College of Surgeons of Edinburgh", "Royal College of Surgeons of Edinburgh", "HEI", "MW", "Lilongwe", "20", datetime.today()),\
					("The Center of Research and Teaching in Economics, Mexico City", "The Center of Research and Teaching in Economics, Mexico City", "RES", "MX", "Mexico City", "77", datetime.today()),\
					("El Colegio de Mexico", "El Colegio de Mexico", "HEI", "MX", "Mexico City", "75", datetime.today()),\
					("Latin American Institute of Educational Communication", "Latin American Institute of Educational Communication", "HEI", "MX", "Mexico City", "38", datetime.today()),\
					("Tecnologico de Monterrey", "Tecnologico de Monterrey", "HEI", "MX", "Monterrey", "78", datetime.today()),\
					("Universidad LaSalle", "Universidad LaSalle", "HEI", "MX", "Mexico City", "10", datetime.today()),\
					("Universidad Nacional Autónoma de México", "Universidad Nacional Autónoma de México", "HEI", "MX", "Guadalajara", "25", datetime.today()),\
					("University of Guadalajara", "University of Guadalajara", "HEI", "MX", "Guadalajara", "43", datetime.today()),\
					("Universidad Nacional Autónoma de México", "Universidad Nacional Autónoma de México", "HEI", "MX", "Guadalajara", "41", datetime.today()),\
					("Fund for Human Resource Development (FIDERH)", "Fund for Human Resource Development (FIDERH)", "NGO", "MX", "Guadalajara", "41", datetime.today()),\
					("Universidad National Autonoma", "Universidad National Autonoma", "HEI", "MX", "Autonoma", "4", datetime.today()),\
					("FUNED", "FUNED", "NGO", "MX", "Xio de Janiean", "45", datetime.today()),\
					("Universidad de las Americas Puebla", "Universidad de las Americas Puebla", "HEI", "MX", "Americas Puebla", "57", datetime.today()),\
					("University of Malaya", "University of Malaya", "HEI", "MY", "Malaya", "56", datetime.today()),\
					("ICLARM (Worldfish)", "ICLARM (Worldfish)", "NGO", "MY", "ICLARM", "31", datetime.today()),\
					("International Medical University", "International Medical University", "HEI", "MY", "University", "42", datetime.today()),\
					("Universiti Tun Abdul Razak", "Universiti Tun Abdul Razak", "HEI", "MY", "Vknrazkver", "34", datetime.today()),\
					("University of the Caribbean Coast of Nicaragua", "University of the Caribbean Coast of Nicaragua", "HEI", "NI", "Florianópolis", "48", datetime.today()),\
					("Groningen University", "Groningen University", "HEI", "NL", "Groningen", "50", datetime.today()),\
					("Nijmegen Radboud University", "Nijmegen Radboud University", "HEI", "NL", "University", "71", datetime.today()),\
					("University of Amsterdam", "University of Amsterdam", "HEI", "NL", "Amsterdam", "48", datetime.today()),\
					("Leiden University", "Leiden University", "HEI", "NL", "Leiden", "52", datetime.today()),\
					("Maastricht University", "Maastricht University", "HEI", "NL", "Maastricht", "87", datetime.today()),\
					("Tilburg University", "Tilburg University", "HEI", "NL", "Tilburg", "33", datetime.today()),\
					("Utrecht University", "Utrecht University", "HEI", "NL", "Utrecht", "47", datetime.today()),\
					("Amsterdam Academy of Architecture", "Amsterdam Academy of Architecture", "HEI", "NL", "Tturemarciter", "72", datetime.today()),\
					("Amsterdam Fashion Institute", "Amsterdam Fashion Institute", "HEI", "NL", "Institute", "24", datetime.today()),\
					("Tromso University", "Tromso University", "HEI", "NO", "Tromso", "67", datetime.today()),\
					("Bergen University", "Bergen University", "HEI", "NO", "Bergen", "16", datetime.today()),\
					("Norwegian School of Veterinary Science", "Norwegian School of Veterinary Science", "HEI", "NO", "Veterinary Science", "48", datetime.today()),\
					("Oslo University", "Oslo University", "HEI", "NO", "Oslo", "43", datetime.today()),\
					("Norwegian National University for Science and Technology", "Norwegian National University for Science and Technology", "HEI", "NO", "Oslo", "88", datetime.today()),\
					("Tribuvan University, Forest Action Nepal", "Tribuvan University, Forest Action Nepal", "HEI", "NP", "Action Nepal", "45", datetime.today()),\
					("Unitec Institute of Technology", "Unitec Institute of Technology", "HEI", "NZ", "Tyntechotec", "33", datetime.today()),\
					("University of Auckland", "University of Auckland", "HEI", "NZ", "Auckland", "68", datetime.today()),\
					("University of Otago", "University of Otago", "HEI", "NZ", "Otago", "28", datetime.today()),\
					("Massey University", "Massey University", "HEI", "NZ", "Massey", "28", datetime.today()),\
					("Higher Education Commission", "Higher Education Commission", "NGO", "PK", "Commission", "94", datetime.today()),\
					("Medical University of Lodz", "Medical University of Lodz", "HEI", "PL", "Izelozica", "63", datetime.today()),\
					("Poznan University of Medical Sciences ", "Poznan University of Medical Sciences ", "HEI", "PL", "Medical Sciences", "31", datetime.today()),\
					("Jagiellonian University Medical College", "Jagiellonian University Medical College", "HEI", "PL", "Ial Collegeaceiel", "37", datetime.today()),\
					("Wroclaw Medical University", "Wroclaw Medical University", "HEI", "PL", "University", "32", datetime.today()),\
					("Medical University of Gdansk", "Medical University of Gdansk", "HEI", "PL", "Ikegdnica", "38", datetime.today()),\
					("Medical University of Lublin", "Medical University of Lublin", "HEI", "PL", "Inelulica", "65", datetime.today()),\
					("University of Gdansk", "University of Gdansk", "HEI", "PL", "Gdansk", "71", datetime.today()),\
					("Pedagogical University of Cracow", "Pedagogical University of Cracow", "HEI", "PL", "Acowe ago", "73", datetime.today()),\
					("Warsaw University", "Warsaw University", "HEI", "PL", "Warsaw", "40", datetime.today()),\
					("Warsaw University", "Warsaw University", "HEI", "PL", "Warsaw", "89", datetime.today()),\
					("Birzeit University", "Birzeit University", "HEI", "PS", "Birzeit", "63", datetime.today()),\
					("University of Porto", "University of Porto", "HEI", "PT", "Porto", "4", datetime.today()),\
					("University of Coimbra", "University of Coimbra", "HEI", "PT", "Coimbra", "84", datetime.today()),\
					("Qatari Cultural Attache", "Qatari Cultural Attache", "NGO", "QA", "Attache", "32", datetime.today()),\
					("Timisoara Polytechnic University", "Timisoara Polytechnic University", "HEI", "RO", "University", "26", datetime.today()),\
					("The Ministry of Higher Education, Saudi", "The Ministry of Higher Education, Saudi", "NGO", "SA", "Seoul", "40", datetime.today()),\
					("Prince Sultan University", "Prince Sultan University", "HEI", "SA", "University", "35", datetime.today()),\
					("Karolinska Institutet", "Karolinska Institutet", "HEI", "SE", "Karolinska", "88", datetime.today()),\
					("Gothenburg Chalmers University of Technology", "Gothenburg Chalmers University of Technology", "HEI", "SE", "University of Technology", "29", datetime.today()),\
					("Stockholm University", "Stockholm University", "HEI", "SE", "Stockholm", "55", datetime.today()),\
					("Lund University", "Lund University", "HEI", "SE", "Lund", "5", datetime.today()),\
					("University of Gothenburg", "University of Gothenburg", "HEI", "SE", "Gothenburg", "7", datetime.today()),\
					("Academy of  Principals Singapore", "Academy of  Principals Singapore", "NGO", "SG", "Dorecsndem", "35", datetime.today()),\
					("Nanyang Technological University", "Nanyang Technological University", "HEI", "SG", "University", "47", datetime.today()),\
					("Nanyang Technological University", "Nanyang Technological University", "HEI", "SG", "University", "49", datetime.today()),\
					("National University of Singapore", "National University of Singapore", "HEI", "SG", "Ioreasnion", "31", datetime.today()),\
					("Nanyang Technological University", "Nanyang Technological University", "HEI", "SG", "University", "35", datetime.today()),\
					("Srinakharinwirot University", "Srinakharinwirot University", "HEI", "TH", "Srinakharinwirot", "87", datetime.today()),\
					("Thammasat University", "Thammasat University", "HEI", "TH", "Thammasat", "45", datetime.today()),\
					("Karadeniz Technical University", "Karadeniz Technical University", "HEI", "TR", "University", "85", datetime.today()),\
					("Mimar Sinan Fine Arts University", "Mimar Sinan Fine Arts University", "HEI", "TR", "Arts University", "59", datetime.today()),\
					("Bo¿aziçi University", "Bo¿aziçi University", "HEI", "TR", "University", "70", datetime.today()),\
					("Cukurova University", "Cukurova University", "HEI", "TR", "Cukurova", "87", datetime.today()),\
					("Istanbul Bilgi University", "Istanbul Bilgi University", "HEI", "TR", "University", "82", datetime.today()),\
					("Bilkent University", "Bilkent University", "HEI", "TR", "Bilkent", "32", datetime.today()),\
					("Istanbul Technical University", "Istanbul Technical University", "HEI", "TR", "University", "9", datetime.today()),\
					("National Taiwan University", "National Taiwan University", "HEI", "TW", "University", "74", datetime.today()),\
					("Taipei Representative Office", "Taipei Representative Office", "RES", "TW", "Office", "8", datetime.today()),\
					("Mackay Medical College", "Mackay Medical College", "HEI", "TW", "College", "34", datetime.today()),\
					("National Taiwan University", "National Taiwan University", "HEI", "TW", "University", "72", datetime.today()),\
					("Kampala International University", "Kampala International University", "HEI", "UG", "University", "90", datetime.today()),\
					("Cornell University", "Cornell University", "HEI", "US", "Cornell", "36", datetime.today()),\
					("University of the People", "University of the People", "HEI", "US", "Venpeopleever", "88", datetime.today()),\
					("Pittsburg Theological Seminary", "Pittsburg Theological Seminary", "NGO", "US", "Seminary", "4", datetime.today()),\
					("University of the People", "University of the People", "HEI", "US", "Venpeopleever", "71", datetime.today()),\
					("University of Texas at Austin", "University of Texas at Austin", "HEI", "US", "Texas at Austin", "75", datetime.today()),\
					("Perkins School for the Blind", "Perkins School for the Blind", "NGO", "US", "School for the Blind", "48", datetime.today()),\
					("University of Western Carolina", "University of Western Carolina", "HEI", "US", "Naerofesorlbe", "20", datetime.today()),\
					("Georgia State University", "Georgia State University", "HEI", "US", "University", "72", datetime.today()),\
					("Howard University, University of Texas", "Howard University, University of Texas", "HEI", "US", "University of Texas", "59", datetime.today()),\
					("Harvard University", "Harvard University", "HEI", "US", "Boston", "50", datetime.today()),\
					("Dartmouth College", "Dartmouth College", "HEI", "US", "Dartmouth", "69", datetime.today()),\
					("DePauw University", "DePauw University", "HEI", "US", "New York", "47", datetime.today()),\
					("University of Pennsylvania", "University of Pennsylvania", "HEI", "US", "Pennsylvania", "20", datetime.today()),\
					("Wellesley College", "Wellesley College", "HEI", "US", "Wellesley", "48", datetime.today()),\
					("Arizona Board of Regents", "Arizona Board of Regents", "NGO", "US", "Zsrregentsgzon", "76", datetime.today()),\
					("Bryn Athyn", "Bryn Athyn", "NGO", "US", "Bryn", "20", datetime.today()),\
					("William Marsh Rice University", "William Marsh Rice University", "HEI", "US", "Liuniveslia", "4", datetime.today()),\
					("Hampshire College", "Hampshire College", "HEI", "US", "Hampshire", "33", datetime.today()),\
					("University of Northern Carolina at Chapel Hill", "University of Northern Carolina at Chapel Hill", "HEI", "US", "Seoul", "13", datetime.today()),\
					("Washington University, St Louis", "Washington University, St Louis", "HEI", "US", "Hisas hin", "59", datetime.today()),\
					("Baker University ", "Baker University ", "HEI", "US", "Baker", "23", datetime.today()),\
					("Baylor University", "Baylor University", "HEI", "US", "Baylor", "25", datetime.today()),\
					("New Jersey Consortium for International Studies", "New Jersey Consortium for International Studies", "NGO", "US", "Seoul", "31", datetime.today()),\
					("West Chester University", "West Chester University", "HEI", "US", "University", "13", datetime.today()),\
					("Alfred University", "Alfred University", "HEI", "US", "Alfred", "44", datetime.today()),\
					("Massachusetts College of Art and Design", "Massachusetts College of Art and Design", "HEI", "US", "Amherst", "25", datetime.today()),\
					("Franklin & Marshall College", "Franklin & Marshall College", "HEI", "US", "College", "17", datetime.today()),\
					("Gordon-Conwell Theological Seminary", "Gordon-Conwell Theological Seminary", "HEI", "US", "Dminaryoseldon", "83", datetime.today()),\
					("Mary Washington University", "Mary Washington University", "HEI", "US", "University", "88", datetime.today()),\
					("Wheaton College", "Wheaton College", "HEI", "US", "Wheaton", "14", datetime.today()),\
					("Rhode Island School of Design", "Rhode Island School of Design", "HEI", "US", "School of Design", "46", datetime.today()),\
					("School of the Museum of Fine Arts, Boston", "School of the Museum of Fine Arts, Boston", "NGO", "US", "School", "7", datetime.today()),\
					("Maryland Institute College of Art", "Maryland Institute College of Art", "HEI", "US", "College of Art", "101", datetime.today()),\
					("Babson College", "Babson College", "HEI", "US", "Babson", "71", datetime.today()),\
					("Binghampton University", "Binghampton University", "HEI", "US", "Binghampton", "41", datetime.today()),\
					("Emory University", "Emory University", "HEI", "US", "Emory", "87", datetime.today()),\
					("University of Louisville", "University of Louisville", "HEI", "US", "Louisville", "70", datetime.today()),\
					("University of Miami", "University of Miami", "HEI", "US", "Miami", "54", datetime.today()),\
					("University of Richmond", "University of Richmond", "HEI", "US", "Richmond", "20", datetime.today()),\
					("University of South Carolina", "University of South Carolina", "HEI", "US", "Vancaroiver", "50", datetime.today()),\
					("University of Chicago", "University of Chicago", "HEI", "US", "Chicago", "100", datetime.today()),\
					("California Institute of Technology", "California Institute of Technology", "HEI", "US", "Iologyaeifo", "54", datetime.today()),\
					("University of Conneticut", "University of Conneticut", "HEI", "US", "Conneticut", "8", datetime.today()),\
					("Iowa State University", "Iowa State University", "HEI", "US", "University", "46", datetime.today()),\
					("University of Mississippi", "University of Mississippi", "HEI", "US", "Mississippi", "74", datetime.today()),\
					("Michigan State University", "Michigan State University", "HEI", "US", "University", "19", datetime.today()),\
					("University of North Carolina", "University of North Carolina", "HEI", "US", "Chapel Hill", "12", datetime.today()),\
					("University of Virginia", "University of Virginia", "HEI", "US", "‎Charlottesville, VA", "19", datetime.today()),\
					("University of Washington", "University of Washington", "HEI", "US", "Seattle", "88", datetime.today()),\
					("State University of New York at Purchase", "State University of New York at Purchase", "HEI", "US", "Purchase", "28", datetime.today()),\
					("Catholic University of Uruguay", "Catholic University of Uruguay", "HEI", "UY", "Montevideo", "80", datetime.today()),\
					("Universidad ORT Uruguay", "Universidad ORT Uruguay", "HEI", "UY", "Montevideo", "28", datetime.today()),\
					("Agricultural Research Council", "Agricultural Research Council", "RES", "KR", "Seoul", "23", datetime.today()),\
					("Konkuk University", "Konkuk University", "HEI", "KR", "Konkuk", "94", datetime.today()),\
					("Konkuk University", "Konkuk University", "HEI", "KR", "Konkuk", "59", datetime.today()),\
					("Universities Allied for Essential Medicines (UAEM)", "Universities Allied for Essential Medicines (UAEM)", "HEI", "ZM", "Lusaka", "45", datetime.today()),\
					("University of Zimbabwe", "University of Zimbabwe", "HEI", "ZW", "Harare", "22", datetime.today()),\
					]

		for p in partners:
			partner = Partner.query.filter_by(name=p[0]).first()
			if partner is None:
				partner = Partner(name=p[0], offname=p[1], ptype=p[2], country=p[3], city=p[4], owner=p[5], created_date=p[6])
				db.session.add(partner)
		db.session.commit()
					
class Agreement(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	partner = db.Column(db.Integer, db.ForeignKey('partner.id'))
	atype = db.Column(db.String(64))
	level = db.Column(db.String(64))
	start_date = db.Column(db.Date, index=True)
	end_date = db.Column(db.Date, index=True)

	def __repr__(self):
		return '<Agreement no: {}>'.format(self.id)

class Visit(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	partner = db.Column(db.Integer, db.ForeignKey('partner.id'))
	vtype = db.Column(db.String(64))
	start_date = db.Column(db.Date, index=True)
	end_date = db.Column(db.Date, index=True)
	status = db.Column(db.String)
	report = db.relationship('Report', backref='visit_report', lazy='dynamic')

	def __repr__(self):
		return '<Visit report no: {}>'.format(self.id)

class Report(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String)
	visit_id = db.Column(db.Integer, db.ForeignKey('visit.id'))
	author = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Report: {}>'.format(self.content)

class Mobility(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	agreement = db.Column(db.Integer, db.ForeignKey('agreement.id'))
	mobilitytype = db.Column(db.String, db.ForeignKey('agree_type.code'))
	partner = db.Column(db.Integer, db.ForeignKey('partner.id'))
	level = db.Column(db.String)
	session = db.Column(db.Integer)
	#direction = db.Column(db.String)
	totalout = db.Column(db.Float)
	totalin = db.Column(db.Float)

	@staticmethod
	def insert_mobs():
		for i in range (0,500):
			m = Mobility(mobilitytype='STUX', partner=randint(115,523), level='Undergraduate', session=randint(2009,2018), totalout=randint(1,25)*0.5, totalin=randint(1,19)*0.5)
			db.session.add(m)
		for i in range (0,200):
			m = Mobility(mobilitytype='STUX', partner=randint(115,523), level='Postgraduate Taught', session=randint(2009,2018), totalout=randint(1,8)*0.5, totalin=randint(1,8)*0.5)
			db.session.add(m)
		for i in range (0,350):
			m = Mobility(mobilitytype='RESE', partner=randint(115,523), level='Academic staff', session=randint(2009,2018), totalout=randint(1,6)*0.5, totalin=randint(1,9)*0.5)
			db.session.add(m)
		db.session.commit()

class Country(db.Model):
	iso = db.Column(db.String, primary_key=True)
	name = db.Column(db.String)

	@staticmethod
	def insert_countries():
		countryvals = [('AF', 'Afghanistan'), ('AX', 'Aland Islands'), ('AL', 'Albania'), ('DZ', 'Algeria'), \
		('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'), \
		('AG', 'Antigua and Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'), \
		('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), \
		('BY', 'Belarus'), ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BT', 'Bhutan'), \
		('BO', 'Bolivia'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BV', 'Bouvet Island'), ('BR', 'Brazil'), \
		('VG', 'British Virgin Islands'), ('IO', 'British Indian Ocean Territory'), ('BN', 'Brunei Darussalam'), \
		('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), \
		('CA', 'Canada'), ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), \
		('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('HK', 'Hong Kong, SAR China'), ('MO', 'Macao, SAR China'), \
		('CX', 'Christmas Island'), ('CC', 'Cocos (Keeling) Islands'), ('CO', 'Colombia'), ('KM', 'Comoros'), \
		('CG', 'Congo (Brazzaville)'), ('CD', 'Congo, (Kinshasa)'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), \
		('CI', 'Côte dIvoire'), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), \
		('DK', 'Denmark'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), \
		('EG', 'Egypt'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'), \
		('ET', 'Ethiopia'), ('FK', 'Falkland Islands (Malvinas)'), ('FO', 'Faroe Islands'), ('FJ', 'Fiji'), ('FI', 'Finland'), \
		('FR', 'France'), ('GF', 'French Guyana'), ('PF', 'French Polynesia'), ('TF', 'French Southern Territories'), ('GA', 'Gabon'), \
		('GM', 'Gambia'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GR', 'Greece'), ('GL', 'Greenland'), \
		('GD', 'Grenada'), ('GP', 'Guadeloupe'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GG', 'Guernsey'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), \
		('GY', 'Guyana'), ('HT', 'Haiti'), ('HM', 'Heard and Mcdonald Islands'), ('VA', 'Holy See (Vatican City State)'), ('HN', 'Honduras'), \
		('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran, Islamic Republic of'), ('IQ', 'Iraq'), \
		('IE', 'Ireland'), ('IM', 'Isle of Man'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'), ('JP', 'Japan'), ('JE', 'Jersey'), \
		('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KI', 'Kiribati'), ('KP', 'Korea (North)'), ('KR', 'Korea (South)'), \
		('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', 'Lao PDR'), ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'), \
		('LY', 'Libya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MK', 'Macedonia, Republic of'), \
		('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MH', 'Marshall Islands'), \
		('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('YT', 'Mayotte'), ('MX', 'Mexico'), ('FM', 'Micronesia, Federated States of'), \
		('MD', 'Moldova'), ('MC', 'Monaco'), ('MN', 'Mongolia'), ('ME', 'Montenegro'), ('MS', 'Montserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), \
		('MM', 'Myanmar'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('AN', 'Netherlands Antilles'), \
		('NC', 'New Caledonia'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'), \
		('NF', 'Norfolk Island'), ('MP', 'Northern Mariana Islands'), ('NO', 'Norway'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PW', 'Palau'), \
		('PS', 'Palestinian Territory'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), \
		('PN', 'Pitcairn'), ('PL', 'Poland'), ('PT', 'Portugal'), ('PR', 'Puerto Rico'), ('QA', 'Qatar'), ('RE', 'Réunion'), ('RO', 'Romania'), \
		('RU', 'Russian Federation'), ('RW', 'Rwanda'), ('BL', 'Saint-Barthélemy'), ('SH', 'Saint Helena'), ('KN', 'Saint Kitts and Nevis'), \
		('LC', 'Saint Lucia'), ('MF', 'Saint-Martin (French part)'), ('PM', 'Saint Pierre and Miquelon'), ('VC', 'Saint Vincent and Grenadines'), \
		('WS', 'Samoa'), ('SM', 'San Marino'), ('ST', 'Sao Tome and Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'), ('RS', 'Serbia'), \
		('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), \
		('SO', 'Somalia'), ('ZA', 'South Africa'), ('GS', 'South Georgia and the South Sandwich Islands'), ('SS', 'South Sudan'), \
		('ES', 'Spain'), ('LK', 'Sri Lanka'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SJ', 'Svalbard and Jan Mayen Islands'), \
		('SZ', 'Swaziland'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SY', 'Syrian Arab Republic (Syria)'), ('TW', 'Taiwan, Republic of China'), \
		('TJ', 'Tajikistan'), ('TZ', 'Tanzania, United Republic of'), ('TH', 'Thailand'), ('TL', 'Timor-Leste'), ('TG', 'Togo'), \
		('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), \
		('TC', 'Turks and Caicos Islands'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'), \
		('GB', 'United Kingdom'), ('US', 'United States of America'), ('UM', 'US Minor Outlying Islands'), ('UY', 'Uruguay'), \
		('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VE', 'Venezuela (Bolivarian Republic)'), ('VN', 'Viet Nam'), \
		('VI', 'Virgin Islands, US'), ('WF', 'Wallis and Futuna Islands'), ('EH', 'Western Sahara'), ('YE', 'Yemen'), \
		('ZM', 'Zambia'), ('ZW', 'Zimbabwe')]

		for c in countryvals:
			country = Country.query.filter_by(iso=c[0]).first()
			if country is None:
				country = Country(iso=c[0])
			country.name = c[1]
			db.session.add(country)
		db.session.commit()

class OrgType(db.Model):
	code = db.Column(db.String, primary_key=True)
	name = db.Column(db.String)

	@staticmethod
	def add_types():
		types = [('HEI', 'University'), ('NGO', 'Non-government organisation'), ('RES', 'Research centre'), ('GOV', 'Government organisation')]
		for t in types:
			orgtype = OrgType.query.filter_by(code=t[0]).first()
			if orgtype is None:
				orgtype = OrgType(code=t[0])
			orgtype.name = t[1]
			db.session.add(orgtype)
		db.session.commit()

class AgreeType(db.Model):
	code = db.Column(db.String, primary_key=True)
	name = db.Column(db.String)
	mobility = db.relationship('Mobility', backref='mobility_type', lazy='dynamic')

	@staticmethod
	def add_types():
		types = [('STUX', 'Student exchange'), ('STAX', 'Staff exchange'), \
		('RESE', 'Research collaboration'), ('GOVE', 'Government organisation'), \
		('ERAS', 'Erasmus student exchange'), ('ERST', 'Erasmus staff exchange')]

		for t in types:
			agreetype = AgreeType.query.filter_by(code=t[0]).first()
			if agreetype is None:
				agreetype = AgreeType(code=t[0])
			agreetype.name = t[1]
			db.session.add(agreetype)
		db.session.commit()

class AcademicYear(db.Model):
	year = db.Column(db.Integer, primary_key=True)
	#desc = db.Column(db.Integer)
	descr = db.Column(db.String)

	def add_years():
		start_year = 2000
		end_year = (datetime.today().year)+1

		while start_year != end_year:
			year = AcademicYear.query.filter_by(year=start_year)
			if year == None:
				ayr = AcademicYear(year=start_year, descr=str(str(start_year)+'/'+str(start_year+1)))
				db.session.add(ayr)
			start_year = start_year+1

		db.session.commit()