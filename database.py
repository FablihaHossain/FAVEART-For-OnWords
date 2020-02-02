import sqlalchemy
import psycopg2
from application import db
from models import Users, Paths, Checkpoints, Interactions
from config import Config
from sqlalchemy import text

class Database():
	# Checking for duplicate values
	def check_duplicate(tablename, columnName, value):
		# Developing the query to get from the table 
		query = text("SELECT * FROM {} WHERE {} = '{}'".format(tablename, columnName, value))

		# Finding out if it exists in the table
		exists = db.engine.execute(query).fetchone() is not None

		# Returning if the entry exists or not
		return exists
	# Get Next ID
	def next_id(tablename):
		last_id = None
		if tablename is "Users":
			lastUser = Users.query.order_by(Users.user_id.desc()).first()
			last_id = lastUser.user_id
		elif tablename is "Paths":
			lastPath = Paths.query.order_by(Paths.path_id.desc()).first()
			last_id = lastPath.path_id
		elif tablename is "Checkpoints":
			lastCheckpoint = Checkpoints.query.order_by(Checkpoints.checkpoint_id.desc()).first()
			last_id = lastCheckpoint.checkpoint_id
		elif tablename is "Interactions":
			lastInteraction= Interactions.query.order_by(Interactions.interaction_id.desc()).first()
			last_id = lastInteraction.interaction_id
		else:
			return "Error! Wrong Table Name Given"

		newId = last_id + 1
		return newID

	# Insert User Into Database 

	# Insert Path into Database

	# Insert Checkpoint into Database

	# Insert Interaction into Database 
	
	# Delete From Table in Database 

	# Select From Table in Database

	# Update Table in Database

	# Validate Login
