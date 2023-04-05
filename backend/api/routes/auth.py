# Path: backend\api\routes\auth.py

# Python imports
import requests
import os
import secrets

# Flask/SQLAlchemy imports
from flask import session, request, Blueprint, current_app, request, redirect, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError          # for handling duplicate entries
from flask_jwt_extended import create_access_token # for creating access tokens


# Utils imports
from utils import GitHubAPIWrapper, fetch_all_projects
from utils.db import db
from utils.models import Users, SavedProjects, Projects
from utils.auth import bcrypt, login_manager

auth = Blueprint('auth', __name__)  # blueprint for auth routes

def authenticate_user(username, password):
    user = Users.query.filter_by(username=username).first()
    if user is None:
        return None
    elif not bcrypt.check_password_hash(user.password, password):
        return None
    else:
        return user

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
    print("login() called")
    # Check if the user is already logged in
    if request.method == 'POST':
        data = request.get_json()
        user = authenticate_user(data['username'], data['password'])
        if user is not None:
            login_user(user)
            assert current_user.is_authenticated
            return 'Logged in successfully!', 200
        else:
            return 'Incorrect username or password!', 401
    # If GET request, return the login page
    else:
        # Handle GET request
        # check if user is already logged in
        print("current_user:")
        print(current_user)
        if current_user.is_authenticated:
            next_url = request.args.get('next')
            return redirect(next_url), 200


@auth.route('/github_login', methods=['GET', 'POST'])
def github_login():
    """Logs in a user using GitHub OAuth.
    If the user is not in the database, create a new user with the GitHub username, a random password, and the GitHub email.
    If the user is in the database, log the user in.
    :return: The username and access token or an error message
    """
    print("github_login() called")
    if request.method == 'GET':        
        req_args = request.args # Get the request arguments
        if 'code' in req_args:
            # Log the user out of Flask-Login
            logout_user()
            
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
            
            token_response.raise_for_status()                        # Check for errors in the response
            access_token = token_response.json().get('access_token') # Extract the access token from the response
            bearer_token = "Bearer " + access_token                  # Create a Bearer token from the access token

            # Use the access token to fetch the user's GitHub profile information
            profile_response = requests.get('https://api.github.com/user', headers={
                                            'Authorization': bearer_token, 'Accept': 'application/json'})
            assert profile_response.status_code == 200
            
            username = profile_response.json().get('login')     # Extract the username from the profile
            auth_token = create_access_token(identity=username) # Create a JSON Web Token (JWT) for the user

            session['jwt_token'] = auth_token  # Save the JWT to the user's session

            # If the username is already in the database, log the user in
            user = Users.query.filter_by(username=username).first()

            if user != None:
                # make request to login route with the username and password
                requests.post('http://localhost:5000/api/login', json={'username': username, 'password': user.password})
                return {'username': username, 'auth_token': auth_token}, 200
            else:
                # If the username is not in the database, create a new user
                email = profile_response.json().get('email')

                # Generate a random password for the user
                password = secrets.token_urlsafe(10)

                # Hash the password
                hashed_password = bcrypt.generate_password_hash(password)

                new_user = Users(username=username, password=hashed_password,  # create new user
                                    email=email)

                db.session.add(new_user)  # add new user to database

                db.session.commit()       # commit changes to database

                login_user(new_user)      # log the user in

                assert current_user.is_authenticated

            return {'username': username, 'auth_token': auth_token}, 200

    return 'Something went wrong!', 200



@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        logout_user()
        return 'Logged out successfully!', 200
    else:
        return 'You are already logged out.', 200