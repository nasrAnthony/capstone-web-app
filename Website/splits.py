from . import db
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user, login_manager
from .models import User
import pickle


splits_page = Blueprint('splits', __name__)

@splits_page.route('/splits', methods=['GET', 'POST'])
@login_required
def splits():
    return render_template('splits.html')

@splits_page.route('/create_splits', methods=['POST'])
@login_required
def create_splits():
    if request.method == 'POST':
        split_data = request.get_json()  # Get the JSON data from the request

        # Process the split_data here (e.g., store it in the database)
        # For example:
        for day, exercises in split_data.items():
            print(f"{day}: {exercises}")  # For debugging purposes

        flash('Workout split created successfully!', 'success')

        # Redirect to another page (e.g., back to the splits page)
        return redirect(url_for('splits.splits'))




