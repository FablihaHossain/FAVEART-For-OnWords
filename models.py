from application import db

# User Table
class Users(db.Model):
	__table_args__ = {'extend_existing': True}
	user_id = db.Column(db.Integer, primary_key = True, unique = True)
	firstname = db.Column(db.String(50), nullable = False)
	lastname = db.Column(db.String(50), nullable = False)
	email = db.Column(db.String(200), unique = True, nullable = False)
	username = db.Column(db.String(100), unique = True, nullable = False)
	password = db.Column(db.String(100), nullable = False)
	role = db.Column(db.String(30)) # Roles can either be pathmaker, explorer, administrator

# Path Table
class Paths(db.Model):
	__table_args__ = {'extend_existing': True}
	path_id = db.Column(db.Integer, primary_key = True, unique = True)
	name = db.Column(db.String(100), nullable = True)
	description = db.Column(db.String(1000000), nullable = False)
	checkpoints = db.Column(db.ARRAY(db.Integer)) # Array of checkpoint id values within Path 
	interactions = db.Column(db.ARRAY(db.Integer)) # Array of interaction id values within Path
	pathmaker = db.Column(db.String(100), nullable = False)
	status = db.Column(db.String(50), nullable = False)
	base_format = db.Column(db.String(20), nullable = False)
	

# Checkpoint Table 
class Checkpoints(db.Model):
	__table_args__ = {'extend_existing': True}
	checkpoint_id = db.Column(db.Integer, primary_key = True, unique = True)
	text = db.Column(db.String(750), nullable = False)
	animation = db.Column(db.String(100), nullable = False)
	color = db.Column(db.String(100))
	geolocation = db.Column(db.ARRAY(db.Float))  # Latitude and Longitude
	font = db.Column(db.String(200))
	marker = db.Column(db.String(200))	# Name of associated Marker 
	path_id = db.Column(db.Integer, db.ForeignKey('paths.path_id'), nullable = False)

# Interactions Table
class Interactions(db.Model):
	__table_args__ = {'extend_existing': True}
	interaction_id = db.Column(db.Integer, primary_key = True, unique = True)
	path_id = db.Column(db.Integer, db.ForeignKey('paths.path_id'), nullable = False)
	checkpoint_id = db.Column(db.Integer, db.ForeignKey('checkpoints.checkpoint_id'), nullable = False)
	user_id = db.Column(db.Integer)
	datetime = db.Column(db.DateTime)

# Credit to https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
# Credit to https://docs.sqlalchemy.org/en/13/orm/join_conditions.html#relationship-primaryjoin 
