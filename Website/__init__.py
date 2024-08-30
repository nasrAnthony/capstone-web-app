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
    application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://tony:Aliame123@localhost/dumbbelldore'
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(application)
    from .authenticator import authenticator
    from .home import home_page
    from .profile import display_profile
    from .models import User, Exercise, Workout
    #if(database_exists('mysql+pymysql://tony:Aliame123@localhost/dumbbelldore')):
    #    print('Database already exists!')
    #else:
    with application.app_context():
        db.create_all() #create the tables in the database
        print('Database not found. A new one was created!')
    login_manager = LoginManager()
    login_manager.login_view = 'authenticator.login'
    login_manager.init_app(application)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)
    
    application.register_blueprint(home_page, url_prefix='/') #no prefix
    application.register_blueprint(authenticator, url_prefix= '/')
    application.register_blueprint(display_profile, url_prefix='/')
    
    return application
