import os
import psycopg2
from config import Config
from application import app, db, conn
from flask import render_template, request, url_for, session, flash, redirect, send_from_directory
from models import Users, Paths, Checkpoints, Interactions
from database import Database
from werkzeug import secure_filename
from datetime import datetime
from sqlalchemy import asc, desc

# Defining basic route (homepage of the site)
@app.route("/")
def index():
	return render_template("layout.html")

# About This Site Page
@app.route("/about")
def about():
	return render_template("about.html")

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

			# Validating login credentials
			valid = Database.validate_login(username, password)

			#If valid, creates a flash session with username and user_id
			if valid:
				# Getting the user_id of the current user
				user_id = Database.get_userId(username)

				# Getting the role of current user
				role = Database.select_where("users", "user_id", user_id, "role")

				# Creating a session with the user data
				session['username'] = username
				session['user_id'] = user_id 
				session['role'] = role

				# Taking the user to the homepage
				return redirect(url_for('homepage'))

			else:
				flash("Invalid Login! Please Try Again")
	return render_template("login.html")

# Register Page
@app.route("/register", methods = ['GET', 'POST'])
def register():
	if request.method == "POST":
		try:
			# Getting the information from all the fields
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

					# Redirecting the user to login page in order to access site
					return redirect(url_for('login'))
		except Exception as error: # Exception Handling to avoid program crashing when a role is choosen 
			flash("Please Choose a Role!")
	return render_template("register.html")

# Home Page
@app.route("/homepage")
def homepage():
	if not session.get('username'):
		return redirect(url_for('login'))

	# Getting all the paths in the database
	paths_list = Paths.query.all()

	# Passing all the paths from the db to the homepage
	return render_template("homepage.html", paths = paths_list)

# Create Paths Page
# Pathmakers Only
@app.route("/createPaths",  methods = ['GET', 'POST'])
def createPath():
	if not session.get('username') and not session.get('user_id'):
		return redirect(url_for('login'))
	elif not session.get('role') == "pathmaker":
		return redirect(url_for('homepage'))
	else:
		if request.method == "POST":
			try:
				# Getting all information in the form and storinbg them into sessions
				pathname = request.form['pathname']
				session['pathname'] = pathname
				description = request.form['description']
				session['description'] = description
				format_chosen = request.form['format']
				session['format_chosen'] = format_chosen
				numOfCheckpoints = request.form.get("checkpointNum")
				session['numOfCheckpoints'] = str(numOfCheckpoints)

				# Invalid Input Checking
				if "" in [pathname, description] or numOfCheckpoints == "Choose Number of Checkpoints Here...":
					flash("Error! Fields Cannot be Empty!")
				else:
					# Getting the user id of the pathmaker
					user_id = session.get('user_id')

					# Getting the name of the pathmaker
					firstname = Database.select_where("users", "user_id", user_id, "firstname")
					lastname = Database.select_where("users", "user_id", user_id, "lastname")
					pathmaker = firstname + " " + lastname
					session['pathmaker'] = pathmaker

					# Going to the create checkpoints page 
					return redirect(url_for('createCheckpoint', numOfCheckpoints = numOfCheckpoints))
			except Exception as error: # Exception Handling to avoid program crashing when a format is chosen
				flash("Please Choose a Base Format for the Path!")
		return render_template("createPaths.html")

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

# Getting all the possible markers
markers_list = []
marker_pathfile = open("application/data/markers.txt", "r")
for marker in marker_pathfile:
	markers_list.append(marker.strip())

