from application import app, db
from flask import render_template, request, url_for
from models import Users, Paths, Checkpoints, Interactions
from database import Database
from datetime import *
# Defining basic route
@app.route("/")
def index():
	# Testing the delete function
	Database.delete_from("users", "user_id", 8, "firstname", "Shoshanah")
	# Adding a new user to the database
	# Database.insert_user("Test", "test@gmail.com", "test", "testing", "guest")

	# Adding a new path to the database
	# cList = [10, 20, 30]
	# iList = [20, 30, 40]
	# codes = [8, 2, -7]
	# Database.insert_path("Roses", 1, cList, iList, "Patrick Star", "public", codes)

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

	# Check duplicate function (with psycopg2)
	# check_exists = Database.check_duplicate("paths", "path_id", "1")
	# print("Check Duplicate:")
	# print(check_exists)

	# Testing the next Id function
	# i = Database.next_id("Interactions")
	# print("Next ID")
	# print(i)

	# Testing the select_where function
	# user1 = Database.select_where("users", "user_id", 2, "email")
	# print(user1)

	# path1 = Database.select_where("paths", "path_id", 1, "description")
	# print(path1)

	# Testing the update function
	# Database.update_table("dfsfsdf", "udsfsdfs", "wfref", "firstname", "Jacob")
	# Database.update_table("dsfsfds", "akdfsadkjf", 9, "lastname", "Smith")
	# Database.update_table("dfsdfsf", "dsfsfds", 9, "username", "jsmith")

	# Testing the validate login function
	result = Database.validate_login("vgrinthal", "chocolate")
	print("Password check")
	print(result)

	return render_template("layout.html", users = user_list, paths = paths_list, checkpoints = checkpoint_list, interactions = interaction_list)