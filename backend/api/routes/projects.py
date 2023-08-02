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
        gh_url = request.args.get('gh_url')
        gh = GitHubAPIWrapper(gh_url)

        if gh.is_valid:
            project = Projects.query.filter_by(gh_repo_url=gh.repo_url).first()    
            if project is not None:
                return {"error": "Project already exists in database"}, 409
            print("f1")
            is_valid, inserted = add_project_to_db(gh.repo_url)
        else:
            return {"error": "Invalid GitHub URL"}, 400
        
        if inserted == False:
            return {"error": "Unable to add project to the database"}, 409
        else:
            return {"message": "Project added to the database"}, 200
            
@projects.route('/all-projects', methods=['GET'])
def AllProjectData():
    """Get all project data from the database
    :return: JSON object with all project data
    """
    if request.method == 'GET':
        return read_all_project_data_json(), 200