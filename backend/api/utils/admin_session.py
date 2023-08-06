from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from utils.models import Users, AdminSecretKeys
from utils.auth import bcrypt, login_manager
import sys
import os
from dotenv import load_dotenv

from app import create_app
from utils.db import db
from utils.models import Users
        

class AdminSession():
    """
    Signs in as admin and returns an access token
    """
    def __init__(self):
        load_dotenv()
        self.username = os.getenv('ADMIN_USERNAME')
        self.password = os.getenv('ADMIN_PASSWORD')
        self.access_token = None

        app = create_app()
        with app.test_client() as client:
            self.client = client

    def __enter__(self):
        """
        Logs in as admin and returns an access token
        """
        load_dotenv()
        admin_user = {'username': self.username, 'password': self.password}
        response = self.client.post('/api/1/auth/login', json=admin_user)
        self.access_token = response.json['access_token']
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Logs out as admin
        """
        admin_user = {'username': self.username, 'password': self.password}
        self.client.post('/api/1/auth/logout', json=admin_user)

    def delete_all_non_admin_accounts(self):
        """
        Deletes all accounts that are not admin accounts
        """
        header = {'Authorization': 'Bearer ' + self.access_token}
        response = self.client.post('/api/1/accounts/protected/delete_all_accounts', headers=header)
        return response