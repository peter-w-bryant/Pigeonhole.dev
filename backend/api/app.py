# Flask/SQLAlchemy imports
from flask import Flask, session, Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt  # for hashing passwords
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.github import make_github_blueprint, github  # for github oauth
from flask_sslify import SSLify
from flask_oauthlib.client import OAuth # for github oauth
import os

from config import config # Import config

# Import routes
from routes.auth import auth
from routes.projects import projects
from routes.profile import profile

# Import SQLAlchemy instance
from utils.models import Users, Projects, SavedProjects
from utils.db import db
from utils.auth import bcrypt, login_manager

# Blueprints
github_blueprint = make_github_blueprint(client_id=os.getenv(
    'GITHUB_CLIENT_ID'), client_secret=os.getenv('GITHUB_CLIENT_SECRET'))

def create_app(config_class='development'):
    app = Flask(__name__)
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

    oauth = OAuth(app)
    github = oauth.remote_app(
        'github',
        consumer_key=app.config['GITHUB_CLIENT_ID'],
        consumer_secret=app.config['GITHUB_CLIENT_SECRET'],
        request_token_params={'scope': 'user:email'},
        base_url='https://api.github.com/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='https://github.com/login/oauth/access_token',
        authorize_url='https://github.com/login/oauth/authorize'
    )

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # Register blueprints
    with app.app_context():
        app.register_blueprint(projects)
        app.register_blueprint(auth)
        app.register_blueprint(profile)
        app.register_blueprint(github_blueprint, url_prefix="/github_login")
    return app


@login_manager.user_loader
def load_user(UID):
    """Reloads the user object from the user ID stored in the session"""
    return Users.query.get(int(UID))


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
