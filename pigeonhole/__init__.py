from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from flask_sslify import SSLify

from pigeonhole.config import config
from pigeonhole.routes.backend.projects import projects
from pigeonhole.routes.frontend.index import index
from pigeonhole.utils.auth import bcrypt, login_manager

# from routes.backend.auth import auth
# from routes.backend.profile import profile
# from routes.backend.accounts import accounts



swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Pigeonhole.dev API",
        "description": "An enriched, Dockerized GitHub API proxy for open-source project discovery. Built with Flask and Azure Postgres Database & deployed with Azure Container Instances. Load tested with k6.",
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

# swagger_doc = Swagger.load_file('swagger.yml')

def create_app(config_class='development'):
    """Factory function to create app instance
    :param config_class: Configuration class to use (defined in config.py)
    :return: Flask app instance
    """
    app = Flask(__name__)
    CORS(app)             # Initialize CORS for all routes
    jwt = JWTManager(app) # Initialize JWT for access tokens 
    sslify = SSLify(app)  # Initialize SSLify for HTTPS
    swagger = Swagger(app, template="swagger.yml") # Initialize Swagger for API documentation

    app.config.from_object(config[config_class]) # load config from config.py
    login_manager.init_app(app)                  # initialize login manager for flask-login

    @login_manager.user_loader
    @jwt_required()
    def load_user(UID):
        """Reloads the user object from the user ID stored in the JWT token.
        :param UID: User ID
        :return: User object or None
        """
        # current_user_id = get_jwt_identity()
        # if current_user_id and current_user_id == int(UID):
        #     user = Users.query.filter_by(UID=UID).first()
        #     return user
        return None
    
    with app.app_context():
        app.register_blueprint(index, url_prefix='/')
        app.register_blueprint(projects, url_prefix='/api')
        # app.register_blueprint(auth, url_prefix='/api')
        # app.register_blueprint(profile, url_prefix='/api')
        # app.register_blueprint(accounts, url_prefix='/api')
    return app