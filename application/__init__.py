# Initializing the Flask App
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from config import Config

# Creating the Flask App
app = Flask(__name__)
app.secret_key = Config.SECRET_KEY