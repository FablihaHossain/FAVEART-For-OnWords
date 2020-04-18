import sqlalchemy
import psycopg2
from application import db, conn, bcrypt
from models import Users, Paths, Checkpoints, Interactions
from config import Config

# Getting a cursor object from database connection
cursor = conn.cursor()

class Database():
	# Checking for duplicate values
	def check_duplicate(tablename, columnName, value):
		# Developing the query to get from the table 
		query = "SELECT * FROM %s WHERE %s = '%s'" % (tablename, columnName, value)

		try:
			# Executing the query
			cursor.execute(query)

			# Finding out if it exists in the table
			exists = cursor.fetchone() is not None

			# Returning if the entry exists or not
			return exists
		except Exception as error:
			return "Error! %s" % error

	# Function to get id of a user
	def get_userId(username):
		try:
			# Developing the query
			query = "SELECT * FROM users WHERE username = '%s'" % (username)

			# Executing the query
			cursor.execute(query)

			# Getting the user info from cursor, then user_id
			user = cursor.fetchall()
			user_id = user[0][0]

			# Returning the user_id
			return user_id
		except Exception as error:
			print ("Error! %s" % error)

	# Function to get checkpoint id
	def getCheckpointID(text, animation, color, font):
		try:
			# Developing the query
			query = "SELECT * FROM checkpoints WHERE text = '%s' AND animation = '%s' AND color = '%s' AND font = '%s'" % (text, animation, color, font)

			# Executing the query
			cursor.execute(query)

			# Getting the user info from cursor, then user_id
			checkpoint = cursor.fetchall()
			checkpoint_id = checkpoint[0][0]

			# Returning the user_id
			return checkpoint_id
		except Exception as error:
			print ("Error! %s" % error)

	# Function to count the number of rows at a given table
	def row_count(tablename):
		try:
			# Developing the query
			query = "SELECT * FROM %s" % (tablename)

			# Executing the query
			cursor.execute(query)

			# Getting the row count
			count = cursor.rowcount

			# Returning the number of rows
			return count
		except:
			print("Error! Wrong table name given")

	# Get Next ID
	def next_id(tablename):
		try:
			# The last id will be found, depending on the table
			last_id = None

			# Developing a query to get all rows in the given table
			query = "SELECT * FROM %s" % (tablename)

			# Executing the query
			cursor.execute(query)

			# Getting the number of rows
			count = cursor.rowcount

			# Incrementing the id
			newId = count + 1
			return newId
		except:
			print("Error! Incorrect table name given")

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

				# Ensuring that the ID doesn't duplicate
				while(Database.check_duplicate("users", "user_id", nextId)):
					nextId = nextId + 1

				# Hashing the password
				hashed_password = Database.hash_password(password)
				hash_decoded = hashed_password.decode('UTF-8')

				# Creating the new user
				newUser = Users(user_id = nextId, firstname = firstname, lastname = lastname, email = email, username = username, password = hash_decoded, role = role)

				# Adding the new user to the database
				db.session.add(newUser)

				# Commiting the change
				db.session.commit()

	# Insert Path into Database
	# Pathmaker cannot have two paths with the same name AND description
	def insert_path(pathname, path_description, checkpoint_ids, interaction_ids, pathmaker, status, base_format):
		try:
			# Formating the string values for raw psycopg2
			name = Database.format_entry(pathname)
			description = Database.format_entry(path_description)

			# Checking if the path already exists in the system (for the specified pathmaker)
			query = "SELECT * FROM paths WHERE name = '%s' AND description = '%s' AND pathmaker = '%s'" % (name, description, pathmaker)

			# Executing the query
			cursor.execute(query)

			# Finding out if it exists in the table
			exists = cursor.fetchone() is not None
		
			# If the path doesn't exist, it is then added to the database
			if not exists:
				# Getting the next path ID
				nextId = Database.next_id("Paths")

				# Ensuring that the ID doesn't duplicate
				while(Database.check_duplicate("paths", "path_id", nextId)):
					nextId = nextId + 1

				# Creating a new path
				newPath = Paths(path_id = nextId, name = pathname, description = path_description, checkpoints = checkpoint_ids, interactions = interaction_ids, pathmaker = pathmaker, status = status, base_format = base_format)

				# Adding the new path to the database
				db.session.add(newPath)

				# Commiting the change to the database
				db.session.commit()
		except Exception as error:
				print ("Error! %s" % error)

	# Insert Checkpoint into Database
	def insert_checkpoint(text, animation, color, geolocation, font, markerName, path_id):
		# Getting the next ID
		nextId = Database.next_id("Checkpoints")

		# Ensuring that the ID doesn't duplicate
		while(Database.check_duplicate("checkpoints", "checkpoint_id", nextId)):
			nextId = nextId + 1

		# Creating a new checkpoint
		newCheckpoint = Checkpoints(checkpoint_id = nextId, text = text, animation = animation, color = color, geolocation = geolocation, font = font, marker = markerName, path_id = path_id)
		
		# Adding the new checkpoint to the database
		db.session.add(newCheckpoint)

		# Commiting the change to the database
		db.session.commit()
	
	# Insert Interaction into Database 
	def insert_interaction(path_id, checkpoint_id, user_ids, currentDatetime):
		# Getting the next ID
		nextId = Database.next_id("Interactions")

		# Ensuring that the ID doesn't duplicate
		while(Database.check_duplicate("interactions", "interaction_id", nextId)):
			nextId = nextId + 1

		# Creating a new interaction
		newInteraction = Interactions(interaction_id = nextId, path_id = path_id, checkpoint_id = checkpoint_id, user_id = user_ids, datetime = currentDatetime)

		# Creating a new checkpoint
		db.session.add(newInteraction)

		# Committing the change to the database
		db.session.commit()

	# Select From Table in Database
	def select_where(tablename, pkcolumn, pk, columnName='*'):
		try:
			# Developing the query
			query = "SELECT %s FROM %s WHERE %s = %d" % (columnName, tablename, pkcolumn, pk)

			# Executing the query
			cursor.execute(query)

			# Getting the result
			result = cursor.fetchone()

			# Returning the result if not none
			if result is not None:
				return result[0]
			else:
				return "Sorry, cannot find value from table {}".format(tablename)
		except Exception as error:
				print ("Error! %s" % error)
				
	# Update Table in Database
	def update_table(tablename, pkcolumn, pk, columnName, newValue):
		try:
			# Developing the query
			query = "UPDATE %s SET %s = '%s' WHERE %s = %d" % (tablename, columnName, newValue, pkcolumn, pk)

			# Executing the query
			cursor.execute(query)

			# Commiting the change
			conn.commit()
		except Exception as error:
			print("Error! %s" % error)

	# Delete From Table in Database 
	# Really needs some work, especially with different types of input
	def delete_from(tablename, pkcolumn, pk, columnName, columnValue):
		try:
			# Developing the query
			query = "DELETE FROM %s WHERE %s = '%s' AND %s = %d" % (tablename, columnName, columnValue, pkcolumn, pk)

			# Executing the query
			cursor.execute(query)

			# Commiting the change
			conn.commit()
		except Exception as error:
			print("Error! %s" % error)

	# Validate Login
	def validate_login(username, password):
		# Initially the validation will be false
		validated = False

		# Checks if the username given exists in the database
		exists = db.session.query(Users.username).filter_by(username = username).scalar() is not None

		# If it exists, it checks if the password given is correct
		try:
			if exists:
				# Getting the user id of the user
				query = "SELECT user_id FROM users WHERE username = '%s'" % username
				cursor.execute(query)
				current_id = cursor.fetchone()[0]

				# Getting the hashed password from the database
				hash_password = Database.select_where("users", "user_id", current_id, "password")

				# Comparing the two passwords to see if they are a match
				validated = Database.check_hashed_passwords(hash_password, password)

			# Returning the result
			return validated
		except Exception as error:
			print("Error! %s" % error)

	# Function to hash password (using bcrypt)
	def hash_password(password):
		try:
			# Generating the hashed password
			hashed_password = bcrypt.generate_password_hash(password)

			# Returning the hashed password
			return hashed_password
		except Exception as error:
			print("Error! %s" % error)

	# Checking password hashes to see if they are the same
	def check_hashed_passwords(password_hash, password):
		try:
			# Initial boolean, set to false
			same_password = False

			# Using the bcrypt function to check if passwords are similar
			same_password = bcrypt.check_password_hash(password_hash, password)

			# Returning it
			return same_password
		except Exception as error:
			print("Error! %s" % error)

	# A String formating function for text entries with '
	# Helper function for insert_user and insert_path 
	def format_entry(text):
		# Declaring a variable to keep count
		position = 0
		# Parsing the text
		while position < len(text):
			# Finding the position of the apostrophe
			if text[position] == "'":
				# Formating the string
				text = text[0:position] + "'" + text[position:]

				# incrementing position to avoid triple apostrophes
				position = position + 1
			# Incrementing position
			position = position + 1
		# Returning the formatted text
		return text

	# A function to check for duplicates in a given list
	# A helper function to ensure that a pathmaker cannot chose the same markers for two checkpoints
	def duplicate_markers(marker_list):
		if len(marker_list) == len(set(marker_list)):
			return False
		else:
			return True
				
	# Credit to https://stackoverflow.com/questions/8551952/how-to-get-last-record
	# Credit to https://docs.sqlalchemy.org/en/13/core/connections.html
	# Credit to https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/

	# Credit to https://github.com/nycdb/nycdb/blob/master/src/nycdb/database.py
	# Credit to http://zetcode.com/python/psycopg2/
	# Credit to https://wiki.postgresql.org/wiki/Psycopg2_Tutorial
	# Credit to https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
	# Credit to https://thispointer.com/python-3-ways-to-check-if-there-are-duplicates-in-a-list/