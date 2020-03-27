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
		if request.form['username'] == "" or request.form['password'] == "":
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
		try:
			firstname = request.form['firstname']
			lastname = request.form['lastname']
			email = request.form['email']
			username = request.form['username']
			password = request.form['password']
			role = request.form['roles']

		# None of the fields can be empty
			if "" in [firstname, lastname, email, username, password, role]:
				flash("Error! Fields Cannot be Empty!")
			else:
				# Checking to see if username already exists in the database
				user_check = Database.check_duplicate("users", "username", username)

				# Checking to see if the email already exists in the database
				email_check = Database.check_duplicate("users", "email", email)

				# If username and/or email exists in the database, it'll flash an error message
				if user_check:
					flash("Error! Username already exists.... Try another one")
				elif email_check:
					flash("Error! Email already exists... Try another one")
				else:
					# Adding the user to the database
					Database.insert_user(firstname, lastname, email, username, password, role)
					flash("Congratulations! You've been registers to FAVEART For OnWords Successfully!")
					return redirect(url_for('login'))
		except Exception as error: # Exception Handling to avoid program crashing when a role is choosen 
			flash("Please Choose a Role!")
	return render_template("register.html")

# Home Page
@app.route("/homepage")
def homepage():
	if not session.get('username'):
		return redirect(url_for('login'))

	# Getting all the paths from the database
	paths_list = Paths.query.all()
	return render_template("homepage.html", paths = paths_list)

# Create Paths Page
@app.route("/createPaths",  methods = ['GET', 'POST'])
def createPath():
	if not session.get('username') and not session.get('user_id'):
		return redirect(url_for('login'))
	else:
		#Getting all the checkpoints in the database
		checkpoint_list = Checkpoints.query.all()

		# Getting all information in the form
		if request.method == "POST":
			pathname = request.form['pathname']
			description = request.form['description']
			checkpoints_str = request.form.getlist("checkpoints")

			# Invalid Input Checking
			if "" in [pathname, description]:
				flash("Error! Fields Cannot be Empty!")
			elif len(checkpoints_str) > 5:
				flash("Error! You Must Choose Only 5 Checkpoints")
			elif len(checkpoints_str) < 1:
				flash("Error! You must choose at least one checkpoint!")
			else:
				# Casting all the text values in the checkpoints list from form
				checkpoint_ints = [int(num) for num in checkpoints_str]

				# Empty interactions for now
				interactions = []

				# Getting the user id of the pathmaker
				user_id = session.get('user_id')

				# Getting the name of the pathmaker
				firstname = Database.select_where("users", "user_id", user_id, "firstname")
				lastname = Database.select_where("users", "user_id", user_id, "lastname")
				pathmaker = firstname + " " + lastname

				# Adding the path data to the database
				Database.insert_path(pathname, description, checkpoint_ints, interactions, pathmaker, "public")
				flash("New Path Created!")

				# Redirecting to homepage
				return redirect(url_for('homepage'))
		return render_template("createPaths.html", checkpoints = checkpoint_list)

# Getting all the possible animations
animations_list = []
animations_pathfile = open("application/data/animations.txt", "r")
for animation in animations_pathfile:
	animations_list.append(animation.strip())

# Getting all the possible fonts
fonts_list = []
fonts_pathfile = open("application/data/fonts.txt", "r")
for font in fonts_pathfile:
	fonts_list.append(font.strip())

# Create Checkpoints
@app.route("/createCheckpoint", methods = ['GET', 'POST'])
def createCheckpoint():
	# Getting all the form data
	if request.method == "POST":
		text = request.form['text']
		animation = request.form.get("animations")
		color = request.form.get("colors")
		font = request.form.get("fonts")
		
		if text == "" or animation == "Choose An Animation..." or color == "Choose A Color..." or font == "Choose A Font...":
			flash("Error! Please Complete the Entire Form!")
		else:
			# No geolocations for now
			geolocation = []
			Database.insert_checkpoint(text, animation, color, geolocation, font)
			flash("New Checkpoint Created!")
			return redirect(url_for('createPath'))

	return render_template("createCheckpoint.html", animations_list = animations_list, fonts_list = fonts_list)

# Logging Out redirects to login page
@app.route("/logout")
def logout():
	# Clearing the session data
	session.pop('username', None)
	session.pop('user_id', None)

	# Log Out Messages
	flash("You have logged out sucessfully")
	return redirect(url_for('login'))

@app.route("/viewCheckpoints/<int:pathID>", methods = ['GET', 'POST'])
def viewCheckpoints(pathID):
	if not session.get('username'):
		return redirect(url_for('login'))
	
	# Getting the current path, given the path id
	current_path = Paths.query.filter_by(path_id = pathID).first()

	# Getting the list of all checkpoints in the database
	checkpoint_list = Checkpoints.query.all()

	return render_template("viewCheckpoints.html", path = current_path, points = checkpoint_list)

# The AR Component
@app.route("/checkpointVisual/<int:checkpointID>")
def checkpointVisual(checkpointID):
	# if not session.get('username'):
	# 	return redirect(url_for('login'))

	# Getting the details for the checkpoint given the ID
	current_checkpoint = Checkpoints.query.filter_by(checkpoint_id = checkpointID).first()
	return render_template("checkpointVisual.html", checkpoint = current_checkpoint, fonts_list = fonts_list)

if __name__ == "__main__":
    app.run(ssl_context='adhoc')

# Credit to https://stackoverflow.com/questions/5306079/python-how-do-i-convert-an-array-of-strings-to-an-array-of-numbers
