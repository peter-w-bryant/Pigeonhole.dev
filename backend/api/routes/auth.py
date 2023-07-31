# Path: backend\api\routes\auth.py
from flask import Flask, render_template, session, request, redirect, jsonify, url_for, flash
from flask import Blueprint, jsonify, current_app, render_template, redirect, url_for, request, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from flask_sqlalchemy import SQLAlchemy  
from sqlalchemy.exc import IntegrityError  

from utils.db import db
from utils.models import Users, SavedProjects, Projects
from utils.auth import bcrypt, login_manager

import requests
import os
import secrets

auth = Blueprint('auth', __name__)  # blueprint for auth routes

def authenticate(username, password):
    # Get user object from database
    user = Users.query.filter_by(username=username).first()

    # Check if user exists and password is correct
    if user is not None and user.check_password(password):
        return user

    # Return None if authentication fails
    return None

@auth.route('/login', methods=['POST'])
def login():
    """Logs in a user
    :return: JSON Web Token (JWT) to be used for protected routes
    """
    if request.method == 'POST':
        data = request.get_json()
        user = authenticate(data['username'], data['password'])
        if user is None:
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Create access token
        access_token = create_access_token(identity=user.UID)
        return jsonify({'access_token': access_token}), 200
        
@auth.route('/logout', methods=['GET', 'POST'])
@jwt_required()
def logout():
    """Logs out a user
    return: Message indicating user has been logged out (status code 422 with invalid JWT, or status code 401 if no JWT)
    """
    logout_user()
    return jsonify({'message': 'User logged out'}), 200

@auth.route('/github_login', methods=['GET', 'POST'])
def github_login():
    if request.method == 'GET':
        data = request.get_json()
        code = data['code']
        if code != None:
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

            print("token_response: ", token_response.json())
            # Extract the access token from the response
            access_token = token_response.json().get('access_token')

            print("access_token: ", access_token)

            # Define the headers for the profile request
            profile_headers = {'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}

            # Use the access token to fetch the user's GitHub profile information
            profile_response = requests.get('https://api.github.com/user', headers=profile_headers)
            
            # Extract the user's name from the GitHub profile information
            username = profile_response.json().get('login')

            # If the username is already in the database, log the user in
            user = Users.query.filter_by(username=username).first()

            if user is None:
                # if the username is not in the database, create a new user
                email = profile_response.json().get('email') 
                password = secrets.token_urlsafe(16) # generate a random password for the user
                hashed_password = bcrypt.generate_password_hash(password)     # hash the password
                new_user = Users(username=username, password=hashed_password, # create new user
                                    email=email)
                db.session.add(new_user)  
                db.session.commit()     
                user = new_user

            login_user(user)
            auth_token = create_access_token(identity=username)
            return {'username': username, 'auth_token': auth_token}, 200
        
    return 'Something went wrong!', 400