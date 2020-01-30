from application import app, db
from flask import render_template, request, url_for
from models import Users, Paths, Checkpoints, Interactions

# Defining basic route
@app.route("/")
def index():
	user_list = Users.query.all()
	return render_template("layout.html", users = user_list)