# Create Checkpoints
# Pathmakers Only
@app.route("/createCheckpoint", methods = ['GET', 'POST'])
def createCheckpoint():
	if not session.get('username') and not session.get('user_id'):
		return redirect(url_for('login'))
	elif not session.get('role') == "pathmaker":
		return redirect(url_for('homepage'))
	elif not session.get('pathname') or not session.get('numOfCheckpoints'):
		return redirect(url_for('createPath'))
	else:
		# Getting the number of checkpoints the user chose for path
		numOfCheckpoints = session.get('numOfCheckpoints')

		# Creating lists to store the checkpoint information
		checkpointTexts = []
		checkpointAnimations = []
		checkpointColors = []
		checkpointFonts = []
		checkpointLatitudes = []
		checkpointLongitudes = []
		markerNames = []
		markerFilenames = []

		# Getting all the form data
		if request.method == "POST":
			# Parsing through each checkpoint form card
			for x in range(1, (int(numOfCheckpoints)+1)):
				# Getting the text of the current checkpoint and adding to list
				textNum = "text" + str(x)
				text = request.form.get(textNum)
				checkpointTexts.append(text)

				# Getting the animation of the current checkpoint and adding to list
				animationNum = "animations" + str(x)
				animation = request.form.get(animationNum)
				checkpointAnimations.append(animation)

				# Getting the color of the current checkpoint and adding to list
				colorNum = "colors" + str(x)
				color = request.form.get(colorNum)
				checkpointColors.append(color)

				# Getting the font of the current checkpoint and adding to list
				fontNum = "fonts" + str(x)
				font = request.form.get(fontNum)
				checkpointFonts.append(font)

				# Geolocation Path
				if session.get('format_chosen') == "geolocation":
					# Getting the latitude of the current checkpoint and adding to the list
					latitudeNum = "latitude" + str(x)
					latitude = request.form.get(latitudeNum)
					checkpointLatitudes.append(latitude)

					# Getting the longitude of the current checkpoint and adding to the list
					longitudeNum = "longitude" + str(x)
					longitude = request.form.get(longitudeNum)
					checkpointLongitudes.append(longitude)

				# Marker Path
				if session.get('format_chosen') == "marker":
					# Getting the marker of the current checkpoint and adding to the list
					markerNum = "markers" + str(x)
					marker = request.form.get(markerNum)
					markerNames.append(marker)
					# Marker list for pdk files
					marker_filename = marker + ".pdf"
					markerFilenames.append(marker_filename)

			# Ensuring that none of the data is NoneType or not filled properly
			if "" in checkpointTexts or "Choose An Animation..." in checkpointAnimations or "Choose A Font..." in checkpointFonts or "" in checkpointLongitudes or "" in checkpointLatitudes or "Choose A Marker..." in markerNames:
				flash("Error! Please complete all fields")
			elif Database.duplicate_markers(markerNames):
				flash("Error! Markers cannot duplicate in a path")
			else:
				# Storing all data in the session
				session['checkpointTexts'] = checkpointTexts
				session['checkpointAnimations'] = checkpointAnimations
				session['checkpointColors'] = checkpointColors
				session['checkpointFonts'] = checkpointFonts

				# Storing geolocation coordinates in session 
				if session.get('format_chosen') == "geolocation":
					session['checkpointLatitudes'] = checkpointLatitudes
					session['checkpointLongitudes'] = checkpointLongitudes
				# Storing marker names in session
				if session.get('format_chosen') == "marker":
					session['markerNames'] = markerNames
					session['markerFilenames'] = markerFilenames

				# Redirecting the path detail page
				return redirect(url_for('pathDetails'))
		return render_template("createCheckpoint.html", animations_list = animations_list, fonts_list = fonts_list, markers_list = markers_list)

