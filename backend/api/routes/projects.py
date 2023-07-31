from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask import Blueprint, jsonify, current_app, render_template, redirect, url_for, request, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user # for handling user sessions
from flask_bcrypt import Bcrypt 
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.exc import IntegrityError 
from utils import GitHubAPIWrapper, fetch_all_projects
from utils.db import db
from utils.models import Users, SavedProjects, Projects
from scripts.database import pop_project

projects = Blueprint('projects', __name__) # blueprint for auth routes

@projects.route('/add-project', methods=['GET', 'POST'])
def AddNewProject():
    """Add a new project to the database given a GH repo URL
    :return: JSON object with the result of the insert
    """
    if request.method == 'GET': # will be POST in production
        gh_url = request.args.get('gh_url')
        if not gh_url.startswith("https://github.com"):
             return {"error": "Invalid GitHub URL"}, 400

        gh = GitHubAPIWrapper(gh_url)
        project = Projects.query.filter_by(gh_repo_url=gh_url).first()
    
        print("Project: ", project)
        if project is not None:
            return {"error": "Project already exists in database"}, 409
        
        elif gh.verify_repo_url() == False:
            return {"error": "Invalid GitHub URL"}, 400
    
        is_valid, inserted = db.pop_project(gh)
        
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
        return fetch_all_projects(), 200