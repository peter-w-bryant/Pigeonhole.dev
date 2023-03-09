from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask import Blueprint, jsonify, current_app, render_template, redirect, url_for, request, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user # for handling user sessions
from flask_bcrypt import Bcrypt # for hashing passwords
from flask_sqlalchemy import SQLAlchemy # for database
from sqlalchemy.exc import IntegrityError # for handling duplicate entries
from utils import GitHubAPIWrapper, fetch_all_projects
from utils.db import db

projects = Blueprint('projects', __name__) # blueprint for auth routes

@projects.route('/add-project', methods=['GET', 'POST'])
def AddNewProject():
    """Add a new project to the database given a ?gh_url=GIT_HUB_REPO_URL"""
    if request.method == 'GET': # will be POST in production
        gh_url = request.args.get('gh_url')
        gh_url = "https://github.com/pallets/flask" # valid repo for testing
        gh = GitHubAPIWrapper(gh_url)
        is_valid = gh.verify_repo_url()
        if not is_valid:
            return {"error": "Invalid GitHub URL"}
        else:
            with DB() as db:
                insert_result = db.pop_project(gh)
            
            return insert_result
            
@projects.route('/all-projects', methods=['GET', 'POST'])
def AllProjectData():
    """Get all project data from the database"""
    if request.method == 'GET':
        return fetch_all_projects()