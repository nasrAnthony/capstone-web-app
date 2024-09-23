from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user, login_manager
from . import db
import requests

exercise_landing = Blueprint('exercise_landing', __name__)

def send_script_request_to_pi(script_name):
    url = "http://10.0.0.159:5000/run_script"
    #TODO: Get fields from the front end through user input.
    #TODO: Integrate different payload if split is launched instead of just one exercise.
    payload = {
        "exerciseList": [],
        "script_name": script_name,
        "delay": 4, #s
        "time": 10, #s
        "animate": False, #default,
    }
    response = requests.post(url, json= payload)
    #if response.status_code == 200:
    #    return response.json().get("output", "No Output")
    #else:
    #    return response.json().get("output", "No Error")

@exercise_landing.route("/launch-exercise", methods=['GET', 'POST'])
def exercise_landing_page():
    return render_template('exercise_landing.html')




