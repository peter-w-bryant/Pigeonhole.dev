from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user # for handling user sessions
from flask_bcrypt import Bcrypt # for hashing passwords
from flask_sqlalchemy import SQLAlchemy
import os
from config import config
from github import GitHubAPI
from db import DB

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

    config_class = os.getenv('FLASK_CONFIG')
    app.config.from_object(config[config_class])

    print(app.config['SQLALCHEMY_DATABASE_URI'])
    
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

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
