from application import app
from flask import render_template, request, url_for

# Defining basic route
@app.route("/"):
	return render_template("layout.html")