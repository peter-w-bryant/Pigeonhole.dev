import os

# Flask/SQLAlchemy imports
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
# for handling user sessions
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt  # for hashing passwords
from flask_sqlalchemy import SQLAlchemy

# Import SQLAlchemy instance
from utils.db import db
from utils.auth import bcrypt, login_manager

# Blueprints
from routes.projects import projects
from routes.auth import auth

from models import Users, Projects, SavedProjects

# Import config
from config import config

def create_app(config_class='development'):
    app = Flask(__name__)

    # if configuration class specified as param, init app with provided config
    if config_class != None:
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

    return app

@login_manager.user_loader
def load_user(UID):
    """Reloads the user object from the user ID stored in the session"""
    return Users.query.get(int(UID)) 

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