# Finalize Path Details before creating
# Pathmakers only 
@app.route("/pathDetails", methods = ['GET', 'POST'])
def pathDetails():
	if not session.get('username'):
		return redirect(url_for('login'))
	if not session.get('role') == "pathmaker":
		return redirect(url_for('homepage'))
	# Redirects to form if no path or checkpoint information stored in session
	if not session.get('pathname') or not session.get('checkpointTexts'):
		return redirect(url_for('createPath'))

	# Path Creation
	if request.method == "POST":
		if request.form.get('pathCreation') == 'createPath':
			# Getting all the data for checkpoints and path from session
			pathname = session.get('pathname')
			description = session.get('description')
			pathmaker = session.get('pathmaker')
			format_chosen = session.get('format_chosen')
			numOfCheckpoints = session.get('numOfCheckpoints')
			checkpointTexts = session.get('checkpointTexts')
			checkpointAnimations = session.get('checkpointAnimations')
			checkpointColors = session.get('checkpointColors')
			checkpointFonts = session.get('checkpointFonts')

			# Getting geolocation coordinates 
			if format_chosen == "geolocation":
				checkpointLatitudes = session.get('checkpointLatitudes')
				checkpointLongitudes = session.get('checkpointLongitudes')
			# Getting marker choices 
			if format_chosen == "marker":
				markerNames = session.get('markerNames')

			# Creating a new list to store checkpoint ids
			checkpointIDs = []

			# Adding each checkpoint in the db
			for y in range(1, (int(numOfCheckpoints)+1)):
				# Current Geolocation for checkpoint
				if format_chosen == "geolocation":
					# Developing the geolocation
					currentLatitude = float(checkpointLatitudes[y-1])
					currentLongitude = float(checkpointLongitudes[y-1])
					geolocation = {currentLatitude, currentLongitude}
					marker = "no_marker"

				# Current marker for checkpoint
				if format_chosen == "marker":
					marker = markerNames[y-1]
					geolocation = []

				# Getting the next possible path_id
				path_id = Database.next_id("paths")

				# Adding the new checkpoint in the database
				Database.insert_checkpoint(checkpointTexts[y-1], checkpointAnimations[y-1], checkpointColors[y-1], geolocation, checkpointFonts[y-1], marker, path_id)
				
				# Getting the checkpoint id and putting them in the list
				checkpoint_id = Database.getCheckpointID(checkpointTexts[y-1], checkpointAnimations[y-1], checkpointColors[y-1], checkpointFonts[y-1])
				checkpointIDs.append(checkpoint_id)

				# Storing the list into the session
				session['checkpointIDs'] = checkpointIDs

			# Empty interactions for now
			interactions = []
			# Creating the path and adding it to the database
			Database.insert_path(pathname, description, checkpointIDs, interactions, pathmaker, "public", format_chosen)
		

			# After path insertion, pathmaker is redirected to the homepage
			flash("New Path Created!")
			return redirect(url_for('homepage'))

		# Path Cancellation
		if request.form.get('pathCreation') == 'cancelPath':
			# Clearing the session data
			session.pop('pathname', None)
			session.pop('description', None)
			session.pop('pathmaker', None)
			session.pop('format_chosen', None)
			session.pop('numOfCheckpoints', None)
			session.pop('checkpointTexts', None)
			session.pop('checkpointAnimations', None)
			session.pop('checkpointColors', None)
			session.pop('checkpointFonts', None)
			session.pop('checkpointLatitudes', None)
			session.pop('checkpointLongitudes', None)
			session.pop('markerNames', None)
			session.pop('markerFilenames', None)

			# Returning to homepage
			flash("Path Creation Canceled")
			return redirect(url_for('homepage'))
	return render_template("pathDetails.html")

# Download Markers
@app.route('/../static/markers/<path:filename>')
def downloadMarkerFile(filename):
	marker_file = os.path.join(app.config['MARKER_FOLDER'], filename)
	return send_from_directory(directory = marker_file, filename = filename)

# Viewing the list of checkpoints in a given path
# Pathmaker's can view their path checkpoints
@app.route("/viewCheckpoints/<int:pathID>", methods = ['GET', 'POST'])
def viewCheckpoints(pathID):
	if not session.get('username'):
		return redirect(url_for('login'))
	
	# Getting the current path, given the path id
	current_path = Paths.query.filter_by(path_id = pathID).first()

	#Getting all the checkpoints in the database
	checkpoint_list = Checkpoints.query.all()

	# Passing path data and all potential checkpoints in the db
	return render_template("viewCheckpoints.html", path = current_path, points = checkpoint_list)

# The route that allows pathmakers to visualize specific checkpoints 
@app.route("/checkpointVisual/<int:checkpointID>")
def checkpointVisual(checkpointID):
	if not session.get('username'):
		return redirect(url_for('login'))

	# Getting the details for the checkpoint given the ID
	current_checkpoint = Checkpoints.query.filter_by(checkpoint_id = checkpointID).first() 

	return render_template("checkpointVisual.html", checkpoint = current_checkpoint, fonts_list = fonts_list)

