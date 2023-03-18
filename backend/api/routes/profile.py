# Path: backend\api\routes\auth.py
from flask import Flask, render_template, session, request, redirect, jsonify, url_for, flash
from flask import Blueprint, jsonify, current_app, render_template, redirect, url_for, request, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy  # for database
from sqlalchemy.exc import IntegrityError  # for handling duplicate entries

from flask_dance.contrib.github import make_github_blueprint, github

from utils import GitHubAPIWrapper, fetch_all_projects
from utils.db import db
from utils.models import Users, SavedProjects, Projects
from utils.auth import bcrypt, login_manager

import requests
import os
import secrets

profile = Blueprint('profile', __name__)  # blueprint for auth routes

@profile.route('/save-project', methods = ['GET', 'POST'])
@login_required
def save_project():
    """Saves a project to the user's saved projects list"""
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        user = Users.query.filter_by(username=data['username']).first()
        UID = user.UID
        if user != None:
            project_exists = SavedProjects.query.filter_by(UID=UID, pUID=data['pUID']).first()
            if project_exists != None:
                return {"error": "Project already saved!"}, 403
            else:
                new_project = SavedProjects(UID=UID, pUID=data['pUID'])
                db.session.add(new_project)
                db.session.commit()
                return {"success": "Project added successfully!"}, 200
            
@profile.route('/saved-projects/<username>', methods = ['GET', 'POST'])
@login_required
def saved_projects(username):
    """Returns a list of saved projects for a user"""
    if request.method == 'GET':
        user = Users.query.filter_by(username=username).first()
        UID = user.UID
        if user != None:
            saved_project = SavedProjects.query.filter_by(UID=UID).all()
            # get the matching projects from the Projects table
            projects = Projects.query.filter(Projects.pUID.in_([project.pUID for project in saved_project])).all()
            projects_list = []
            for project in projects:
                project_dict = {
                    "pUID": project.pUID,
                    "gh_repo_name": project.gh_repo_name,
                    "gh_username": project.gh_username,
                    "gh_description": project.gh_description,
                    "gh_rep_url": project.gh_repo_url,
                    "gh_contributing_url": project.contrib_url,
                    "num_watchers": project.num_watchers,
                    "num_forks": project.num_forks,
                    "num_stars": project.num_stars,
                    "date_last_commit": project.date_last_commit,
                    "date_last_merged_PR": project.date_last_merged_PR,
                    "new_contrib_score": project.new_contrib_score,
                    "gh_topics_1": project.gh_topics1,
                    "gh_topics_2": project.gh_topics2,
                    "gh_topics_3": project.gh_topics3,
                    "gh_topics_4": project.gh_topics4,
                    "gh_topics_5": project.gh_topics5,
                    "issue_label_1": project.issue_label_1,
                    "issue_label_2": project.issue_label_2,
                    "issue_label_3": project.issue_label_3,
                    "issue_label_4": project.issue_label_4,
                    "issue_label_5": project.issue_label_5,
                    "issue_label_6": project.issue_label_6,
                    "issue_label_7": project.issue_label_7,
                }
                projects_list.append(project_dict)
            return {"projects": projects_list}, 200
        
@profile.route('/delete-all-projects', methods = ['GET', 'POST'])
@login_required
def delete_all_projects():
    """Deletes all projects for a user"""
    if request.method == 'POST':
        data = request.get_json()
        user = Users.query.filter_by(username=data['username']).first()
        UID = user.UID
        if user != None:
            projects = SavedProjects.query.filter_by(UID=UID).all()
            for project in projects:
                db.session.delete(project)
            db.session.commit()
            return {"success": "Projects deleted successfully!"}, 200