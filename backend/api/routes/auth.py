# Path: backend\api\routes\auth.py
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask import Blueprint, jsonify, current_app, render_template, redirect, url_for, request, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user # for handling user sessions
from flask_sqlalchemy import SQLAlchemy # for database
from sqlalchemy.exc import IntegrityError # for handling duplicate entries
from utils import GitHubAPIWrapper, fetch_all_projects
from utils.db import db

auth = Blueprint('auth', __name__) # blueprint for auth routes

# Import bcrypt and login_manager
from utils.auth import bcrypt, login_manager
from models import Users

@auth.route('/register', methods=['GET', 'POST']) 
def register():
    print("registering user")
    if request.method == 'POST': 
        data = request.get_json()
        try:
            # check if username already exists
            user = Users.query.filter_by(username=data['username']).first()

            if user != None:
                return 'Username already exists!', 409 # return error message

            hashed_password = bcrypt.generate_password_hash(data['password']) # hash password
            
            new_user = Users(username=data['username'], password=hashed_password, # create new user
                            email=data['email'])
            
            db.session.add(new_user) # add new user to database
            db.session.commit()      # commit changes to database
            return 'User created successfully!', 201 # return success message
        
        except IntegrityError:
            return 'Username already exists!', 409   # return error message
        
        except Exception as e:
            print(e)
            return str(e), 500
       
@auth.route('/login', methods=['GET', 'POST'])
def login():
    Users.print_all_users()
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