# Route allowing explorers to visualize the entire path with all checkpoints
@app.route("/explorePath/<int:path_id>", methods = ['GET', 'POST'])
def explorePath(path_id):
	if not session.get('username'):
		return redirect(url_for('login'))

	# Getting the path information based on path id
	current_path = Paths.query.filter_by(path_id = path_id).first()

	# Getting the list of checkpoints based on the path and the number of checkpoints
	checkpointIdList = Database.select_where("paths", "path_id", path_id, "checkpoints")
	numOfCheckpoints = len(checkpointIdList)

	if request.method == "POST":
		if request.form.get('logInteraction') == "interaction":
			# Getting the number of the checkpoint the explorer would like to log in
			loggedCheckpointNum = request.form.get('checkpointNumber')

			# Ensuring that it continues only if they choose an appropriate number
			if loggedCheckpointNum != "Checkpoint Number":
				# Getting the associated checkpoint id
				checkpoint_id = checkpointIdList[int(loggedCheckpointNum)-1]

				# Getting the user_id of the user
				user_id = session.get('user_id')

				# Checking if the interaction has already been logged or not
				interaction_already = Database.interaction_check(path_id, checkpoint_id, user_id)

				if not interaction_already:
					# Getting the current date and time
					dateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

					# Logging the interaction in the database
					Database.insert_interaction(path_id, checkpoint_id, user_id, dateTime)
					print("Logged Interaction")
				else:
					print("Interaction Already Logged")
	# Getting the base format of the path
	base_format = Database.select_where("paths", "path_id", path_id, "base_format")

	# Getting the list of checkpoints and adding them to a list
	# Addtionally getting the list of coordinates if location based
	listOfCheckpoints = []
	listOfLatitudes = []
	listOfLongitudes = []
	for checkpoint_id in checkpointIdList:
		# Getting current checkpoint based on id number
		checkpoint = Checkpoints.query.filter_by(checkpoint_id = checkpoint_id).first()
		listOfCheckpoints.append(checkpoint)

		# Getting the marker associated with it
		if base_format == "marker":
			marker = Database.select_where("checkpoints", "checkpoint_id", checkpoint_id, "marker")

		# Getting the geographical coordinates
		if base_format == "geolocation":
			geo_coordinates = Database.select_where("checkpoints", "checkpoint_id", checkpoint_id, "geolocation")
			# Latitude of checkpoint 
			latitude = geo_coordinates[0]
			listOfLatitudes.append(latitude)

			# Longitude of checkpoint
			longitude = geo_coordinates[1]
			listOfLongitudes.append(longitude)

	return render_template("explorePath.html", numOfCheckpoints = numOfCheckpoints, base_format = base_format, checkpointList = listOfCheckpoints, latitudeList = listOfLatitudes, longitudeList = listOfLongitudes, checkpointIdList = checkpointIdList)

# Admin Route to Manage Users of Database
@app.route("/manageUsers", methods = ['GET', 'POST'])
def manageUsers():
	if not session.get('username'):
		return redirect(url_for('login'))
	elif not session.get('role') == "admin":
		return redirect(url_for('homepage'))

	# Getting all users in the database (in order by user_id)
	user_list = Users.query.order_by(asc(Users.user_id))

	if request.method == "POST":
		# User Deletion
		if request.form.get('user_deletion') == 'deleted_user':
			# Getting the user's id number
			user_id = request.form.get('user_id')

			if user_id != None:
				# Getting the user's email address 
				email = Database.select_where("users", "user_id", int(user_id), "email")

				# Deleting the entry
				Database.delete_from("users", "user_id", int(user_id), "email", email)
				return redirect(url_for("manageUsers"))

		# User Information Edits
		if request.form.get('user_change') == 'change_submitted':
			# Getting the current user_id
			user_id = request.form.get('user_id')

			# Getting all current user information
			currentFirstname = Database.select_where("users", "user_id", int(user_id), "firstname")
			currentLastname = Database.select_where("users", "user_id", int(user_id), "lastname")
			currentEmail = Database.select_where("users", "user_id", int(user_id), "email")
			currentRole = Database.select_where("users", "user_id", int(user_id), "role")

			# Getting all new information
			new_firstname = request.form.get('firstname')
			new_lastname = request.form.get('lastname')
			new_email = request.form.get('email')
			new_role = request.form.get('role')

			# Updating If New Information is Given
			if new_firstname != currentFirstname:
				Database.update_table("users", "user_id", int(user_id), "firstname", new_firstname)
			if new_lastname != currentLastname:
				Database.update_table("users", "user_id", int(user_id), "lastname", new_lastname)
			if new_email != currentEmail:
				Database.update_table("users", "user_id", int(user_id), "email", new_email)
			if new_role != currentRole:
				Database.update_table("users", "user_id", int(user_id), "role", new_role)

			return redirect(url_for("manageUsers"))
	return render_template("manageUsers.html", users = user_list)

