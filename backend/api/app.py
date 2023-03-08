import os
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user # for handling user sessions
from flask_bcrypt import Bcrypt # for hashing passwords
from flask_sqlalchemy import SQLAlchemy

# Custom Imports
from config import config
from github import GitHubAPI

def create_app(config_class=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

    # if configuration class specified as param, init app with provided config
    if config_class != None:
        app.config.from_object(config[config_class]) # initialize environment variables from config

    # if configuration class not specified, init app from config from .env
    else:
        config_class = os.getenv('FLASK_CONFIG') # get configuration "development" or "production"
        app.config.from_object(config[config_class]) # initialize environment variables from config

    # Initialize db object with app config
    from db import db
    db.init_app(app)

    bcrypt = Bcrypt() # Bcrypt for hashing passwords
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    # Routes
    from routes.projects import projects

    with app.app_context():
        # Register blueprints
        app.register_blueprint(projects)

    # Create database tables for our data models
    from models import Users, Projects

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
