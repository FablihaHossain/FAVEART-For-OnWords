# Initializing the Flask App
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from config import Config
from flask_bcrypt import Bcrypt

# Creating the Flask App
app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Database Connection (Admin User)
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}'.format(user=Config.user,pw=Config.password, host = "localhost", port = 5432 ,db=Config.db)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

# Database Connection (General User)
DB_URL_GENERAL = 'postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}'.format(user=Config.general_user,pw=Config.general_password, host = "localhost", port = 5432 ,db=Config.db)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL_GENERAL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

# Database Object
db = SQLAlchemy(app)

# Database Connection with general user credentials
try:
	conn = psycopg2.connect(user=Config.general_user, password=Config.general_password, host = "localhost", database=Config.db, port = 5432)
	print("Successully Connected to Database")
except:
	print("Unable to Connect to Database")

# Bcrypt Connection (For password hashing)
bcrypt = Bcrypt(app)

# File location for all the markers
MARKER_FOLDER = '../static/markers'
app.config['MARKER_FOLDER'] = MARKER_FOLDER

# Credit to https://flask.palletsprojects.com/en/1.1.x/quickstart/