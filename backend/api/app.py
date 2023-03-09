import os

# Flask/SQLAlchemy imports
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user # for handling user sessions
from flask_bcrypt import Bcrypt # for hashing passwords
from flask_sqlalchemy import SQLAlchemy

# Import SQLAlchemy instance
from utils.db import db
from models import Users, Projects

# Blueprints
from routes.projects import projects

# Import config
from config import config

def create_app(config_class='development'):
    app = Flask(__name__)

    # if configuration class specified as param, init app with provided config
    if config_class != None:
        app.config.from_object(config[config_class]) # initialize environment variables from config

    # if configuration class not specified, init app from config from .env
    else:
        config_class = os.getenv('FLASK_CONFIG') # get configuration "development" or "production"
        app.config.from_object(config[config_class]) # initialize environment variables from config
    
    db.init_app(app)

    bcrypt = Bcrypt() # Bcrypt for hashing passwords
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    # Register blueprints
    with app.app_context():
        app.register_blueprint(projects)
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
