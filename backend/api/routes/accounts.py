# Path: backend\api\routes\auth.py
from flask import Flask, render_template, session, request, redirect, jsonify, url_for, flash
from flask import Blueprint, jsonify, current_app, render_template, redirect, url_for, request, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy  # for database
from sqlalchemy.exc import IntegrityError  # for handling duplicate entries
from flask_jwt_extended import create_access_token

from flask_dance.contrib.github import make_github_blueprint, github

from utils import GitHubAPIWrapper, fetch_all_projects
from utils.db import db
from utils.models import Users, SavedProjects, Projects
from utils.auth import bcrypt, login_manager

import requests
import os
import secrets

accounts = Blueprint('accounts', __name__)  # blueprint for auth routes


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
        
    