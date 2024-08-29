from flask import Flask
from getpass import getpass
from mysql.connector import connect, Error
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists
from flask_login import LoginManager, logout_user
import pickle

db = SQLAlchemy() #create db obj

def init_application():
    application = Flask(__name__)
    application.config['SECRET_KEY'] = 'sk2002' #random
    application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://tony:Aliame123@localhost/eHotelsDB'
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(application)
    from .models import User, Exercise, Workout
    