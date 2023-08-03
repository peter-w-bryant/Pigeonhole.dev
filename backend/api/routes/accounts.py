# Path: backend\api\routes\auth.py
from flask import Flask, render_template, session, request, redirect, jsonify, url_for, flash
from flask import Blueprint, jsonify, current_app, render_template, redirect, url_for, request, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.exc import IntegrityError  

from scripts import GitHubAPIWrapper, read_all_project_data_json
from utils.db import db
from utils.models import Users, SavedProjects, Projects
from utils.auth import bcrypt, login_manager

import requests
import os
import secrets

accounts = Blueprint('accounts', __name__)  # blueprint for auth routes

@accounts.route('/accounts/register', methods=['POST'])
def register():
    """
    Registers a new user to the database and returns an access token.
    ---
    tags:
    - Accounts
    parameters:
    - name: User JSON object
      in: body
      required: true
      description: Registers a new user to the database and returns an access token.
      schema:
        type: object
        properties:
          username:
            type: string
            description: The username of the new user.
            example: testuser
          password:
            type: string
            description: The password of the new user.
            example: testpassword
          email:
            type: string
            description: The email address of the new user.
            example: test@email.com
    responses:
      200:
          description: User registered successfully, returns access token
      400:
          description: Invalid payload, username, password, and email required in request body
      409:
          description: Username already exists
      500:
          description: Internal server error
    """

    if request.method == 'POST':
        data = request.get_json()
        if not all(key in data.keys() for key in ['username', 'password', 'email']):
             return {'error': 'Invalid payload, username, password, and email required i request body.'}, 400
        try:
            # ensure username and password are not empty
            if data['username'] == '' or data['username'] == None or data['password'] == '' or data['password'] == None or data['email'] == '' or data['email'] == None:
                return {'error': 'Username, password, and email cannot be empty!'}, 400

            # check if username already exists
            user = Users.query.filter_by(username=data['username']).first()

            if user != None:
                return {'error': 'Username already exists!'}, 409
            
            hashed_password = bcrypt.generate_password_hash(data['password']) # hash password
            new_user = Users(username=data['username'], password=hashed_password, # create new user
                             email=data['email'])
            
            db.session.add(new_user)  # add new user to database
            db.session.commit()       # commit changes to database
            access_token = create_access_token(identity=new_user.UID)
            return jsonify({'access_token': access_token}), 200

        except IntegrityError as ie:
            # print(ie)
            return {'error': 'IntegrityError: Username already exists!'}, 409

        except Exception as e:
            # print(e)
            return {'error': f"Exception {e}"}, 500
        
@accounts.route('/accounts/delete_account', methods=['POST'])
def delete_account():
    """
    Deletes a user account from the database.
    ---
    tags:
    - Accounts
    parameters:
    - name: User JSON object
      in: body
      required: true
      description: Deletes a user account from the database.
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
          description: User deleted successfully
      400:
          description: Invalid payload, username and password required in request body
      401:
            description: Incorrect password
      404:
          description: Username does not exist
      500:
          description: Internal server error
    """
    if request.method == 'POST':
        data = request.get_json()
        try:
            # ensure username and password are not empty
            if data['username'] == '' or data['username'] == None or data['password'] == '' or data['password'] == None:
                return {'error': 'Username or password cannot be empty!'}, 400

            # check if username already exists
            user = Users.query.filter_by(username=data['username']).first()
            if user == None:
                return {'error': 'Username does not exist!'}, 404
            
            if user.check_password(data['password']):
                db.session.delete(user)
                db.session.commit()
                return {'message': 'Account deleted!'}, 200
            else:
                return {'error': 'Incorrect password!'}, 401

        except Exception as e:
            print(e)
            return {'error': str(e)}, 500

@accounts.route('/accounts/delete_all_accounts', methods=['GET'])
def delete_all_accounts():
    """
    Protected route to delete all user accounts for testing purposes (requires admin access)
    ---
    tags:
    - Accounts
    parameters:
    - name: Admin JSON object
      in: body
      required: true
      description: Deletes all user accounts from the database.
      schema:
        type: object
        properties:
          username:
            type: string
            description: The username of the administator.
            example: admin
          password:
            type: string
            description: The password of the administrator.
            example: admin
          secret:
            type: string
            description: The secret key of the administrator.
            example: secret
    responses:
      200:
          description: User deleted successfully
      400:
          description: Invalid payload, username and password required in request body
      401:
            description: Incorrect password
      404:
          description: Username does not exist
      500:
          description: Internal server error
    """
    if request.method == 'GET':
        try:
            db.session.query(Users).delete()
            db.session.commit()
            return {'message': 'All accounts deleted!'}, 200
        except Exception as e:
            print(e)
            return {'error': str(e)}, 500
        
    return {'error': 'Invalid request method!'}, 405
    