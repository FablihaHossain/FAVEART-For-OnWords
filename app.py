from application import app, db
from flask import render_template, request, url_for
from models import Users, Paths, Checkpoints, Interactions
from database import Database
from datetime import *
# Defining basic route
@app.route("/")
def index():
	# Getting all users in the database
	user_list = Users.query.all()

	# Getting all the paths in the database
	paths_list = Paths.query.all()

	#Getting all the checkpoints in the database
	checkpoint_list = Checkpoints.query.all()

	#Getting all the interactions in the database
	interaction_list = Interactions.query.all()

	# Add new user to test password hashing
	Database.insert_user("John", "Smith", "jsmith@gmail.com", "jsmith", "mystery", "guest")

	# Testing how to match hashed passwords
	# hash_pw1 = Database.hash_password("password")

	# hash_pw2 = Database.hash_password("password")
	# decoded_hash = hash_pw1.decode('UTF-8')
	# decoded_hash2 = hash_pw2.decode('UTF-8')
	# print(decoded_hash)
	# print(decoded_hash2)

	# # Getting the current password hash
	pw3 = Database.select_where("users", "user_id", 7, "password")
	# print(pw1)

	# if decoded_hash == decoded_hash2:
	# 	valid = True
	# else:
	# 	valid = False

	valid = Database.validate_login("jsmith", "mysTery")
	print(valid)



	# pw1_check = Database.check_hashed_passwords(hash_pw1, 'password')

	return render_template("layout.html", users = user_list, paths = paths_list, checkpoints = checkpoint_list, interactions = interaction_list)