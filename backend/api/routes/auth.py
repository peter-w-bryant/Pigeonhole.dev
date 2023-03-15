# Path: backend\api\routes\auth.py
from flask import Flask, render_template, session, request, redirect, jsonify, url_for, flash
from flask import Blueprint, jsonify, current_app, render_template, redirect, url_for, request, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy  # for database
from sqlalchemy.exc import IntegrityError  # for handling duplicate entries

from flask_dance.contrib.github import make_github_blueprint, github

from utils import GitHubAPIWrapper, fetch_all_projects
from utils.db import db
from utils.models import Users, SavedProjects
from utils.auth import bcrypt, login_manager

import requests
import os
import secrets

auth = Blueprint('auth', __name__)  # blueprint for auth routes

@auth.route('/register', methods=['POST'])
def register():
    """Registers a new user"""
    if request.method == 'POST':
        data = request.get_json()
        try:
            # check if username already exists
            user = Users.query.filter_by(username=data['username']).first()

            if user != None:
                return 'Username already exists!', 409  # return error message

            hashed_password = bcrypt.generate_password_hash(
                data['password'])  # hash password

            new_user = Users(username=data['username'], password=hashed_password,  # create new user
                             email=data['email'])

            db.session.add(new_user)  # add new user to database
            db.session.commit()      # commit changes to database
            return 'User created successfully!', 201  # return success message

        except IntegrityError:
            return 'Username already exists!', 409   # return error message

        except Exception as e:
            print(e)
            return str(e), 500

@auth.route('/login', methods=['POST'])
def login():
    """Logs in a user"""
    if request.method == 'POST':
        data = request.get_json()
        user = Users.query.filter_by(username=data['username']).first()
        if user != None:
            if bcrypt.check_password_hash(user.password, data['password']):
                login_user(user)
                return 'Logged in successfully!', 200

            return 'Incorrect password!', 401
        else:
            return 'Username not found!', 401 
        
@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return 'Logged out successfully!', 200

@auth.route('/save-project', methods = ['GET', 'POST'])
@login_required
def save_project():
    """Saves a project to the user's saved projects list"""
    if request.method == 'POST':
        data = request.get_json()
        user = Users.query.filter_by(username=data['username']).first()
        if user != None:
            project_exists = SavedProjects.query.filter_by(user['UID'], data['pUID']).first()
            if project_exists != None:
                return {"error": "Project already saved!"}, 403
            else:
                new_project = SavedProjects(user['UID'], data['pUID'])
                SavedProjects.add(new_project)
                return {"success": "Project added successfully!"}, 200 

@auth.route('/github_callback')
def github_callback():
    """Handle the response from Github after authorization."""
    code = request.args.get('code')

    # Send the authorization code to the Github API to retrieve an access token
    response = requests.post(
        'https://github.com/login/oauth/access_token',
        data={
            'client_id': current_app.config['GITHUB_CLIENT_ID'],
            'client_secret': current_app.config['GITHUB_CLIENT_SECRET'],
            'code': code
        },
        headers={
            'Accept': 'application/json'
        }
    )

    # Parse the Github API response to retrieve the access token
    data = response.json()
    access_token = data['access_token']

    # Save the access token to the user's session or database
    session['access_token'] = access_token

    # Redirect the user back to the React app
    return redirect('http://localhost:3000/')
