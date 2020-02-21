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

			# Getting all the rows from the table given
			rows = cursor.fetchall()

			# Getting the id of the last row
			last_id = rows[count-1][0]

			# Incremeting the id
			newId = last_id + 1
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

				# Creating the new user
				newUser = Users(user_id = nextId, firstname = firstname, lastname = lastname, email = email, username = username, password = password, role = role)

				# Adding the new user to the database
				db.session.add(newUser)

				# Commiting the change
				db.session.commit()

	# Insert Path into Database
	# Pathmaker cannot have two paths with the same name AND description
	def insert_path(pathname, path_description, checkpoint_ids, interaction_ids, pathmaker, status, codes=[0]):
		try:
			# Checking if the path already exists in the system (for the specified pathmaker)
			query = "SELECT * FROM paths WHERE name = '%s' AND description = '%s' AND pathmaker = '%s'" % (pathname, path_description, pathmaker)

			# Executing the query
			cursor.execute(query)

			# Finding out if it exists in the table
			exists = cursor.fetchone() is not None
		
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
		except Exception as error:
				print ("Error! %s" % error)

	# Insert Checkpoint into Database
	def insert_checkpoint(text_list, animation_list, color, geolocation):
		# Getting the next ID
		nextId = Database.next_id("Checkpoints")

		# Creating a new checkpoint
		newCheckpoint = Checkpoints(checkpoint_id = nextId, text = text_list, animations = animation_list, color = color, geolocation = geolocation)
		
		# Adding the new checkpoint to the database
		db.session.add(newCheckpoint)

		# Commiting the change to the database
		db.session.commit()
	
	# Insert Interaction into Database 
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

				# Getting the password from the database
				user_password = Database.select_where("users", "user_id", current_id, "password")

				# Comparing the two passwords to see if they are a match
				if user_password == password:
					validated = True

			# Returning the result
			return validated
		except Exception as error:
			print("Error! %s" % error)

	# Function to hash password (using bcrypt)
	def hash_password(password):
		# Generating the hashed password
		hashed_password = bcrypt.generate_password_hash(password)

		# Returning the hashed password
		return hashed_password

	# Checking password hashes to see if they are the same
	def check_hashed_passwords(password_hash, password):
		# Initial boolean, set to false
		same_password = False

		# Using the bcrypt function to check if passwords are similar
		same_password = bcrypt.check_password_hash(password_hash, password)

		# Returning it
		return same_password


	# Credit to https://stackoverflow.com/questions/8551952/how-to-get-last-record
	# Credit to https://docs.sqlalchemy.org/en/13/core/connections.html
	# Credit to https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/

	# Credit to https://github.com/nycdb/nycdb/blob/master/src/nycdb/database.py
	# Credit to http://zetcode.com/python/psycopg2/
	# Credit to https://wiki.postgresql.org/wiki/Psycopg2_Tutorial