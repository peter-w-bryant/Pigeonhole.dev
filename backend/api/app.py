import os
from datetime import timedelta

from flask import Flask
from flask_sslify import SSLify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_identity

from routes.auth import auth
from routes.projects import projects
from routes.profile import profile
from routes.accounts import accounts

from utils.models import Users, Projects, SavedProjects
from utils.db import db
from utils.auth import bcrypt, login_manager

from config import config 

def create_app(config_class='development'):
    """Factory function to create app instance
    :param config_class: Configuration class to use (defined in config.py)
    :return: Flask app instance
    """
    app = Flask(__name__)
    CORS(app)             # Initialize CORS for all routes
    jwt = JWTManager(app) # Initialize JWT for access tokens 
    sslify = SSLify(app)  # Initialize SSLify for HTTPS

    # if configuration class specified as param, init app with provided config
    if config_class != None:
        app.config.from_object(config[config_class]) # initialize environment variables from config class
    # if configuration class not specified, init app from config from .env
    else:
        config_class = os.getenv('FLASK_CONFIG')     # get config class from environment variable
        app.config.from_object(config[config_class]) # initialize environment variables from config

    # Initialize extensions
    db.init_app(app)                                                 # initialize database
    login_manager.init_app(app)                                      # initialize login manager for flask-login
    # app.config['SESSION_COOKIE_SECURE'] = True                       # set session cookie to secure
    # app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30) # set session lifetime to 30 minutes
    
    # Register blueprints
    with app.app_context():
        app.register_blueprint(projects)
        app.register_blueprint(auth)
        app.register_blueprint(profile)
        app.register_blueprint(accounts)
    return app

@login_manager.user_loader
def load_user(UID):
    """Reloads the user object from the user ID stored in the JWT token.
    :param UID: User ID
    :return: User object or None
    """
    current_user_id = get_jwt_identity()
    if current_user_id and current_user_id == int(UID):
        # Here you can load the user object using the current_user_id
        # For example, if you have a User model with a get_by_id method:
        user = Users.get_by_id(current_user_id)
        return user
    return None

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True,host='0.0.0.0')
