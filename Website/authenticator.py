from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from datetime import date
import uuid
from sqlalchemy import or_
from . import db
from .models import User

authenticator = Blueprint('authenticator', __name__)
@authenticator.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        email = request.form.get('email')
    return render_template('login.html')

def validate_user(email, passwordv1, passwordv2, full_name, address, potential_user) -> bool:
    #catch dupe
    if potential_user:
        return (False, "Account exists with this email, please login instead")
    elif len(passwordv1) < 5:
        return (False, "Password is too short")
    elif passwordv1  != passwordv2:
        return (False, "Passwords do not match")
    elif full_name.strip() == "":
        return (False, "Please enter your name")
    elif(email.strip() == ""):
        return (False, "Please enter your email")
    elif(address.strip() == ""):
        return (False, "Please enter your address")
    return (True, "User input is valid")

@authenticator.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        passwordv1 = request.form.get('passwordTemp')
        passwordv2 = request.form.get('password')
        full_name = request.form.get('fullName')
        user_dob = request.form.get('dob')
        user_id= str(uuid.uuid4())
        user_dor = str(date.today())
        address = request.form.get('address')
        potential_user = User.query.filter(or_(User.email == email, User.id == user_id)).first()
        validate_result = validate_user(email, 
                                        passwordv1,
                                        passwordv2,
                                        full_name,
                                        address,
                                        potential_user
                                        )
        if validate_result[0]:
            current_user = User(
                    email= email, 
                    id= user_id, 
                    DOR = user_dor,
                    full_name= full_name, 
                    date_of_birth= user_dob, 
                    goal_weight= 0.0, 
                    goal_str = "", 
                    current_weight = 0.0, 
                    password= passwordv1
                )
            try:
                db.session.add(current_user)
                db.session.commit()
                flash(f"Account created! DOR: {user_dor}", category='success')
            except Exception:
                flash(f"Account creation failed, please try again.", category='error')
        else:
            flash(validate_result[1], category='error') #show user error message.
            

    return render_template('signup.html')