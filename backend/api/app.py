import os
from datetime import timedelta

from flask import Flask
from flask_sslify import SSLify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flasgger import Swagger

from routes.auth import auth
from routes.projects import projects
from routes.profile import profile
from routes.accounts import accounts

from utils.models import Users, Projects, SavedProjects
from utils.db import db
from utils.auth import bcrypt, login_manager

from config import config 

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Pigeonhole.dev API",
        "description": "An enriched GitHub API offering Open Source Project Discovery for new developers.",
        "contact": {
            "responsibleDeveloper": "Peter Bryant",
            "email": "peter.bryant@gatech.edu",
        },
        "termsOfService": "",
        "version": "0.0.1"
    },
    "host": "localhost:5000",  
    "basePath": "/", 
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "\
            JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
}

def create_app(config_class='development'):
    """Factory function to create app instance
    :param config_class: Configuration class to use (defined in config.py)
    :return: Flask app instance
    """
    app = Flask(__name__)
    CORS(app)             # Initialize CORS for all routes
    jwt = JWTManager(app) # Initialize JWT for access tokens 
    sslify = SSLify(app)  # Initialize SSLify for HTTPS
    swagger = Swagger(app, template=swagger_template) # Initialize Swagger for API documentation

    app.config.from_object(config[config_class]) # load config from config.py
    db.init_app(app)                             # initialize database
    login_manager.init_app(app)                  # initialize login manager for flask-login

    @login_manager.user_loader
    @jwt_required()
    def load_user(UID):
        """Reloads the user object from the user ID stored in the JWT token.
        :param UID: User ID
        :return: User object or None
        """
        current_user_id = get_jwt_identity()
        if current_user_id and current_user_id == int(UID):
            user = Users.query.filter_by(UID=UID).first()
            return user
        return None
    
    with app.app_context():
        app.register_blueprint(projects, url_prefix='/api/1')
        app.register_blueprint(auth, url_prefix='/api/1')
        app.register_blueprint(profile, url_prefix='/api/1')
        app.register_blueprint(accounts, url_prefix='/api/1')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True,host='0.0.0.0')