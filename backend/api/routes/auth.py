# Path: backend\api\routes\auth.py
from flask import Flask, render_template, session, request, redirect, jsonify, url_for, flash
from flask import Blueprint, jsonify, current_app, render_template, redirect, url_for, request, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_jwt_extended import create_access_token

from flask_sqlalchemy import SQLAlchemy  
from sqlalchemy.exc import IntegrityError  

from utils.db import db
from utils.models import Users, SavedProjects, Projects
from utils.auth import bcrypt, login_manager

import requests
import os
import secrets

auth = Blueprint('auth', __name__)  # blueprint for auth routes

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


@auth.route('/github_login', methods=['GET', 'POST'])
def github_login():
    if request.method == 'GET':
        req_args = request.args
        if 'code' in req_args:
            code = req_args['code']
            # Define the parameters for the access token request
            token_params = {
                'client_id': current_app.config['GITHUB_CLIENT_ID'],
                'client_secret': current_app.config['GITHUB_CLIENT_SECRET'],
                'code': code
            }
            # Exchange the authorization code for an access token
            token_response = requests.post('https://github.com/login/oauth/access_token',
                                        params=token_params, headers={'Accept': 'application/json'})

            # Check for errors in the response
            token_response.raise_for_status()

            # Extract the access token from the response
            access_token = token_response.json().get('access_token')

            # Convert to bearer token
            bearer_token = "Bearer " + access_token

            # Use the access token to fetch the user's GitHub profile information
            profile_response = requests.get('https://api.github.com/user', headers={
                                            'Authorization': bearer_token, 'Accept': 'application/json'})
            
            # Extract the user's name from the GitHub profile information
            username = profile_response.json().get('login')

            # Create a JSON Web Token (JWT) for the user
            auth_token = create_access_token(identity=username)

            # Save the JWT to the user's session
            session['jwt_token'] = auth_token

            # If the username is already in the database, log the user in
            user = Users.query.filter_by(username=username).first()
            if user != None:
                login_user(user)
                return {'username': username, 'auth_token': auth_token}, 200

            else:
                # If the username is not in the database, create a new user
                email = profile_response.json().get('email')

                # Generate a random password for the user
                password = secrets.token_urlsafe(16)

                # Hash the password
                hashed_password = bcrypt.generate_password_hash(password)

                new_user = Users(username=username, password=hashed_password,  # create new user
                                    email=email)

                db.session.add(new_user)  # add new user to database

                db.session.commit()      # commit changes to database

                login_user(new_user)    # log in the new user

            return {'username': username, 'auth_token': auth_token}, 200

    return 'Something went wrong!', 200