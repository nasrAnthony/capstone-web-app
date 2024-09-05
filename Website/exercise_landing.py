from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user, login_manager
from . import db
import requests



exercise_landing = Blueprint('exercise_landing', __name__)



def send_script_request_to_pi(script_name):
    url = "http://10.0.0.163:5000/run_script"
    payload = {
        "script_name": script_name,
    }
    response = requests.post(url, json= payload)
    if response.status_code == 200:
        return response.json().get("output", "No Output")
    else:
        return response.json().get("output", "No Error")
    
@exercise_landing.route("/launch-exercise", methods=['GET', 'POST'])#decorator
def exercise_landing_page():
    if request.method == 'POST':
        exercise_name = request.form['exercise_name']
        print(exercise_name)
        send_script_request_to_pi(exercise_name)
    return render_template('exercise_landing.html')

