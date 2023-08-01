# Path: backend\api\routes\auth.py
from flask import Flask, render_template, session, request, redirect, jsonify, url_for, flash
from flask import Blueprint, jsonify, current_app, render_template, redirect, url_for, request, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_jwt_extended import create_access_token

from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.exc import IntegrityError  

from scripts import GitHubAPIWrapper, fetch_all_projects
from utils.db import db
from utils.models import Users, SavedProjects, Projects
from utils.auth import bcrypt, login_manager

import requests
import os
import secrets

accounts = Blueprint('accounts', __name__)  # blueprint for auth routes

@accounts.route('/register', methods=['POST'])
def register():
    """Registers a new user"""
    if request.method == 'POST':
        data = request.get_json()
        try:
            # check if username already exists
            user = Users.query.filter_by(username=data['username']).first()
            if user != None:
                return 'Username already exists!', 409 
            
            hashed_password = bcrypt.generate_password_hash(data['password'])  # hash password
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

@accounts.route('/delete_all_accounts', methods=['GET', 'POST'])
def delete_all_accounts():
    """Deletes all accounts"""
    if request.method == 'GET':
        try:
            db.session.query(Users).delete()
            db.session.commit()
            return 'All accounts deleted successfully!', 200
        except Exception as e:
            print(e)
            return str(e), 500
        
    return 'Invalid request method!', 405
    