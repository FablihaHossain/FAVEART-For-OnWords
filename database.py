import sqlalchemy
import psycopg2
from sqlalchemy.inspection import inspect
from application import db
from models import Users, Paths, Checkpoints, Interactions
from config import Config
from sqlalchemy import text

class Database():
	# Checking if the primary correct primary key was given for a table
	# def pkey_check(tablename, pkcolumn):
	# 	pkey = inspect(tablename).primary_key[0].name


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
		# The last id will be found, depending on the table
		last_id = None

		# Since the ID numbers are generated through increments, the very last object in the table is found
		# From there, the last_id variable will be determined
		if tablename == "Users":
			lastUser = Users.query.order_by(Users.user_id.desc()).first()
			last_id = lastUser.user_id
		elif tablename == "Paths":
			lastPath = Paths.query.order_by(Paths.path_id.desc()).first()
			last_id = lastPath.path_id
		elif tablename == "Checkpoints":
			lastCheckpoint = Checkpoints.query.order_by(Checkpoints.checkpoint_id.desc()).first()
			last_id = lastCheckpoint.checkpoint_id
		elif tablename == "Interactions":
			lastInteraction= Interactions.query.order_by(Interactions.interaction_id.desc()).first()
			last_id = lastInteraction.interaction_id
		else:
			return "Error! Wrong Table Name Given"

		# Incrementing the ID
		newId = last_id + 1

		# Returning the new ID
		return newId

	# Insert User Into Database 
	# Note: No two users can have the same username and/or the same email
	def insert_user(firstname, lastname, email, username, password, role):
		# Checking if the user already exists in the database 
		username_exists = Database.check_duplicate("Users", "username", username)
		email_exists = Database.check_duplicate("Users", "email", email)

		# If the username and email doesn't already exist, the new user is added to the database
		if not username_exists and not email_exists:
			# Getting the next ID
			nextId = Database.next_id("Users")
			# Creating the new user
			newUser = Users(user_id = nextId, firstname = firstname, lastname = lastname, email = email, username = username, password = password, role = role)

			# Adding the new user to the database
			db.session.add(newUser)

			# Commiting the change
			db.session.commit()

	# Insert Path into Database
	# Pathmaker cannot have two paths with the same name AND description
	def insert_path(pathname, path_description, checkpoint_ids, interaction_ids, pathmaker, status, codes):
		# Checking if the path already exists in the system (for the specified pathmaker)
		query = text("SELECT * FROM paths WHERE name = '{}' AND description = '{}' AND pathmaker = '{}'".format(pathname, path_description, pathmaker))
		exists = db.engine.execute(query).fetchone() is not None

		# If the path doesn't exist, it is then added to the database
		if not exists:
			# Getting the next path ID
			nextID = Database.next_id("Paths")

			# Creating a new path
			newPath = Paths(path_id = nextID, name = pathname, description = path_description, checkpoints = checkpoint_ids, interactions = interaction_ids, pathmaker = pathmaker, status = status, access_codes = codes)

			# Adding the new path to the database
			db.session.add(newPath)

			# Commiting the change to the database
			db.session.commit()
	# # Insert Checkpoint into Database
	def insert_checkpoint(text_list, animation_list, color, geolocation):
		# Getting the next ID
		nextId = Database.next_id("Checkpoints")

		# Creating a new checkpoint
		newCheckpoint = Checkpoints(checkpoint_id = nextId, text = text_list, animations = animation_list, color = color, geolocation = geolocation)
		
		# Adding the new checkpoint to the database
		db.session.add(newCheckpoint)

		# Commiting the change to the database
		db.session.commit()
	# # Insert Interaction into Database 
	def insert_interaction(path_id, checkpoint_id, user_ids, currentDatetime):
		# Getting the next ID
		nextId = Database.next_id("Interactions")

		# Creating a new interaction
		newInteraction = Interactions(interaction_id = nextId, path_id = path_id, checkpoint_id = checkpoint_id, user_id = user_ids, datetime = currentDatetime)

		# Creating a new checkpoint
		db.session.add(newInteraction)

		# Committing the change to the database
		db.session.commit()

	# Select From Table in Database
	def select_where(tablename, pkcolumn, pk, columnName):
		# Developing the query
		query = text("SELECT {} FROM {} WHERE {} = '{}'".format(columnName, tablename, pkcolumn, pk))

		# Executing the query
		result = db.session.execute(query).fetchone()

		# Reformating the result statement
		result = str(result).strip("(',')")

		# Returning result
		if result != "None":
			return result 
		else:
			return "Sorry, cannot find value from table {}".format(tablename)

	# Update Table in Database
	def update_table(tablename, pkcolumn, pk, columnName, newValue):
		# Developing the query
		query = text("UPDATE {} SET {} = '{}' WHERE {} = {}".format(tablename, columnName, newValue, pkcolumn, pk))

		# Executing the query
		db.engine.execute(query)

	# Delete From Table in Database 
	# Really needs some work, especially with different types of input
	def delete_from(tablename, pkcolumn, pk, columnName, columnValue):
		# Developing the query
		query = text("DELETE FROM {} WHERE {} = '{}'".format(tablename, columnName, columnValue))

		# Executing the query
		db.engine.execute(query)

	# Validate Login
	def validate_login(username, password):
		# Initially the validation will be false
		validated = False

		# Checks if the username given exists in the database
		exists = db.session.query(Users.username).filter_by(username = username).scalar() is not None

		# If it exists, it checks if the password given is correct
		if exists:
			# Getting the password from the database
			user_password = Database.select_where("users", "username", username, "password")

			# Comparing the two passwords to see if they are a match
			if user_password == password:
				validated = True

		# Returning the result
		return validated
	# Credit to https://stackoverflow.com/questions/8551952/how-to-get-last-record
	# Credit to https://docs.sqlalchemy.org/en/13/core/connections.html
	# Credit to https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/