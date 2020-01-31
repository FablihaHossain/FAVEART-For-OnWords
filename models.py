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
	# Roles can either be pathmaker, explorer, administrator
	role = db.Column(db.String(30))

# Path Table
class Paths(db.Model):
	__table_args__ = {'extend_existing': True}
	path_id = db.Column(db.Integer, primary_key = True, unique = True)
	name = db.Column(db.String(100), nullable = True)
	description = db.Column(db.String(1000000), nullable = False)
	# Array of checkpoint id values within Path 
	checkpoints = db.Column(db.ARRAY(db.Integer))
	# Array of interaction id values within Path
	interactions = db.Column(db.ARRAY(db.Integer))
	pathmaker = db.Column(db.String(100), nullable = False)

# Checkpoint Table 
class Checkpoints(db.Model):
	__table_args__ = {'extend_existing': True}
	checkpoint_id = db.Column(db.Integer, primary_key = True, unique = True)
	# Array of strings of text at that particular checkpoint
	# Note: Must be maximun of 3
	text = db.Column(db.ARRAY(db.String(100)), nullable = False)
	# Array of animations to correspond with the text
	animations = db.Column(db.ARRAY(db.String(200)), nullable = False)
	color = db.Column(db.String(100))
	# Latitude and Longitude
	geolocation = db.Column(db.ARRAY(db.Float))

class Interactions(db.Model):
	__table_args__ = {'extend_existing': True}
	interaction_id = db.Column(db.Integer, primary_key = True, unique = True)
	path_id = db.Column(db.Integer, db.ForeignKey('path.path_id'), nullable = False)
	checkpoint_id = db.Column(db.Integer, db.ForeignKey('checkpoint.checkpoint_id'), nullable = False)
	# Array of user ids of those explorers that made the interaction
	user_id = db.Column(db.ARRAY(db.Integer))
	datetime = db.Column(db.DateTime)

# Credit to https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
# Credit to https://docs.sqlalchemy.org/en/13/orm/join_conditions.html#relationship-primaryjoin 
