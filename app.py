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

	# Hashing all the passwords in the database
	# for user in user_list:
	# 	# getting the current password
	# 	password = Database.select_where("users", "user_id", user.user_id, "password")
	# 	print(password)
		
	# 	# Hashing the password
	# 	hashed_pw = Database.hash_password(password)
	# 	print(hashed_pw)

	# 	# Updating the database
	# 	Database.update_table("users", "user_id", user.user_id, "password", hashed_pw.decode('UTF-8'))

	return render_template("layout.html", users = user_list, paths = paths_list, checkpoints = checkpoint_list, interactions = interaction_list)