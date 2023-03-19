# Flask/SQLAlchemy imports
from flask import Flask, session, Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt  # for hashing passwords
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.github import make_github_blueprint, github  # for github oauth
from flask_sslify import SSLify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

from config import config # Import config

# Import routes
from routes.auth import auth
from routes.projects import projects
from routes.profile import profile
from routes.accounts import accounts

# Import SQLAlchemy instance
from utils.models import Users, Projects, SavedProjects
from utils.db import db
from utils.auth import bcrypt, login_manager

# Blueprints
github_blueprint = make_github_blueprint(client_id=os.getenv(
    'GITHUB_CLIENT_ID'), client_secret=os.getenv('GITHUB_CLIENT_SECRET'))

def create_app(config_class='development'):
    app = Flask(__name__)
    CORS(app)
    jwt = JWTManager(app)
    sslify = SSLify(app)

    # if configuration class specified as param, init app with provided config
    if config_class != None:
        print("config class: ", config_class)
        # initialize environment variables from config
        app.config.from_object(config[config_class])

    # if configuration class not specified, init app from config from .env
    else:
        # get configuration "development" or "production"
        config_class = os.getenv('FLASK_CONFIG')
        # initialize environment variables from config
        app.config.from_object(config[config_class])

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # Register blueprints
    with app.app_context():
        app.register_blueprint(projects)
        app.register_blueprint(auth)
        app.register_blueprint(profile)
        app.register_blueprint(accounts)
    return app


@login_manager.user_loader
def load_user(UID):
    """Reloads the user object from the user ID stored in the session"""
    return Users.query.get(int(UID))


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
