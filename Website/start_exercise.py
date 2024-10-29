from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user, login_manager
from . import db
from datetime import datetime
from .frames_to_vid import png_to_mp4_multithreaded
import requests
import subprocess
import time
import os
import zipfile
from io import BytesIO

start_exercise = Blueprint('start_exercise', __name__)
batch_file_path = os.getcwd() + "\\Website\\run_unity_engine_no_engine.bat"
video_name = None


def stall_for_unity(folder_path):
    completion_path = os.path.join(folder_path, "completion.txt")
    while not(os.path.exists(completion_path)):
        time.sleep(1)

def get_fps(total_duration, num_frames):
    return int(num_frames/int(total_duration)) #round

def run_unity_animator(duration, number_of_frames):
    try:
        subprocess.run([batch_file_path], check= True)
    except Exception as e:
        print(f"Error executing the Unity Motion Capture animation project: {e}")

    try:
        input_folder = os.getcwd() + '\\Website\\animation\\MotionCapture_Data\\Animation Frames'
        stall_for_unity(input_folder)
        time_now = datetime.now().strftime("%Y%m%d_%H%M%S")
        vid_name = f"animation_{time_now}_.mp4"
        output_folder = os.getcwd() + f'\\Website\\static\\Animation Results\\{vid_name}'
        target_fps = get_fps(duration, number_of_frames)
        png_to_mp4_multithreaded(input_folder, output_folder, fps= target_fps)
        return vid_name
    except Exception as e:
        print(f"Error building video from frames in folder: {e}")
        return None

def send_script_request_to_pi(exercise_name, delay, duration, animate_flag, exercise_list):
    url = "http://10.0.0.161:5000/run_script"
    #TODO: Get fields from the front end through user input.
    #TODO: Integrate different payload if split is launched instead of just one exercise.
    payload = {
        "exercise_list": exercise_list,
        "script_name": exercise_name,
        "delay": delay, #s
        "time": duration, #s
        "animate": animate_flag, #default
    }
    try:
        response = requests.post(url, json= payload)
    except Exception as e:
        print(f"Failed to communicate with pi server: {e}")
    directory_path = os.path.join(os.getcwd(), "Website", "animation", "MotionCapture_Data")
    image_path = os.path.join(os.getcwd(), "Website", "static", "Snapshots")
    os.makedirs(image_path, exist_ok=True)
    if response and response.status_code == 200:
        with zipfile.ZipFile(BytesIO(response.content)) as z:
            for file in z.namelist():
                if file=="AnimationFileUnityData.txt":
                    file_name = os.path.join(directory_path, "AnimationFileUnityData.txt")
                    with open(file_name, 'wb') as f:
                        f.write(z.read(file))
                    print(f"File saved as {file_name}")
                elif file.endswith(".png"):
                    png_path = os.path.join(image_path, os.path.basename(file))
                    with open(png_path, 'wb') as f:
                        f.write(z.read(file))
                    print(f"Snapshot extracted to {png_path}")
        with open(file_name, 'r') as f:
            line_count = len(f.readlines())
        if animate_flag:
            video_name = run_unity_animator(duration, line_count)
            return video_name
    else:
        return response.json().get("output", "Error, no response from pi server")

@start_exercise.route("/start", methods=["GET", "POST"])
def start_page():
    if request.method == 'POST':
        print(request.form)
        exercise_delay = request.form['delay']
        exercise_duration = request.form['duration']
        exercise_animate = request.form.get('animate') == 'on' #true if checked, flase otherwise.
        exercise_name = request.form['exercise_name']
        #print(exercise_name, exercise_delay, exercise_duration, exercise_animate)
        #wrap in try to not crash website... 
        video_name = send_script_request_to_pi(exercise_name, exercise_delay, exercise_duration, exercise_animate, [])
        snapshots_dir = os.path.join(os.getcwd(),'Website', 'static', 'Snapshots')
        # Get list of PNG files in the folder
        png_files = [file for file in os.listdir(snapshots_dir) if file.endswith('.png')]
        
    return render_template('start_exercise.html', vid_name= video_name, png_files= png_files)


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






