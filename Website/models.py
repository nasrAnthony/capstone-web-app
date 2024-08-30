from . import db
from flask_login import UserMixin
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
import pickle

Base = declarative_base()

class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.String(255), primary_key= True) #PK
    full_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique= True)
    password = db.Column(db.String(255))
    address = db.Column(db.String(255))
    date_of_birth = db.Column(db.String(255))
    current_weight = db.Column(db.Float)
    goal_weight = db.Column(db.Float)
    goal_str = db.Column(db.String(255))
    DOR = db.Column(db.String(255))


class Workout(db.Model):
    __tablename__ = 'Workout'
    workout_ID = db.Column(db.Integer, primary_key= True)
    workout_name = db.Column(db.String(255), unique= True)
    num_exercises = db.Column(db.Integer)
    pause_interval = db.Column(db.Float)
    #exercises = db.relationship(
    #    'Exercise', 
    #    back_populates= 'workout_playlist'
    #)

class Exercises(db.Model):
    __tablename__ = 'Exercises'
    exercise_ID = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(255), unique= True)
    level = db.Column(db.String(255))
    description = db.Column(db.String(255))
    image_resource_path = db.Column(db.String(255))
    #workout_playlist = db.relationship('Workout',
    #                                back_populates= 'exercises'
    #                            )