# Admin Route to Manage Paths of Database
@app.route("/managePaths", methods = ['GET', 'POST'])
def managePaths():
	if not session.get('username'):
		return redirect(url_for('login'))
	elif not session.get('role') == "admin":
		return redirect(url_for('homepage'))

	# Getting all the paths in the database (in order by path_id)
	paths_list = Paths.query.order_by(asc(Paths.path_id))

	# Getting all users in the database
	user_list = Users.query.all()

	#Getting all the checkpoints in the database
	checkpoint_list = Checkpoints.query.all()

	#Getting all the interactions in the database
	interaction_list = Interactions.query.all()

	if request.method == "POST":
		if request.form.get('path_change') == 'change_submitted':
			# Getting the ID of the path intended to change
			path_id = request.form.get('path_id')

			# Getting the current path data from the db
			currentName = Database.select_where("paths", "path_id", int(path_id), "name")
			currentDescription = Database.select_where("paths", "path_id", int(path_id), "description")
			currentPathmaker = Database.select_where("paths", "path_id", int(path_id), "pathmaker")

			# Getting the new pathname and description from the fields
			new_pathname = request.form.get('pathname')
			new_pathdescription = request.form.get('description')

			# Getting the id of the pathmaker chosen
			pathmaker_id = request.form.get('pathmaker')
			pathmakerFirstName = Database.select_where("users", "user_id", int(pathmaker_id), "firstname")
			pathmakerLastName = Database.select_where("users", "user_id", int(pathmaker_id), "lastname")
			newPathmaker = pathmakerFirstName + " " + pathmakerLastName
			
			# Checking to see if there are any changes
			# Updating accordingly
			if new_pathname != currentName:
				Database.update_table("paths", "path_id", int(path_id), "name", new_pathname)
			if new_pathdescription != currentDescription:
				Database.update_table("paths", "path_id", int(path_id), "description", new_pathdescription)
			if newPathmaker != currentPathmaker:
				Database.update_table("paths", "path_id", int(path_id), "pathmaker", newPathmaker)

			# Refreshing the page
			return redirect(url_for("managePaths"))
		if request.form.get('path_deletion') == 'deletion_activated':
			# Getting the Path ID of the Soon to Be Deleted Path
			path_id = request.form.get('path_id')
			if path_id != None:
				# Getting the pathmaker of the path
				pathmaker = Database.select_where("paths", "path_id", int(path_id), "pathmaker")

				# Deleting the Path from Database
				Database.delete_from("paths", "path_id", int(path_id), "pathmaker", pathmaker)

				# Refreshing the page
				return redirect(url_for("managePaths"))
	return render_template("managePaths.html", users = user_list, paths = paths_list, checkpoints = checkpoint_list, interactions = interaction_list)

# Logging Out redirects to login page
@app.route("/logout")
def logout():
	# Clearing the session data
	session.pop('username', None)
	session.pop('user_id', None)
	session.clear()

	# Log Out Messages
	flash("You have logged out sucessfully")
	return redirect(url_for('login'))
# Credit to https://stackoverflow.com/questions/5306079/python-how-do-i-convert-an-array-of-strings-to-an-array-of-numbers
# Credit to https://stackoverflow.com/questions/24577349/flask-download-a-file