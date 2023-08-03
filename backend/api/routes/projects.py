from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, Blueprint, current_app
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user # for handling user sessions
from flask_bcrypt import Bcrypt 
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.exc import IntegrityError 

from scripts import GitHubAPIWrapper, read_all_project_data_json, add_project_to_db
from utils.db import db
from utils.models import Users, SavedProjects, Projects

projects = Blueprint('projects', __name__) # blueprint for auth routes

@projects.route('/add-project', methods=['GET', 'POST'])
def AddNewProject():
    """Add a new project to the database given a GH repo URL
    :return: JSON object with the result of the insert
    """
    if request.method == 'GET': # will be POST in production
        gh_url = request.get_json()['gh_url']
        gh = GitHubAPIWrapper(gh_url)
        if not gh.is_valid:
            return jsonify({'status': 'error', 'message': 'Invalid GitHub URL!'}), 400
        
        project = Projects.query.filter_by(gh_repo_url=gh.repo_url).first()    
        if project is not None:
            return jsonify({'status': 'error', 'message': 'Project already exists in database!'}), 409
        
        response = add_project_to_db(gh.repo_url)
        if response['status'] == 'success':
            return jsonify({'status': 'success', 'message': 'Project added to database!'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Error adding project to database!'}), 500

@projects.route('/all-projects', methods=['GET'])
def AllProjectData():
    """
    Returns all project data in the database as a JSON object or an error message if there was an error retrieving the data
    ---
    parameters:
      - name: per_page
        in: query
        type: integer
        required: false
        default: 10
        description: Number of results to return per page (max 100)
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: Page number to return
    responses:
      200:
        description: Project data returned successfully
      500:
        description: Error retrieving project data
    """
    if request.method == 'GET':
        per_page = request.args.get('per_page', default=10, type=int)
        page = request.args.get('page', default=1, type=int)

        # ensure per_page is between 1 and 100
        if per_page > 100:
            per_page = 100
        elif per_page < 1:
            per_page = 10

        # ensure page is greater than 0
        if page < 1:
            page = 1

        response_dict = read_all_project_data_json(per_page, page)
        if 'status' in response_dict:
            return response_dict, 500
    
        return response_dict, 200