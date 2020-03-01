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

	return render_template("layout.html", users = user_list, paths = paths_list, checkpoints = checkpoint_list, interactions = interaction_list)
