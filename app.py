from application import app, db
from flask import render_template, request, url_for, session, flash, redirect
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

# Login Page
@app.route("/login", methods = ['GET', 'POST'])
def login():
	# Getting the username and password entered
	if request.method == "POST":
		# If either field is empty, gives an error message
		if request.form['username'] is "" or request.form['password'] is "":
			flash("Error! Neither field can be empty!")
		else:
			username = request.form['username']
			password = request.form['password']

			# Validating login
			valid = Database.validate_login(username, password)

			#If valid, creates a flash session with username and user_id
			if valid:
				# Getting the user_id of the current user
				user_id = Database.get_userId(username)

				# Creating a session with the user
				session['username'] = username
				session['user_id'] = user_id 

				# Taking the user to the homepage
				return redirect(url_for('homepage'))

			else:
				flash("Invalid Login! Please Try Again")
	return render_template("login.html")

# Register Page
@app.route("/register", methods = ['GET', 'POST'])
def register():
	# Getting the information from all the fields
	if request.method == "POST":
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		email = request.form['email']
		username = request.form['username']
		password = request.form['password']
		role = request.form['roles']

		print("role is %s" % role)
		# None of the fields can be empty 
	return render_template("register.html")

# Home Page
@app.route("/homepage")
def homepage():
	return render_template("homepage.html")

# Logging Out redirects to login page
@app.route("/logout")
def logout():
	session.pop('username', None)
	session.pop('user_id', None)
	flash("You have logged out sucessfully")
	return redirect(url_for('login'))