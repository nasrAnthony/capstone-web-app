from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user, login_manager
from . import db
import requests

start_exercise = Blueprint('start_exercise', __name__)

def send_script_request_to_pi(exercise_name, delay, duration, animate_flag):
    url = "http://10.0.0.159:5000/run_script"
    #TODO: Get fields from the front end through user input.
    #TODO: Integrate different payload if split is launched instead of just one exercise.
    payload = {
        "exerciseList": [],
        "script_name": exercise_name,
        "delay": delay, #s
        "time": duration, #s
        "animate": animate_flag, #default,
    }
    try:
        response = requests.post(url, json= payload)
    except Exception as e:
        print(f"Failed to communicate with pi server: {e}")
    #if response.status_code == 200:
    #    return response.json().get("output", "No Output")
    #else:
    #    return response.json().get("output", "No Error")

@start_exercise.route("/start", methods=["GET", "POST"])
def start_page():
    if request.method == 'POST':
        print(request.form)
        exercise_delay = request.form['delay']
        exercise_duration = request.form['duration']
        exercise_animate = request.form.get('animate') == 'on' #true if checked, flase otherwise.
        exercise_name = request.form['exercise_name']
        print(exercise_name, exercise_delay, exercise_duration, exercise_animate)
        #wrap in try to not crash website... 
        send_script_request_to_pi(exercise_name, exercise_delay, exercise_duration, exercise_animate)
    return render_template('start_exercise.html')

@start_exercise.route("/exercise", methods=['GET', 'POST'])
def exercise_landing_page():
    if request.method == 'POST':
        exercise_name = request.form['exercise_name']
    return render_template('exercise_landing.html', exercise_name= exercise_name)






