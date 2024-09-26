from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user, login_manager
from . import db
from datetime import datetime
import requests

start_exercise = Blueprint('start_exercise', __name__)

def send_script_request_to_pi(exercise_name, delay, duration, animate_flag, exercise_list):
    url = "http://10.0.0.159:5000/run_script"
    #TODO: Get fields from the front end through user input.
    #TODO: Integrate different payload if split is launched instead of just one exercise.
    payload = {
        "exercise_list": exercise_list,
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
        send_script_request_to_pi(exercise_name, exercise_delay, exercise_duration, exercise_animate, [])
    return render_template('start_exercise.html')


@start_exercise.route("/start-split", methods=["GET", "POST"])
def start_split_page():
    #fetch the current set of exercises to launch based on user's split. 
    #this page is not attainable if a user does not have a split, so no need to null check it. 
    current_user_split = current_user.splits[0].content
    current_day = datetime.now().strftime("%A") #returns string of weekday name (i.e "Wednesday")
    exercise_list_for_today = current_user_split.get(current_day, None)
    print(exercise_list_for_today)
    if exercise_list_for_today: #if not rest...
        is_rest = False
        send_script_request_to_pi("", 10, 10, "false", exercise_list_for_today)
    else:
        is_rest = True
    return render_template('start_split.html', rest_flag = is_rest)

@start_exercise.route("/exercise", methods=['GET', 'POST'])
def exercise_landing_page():
    if request.method == 'POST':
        exercise_name = request.form['exercise_name']
    return render_template('exercise_landing.html', exercise_name= exercise_name)






