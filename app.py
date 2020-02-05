from application import app, db
from flask import render_template, request, url_for
from models import Users, Paths, Checkpoints, Interactions
from database import Database
from datetime import *
# Defining basic route
@app.route("/")
def index():
	# Adding a new user to the database
	Database.insert_user("Shoshanah", "Tarkow", "tarkow@gmail.com", "starkow", "onwords", "admin")

	# Adding a new path to the database
	cList = [10, 20, 30]
	iList = [20, 30, 40]
	Database.insert_path("Blah", "Blah blah", cList, iList, "Vickie")

	# # Adding a new checkpoint to the database
	# text = ['Will', 'This', 'Work?']
	# animations = ['Animation1', 'Animation2', 'Animation3']
	# geolocation = [43.3232, -54.2323]
	# Database.insert_checkpoint(text, animations, "pink", geolocation)

	# # Adding a new interaction to the database
	# ids = [3, 5, 2]
	# today = datetime.today()
	# Database.insert_interaction(1, 1, ids, today)

	# Getting all users in the database
	user_list = Users.query.all()

	# Getting all the paths in the database
	paths_list = Paths.query.all()

	#Getting all the checkpoints in the database
	checkpoint_list = Checkpoints.query.all()

	#Getting all the interactions in the database
	interaction_list = Interactions.query.all()

	# check_exists = Database.check_duplicate("Users", "firstname", "Leune")
	# print(check_exists)

	# Testing the select_where function
	user1 = Database.select_where("users", "user_id", 100)
	print(user1)

	path1 = Database.select_where("paths", "path_id", 1)
	print(path1)

	# Testing the update function
	Database.update_table("paths", "path_id", 4, "description", "this is testing update")

	return render_template("layout.html", users = user_list, paths = paths_list, checkpoints = checkpoint_list, interactions = interaction_list)