# Path: backend\api\routes\auth.py
from flask import request, jsonify, Blueprint, current_app
from flask_login import login_user, logout_user, current_user
from flask_jwt_extended import create_access_token, jwt_required

from utils.db import db
from utils.models import Users
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

@auth.route('/auth/login', methods=['POST'])
def login():
    """
    Logs in a user given login credentials, returns a JWT (access token).
    ---
    tags:
    - Auth
    parameters:
    - name: User JSON object
      in: body
      required: true
      description: A JSON object containing the username and password of the user.
      schema:
        type: object
        properties:
          username:
            type: string
            description: The username of the user.
            example: testuser
          password:
            type: string
            description: The password of the user.
            example: testpassword
    responses:
      200:
          description: User logged in successfully, returns access token
      401:
          description: Invalid username or password, returns error message
    """
    if request.method == 'POST':
        data = request.get_json()
        user = authenticate(data['username'], data['password'])
        if user is None:
            return jsonify({'error': 'Invalid username or password'}), 401
        access_token = create_access_token(identity=user.UID)
        login_user(user)
        return jsonify({'access_token': access_token}), 200

@auth.route('/auth/logout', methods=['GET'])
@jwt_required()
def logout():
    """
    Logs out a user if they are logged in, requires an access token in the request header.
    ---
    tags:
      - Auth
    parameters:
    - name: Authorization
      in: header
      required: true
      description: "The JWT of the current user. The required header format is: **{'Authorization: Bearer {JWT}'}**"
      example: Bearer <JWT_token>
      schema:
        type: object
        properties:
          access_token:
            type: string
            description: The access token of the user.
            example: access_token
    responses:
      200:
          description: User logged out successfully, returns success message
      401:
          description: Invalid access token, returns error message
    """
    logout_user()
    return jsonify({'message': 'User logged out'}), 200

@auth.route('/auth/github_login', methods=['POST'])
def github_login():
    """
    Logs in a user using GitHub OAuth and returns an access token.
    ---
    tags:
      - Auth
    parameters:
    - name: code
      in: body
      required: true
      description: The authorization code returned by GitHub OAuth.
      schema:
        type: object
        properties:
          code:
            type: string
            description: The authorization code returned by GitHub OAuth.
            example: aah17ka93ka045kal39ak
    responses:
      200:
          description: User logged in successfully, returns access token, username, and status
      401:
          description: Invalid authorization code, returns status and error message
    """
    if request.method == 'POST':
        data = request.get_json()
        code = data['code']
        if code != None: # GitHub OAuth code is present
            # Define the parameters for the access token request
            token_params = {
                'client_id': current_app.config['GITHUB_CLIENT_ID'],
                'client_secret': current_app.config['GITHUB_CLIENT_SECRET'],
                'code': code
            }

            # TODO: remove! testing_access_token is used for testing purposes
            testing_access_token = request.args.get('testing_access_token')
            if testing_access_token is None:
                # Exchange the authorization code for an access token
                token_response = requests.post('https://github.com/login/oauth/access_token',
                                               params=token_params, headers={'Accept': 'application/json'})

                token_response.raise_for_status()  # Check for errors in the response
                # Extract the access token from the response
                access_token = token_response.json().get('access_token')
            else:
                # Use the testing access token
                access_token = os.environ.get('GITHUB_TOKEN')

            # Define the headers for the profile request
            profile_headers = {
                'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}

            # Use the access token to fetch the user's GitHub profile information
            profile_response = requests.get(
                'https://api.github.com/user', headers=profile_headers)

            # Extract the user's name from the GitHub profile information
            username = profile_response.json().get('login')

            # If the username is already in the database, log the user in
            user = Users.query.filter_by(username=username).first()

            if user is None:
                # if the username is not in the database, create a new user
                email = profile_response.json().get('email')
                # generate a random password for the user
                password = secrets.token_urlsafe(16)
                hashed_password = bcrypt.generate_password_hash(
                    password)     # hash the password
                new_user = Users(username=username, password=hashed_password,  # create new user
                                 email=email)
                db.session.add(new_user)
                db.session.commit()
                user = new_user

            login_user(user)
            access_token = create_access_token(identity=username)
            return {'status': 'success', 'username': username, 'access_token': access_token}, 200

    return {'status': 'error', 'message': 'Invalid code'}, 401