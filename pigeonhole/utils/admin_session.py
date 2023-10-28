import os
import sys
from functools import wraps

from dotenv import load_dotenv
from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from utils.auth import bcrypt, login_manager
from utils.db import db


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
        self.headers = {'Authorization': 'Bearer ' + self.access_token}
        headers = {'Authorization': f'Bearer {self.access_token}', 'Content-Type': 'application/json'}

        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Logs out as admin
        """
        admin_user = {'username': self.username, 'password': self.password}
        self.client.post('/api/1/auth/logout', json=admin_user)

    def delete_all_test_accounts(self):
        """
        Deletes all accounts that are not admin accounts
        """
        query_params = {'filter': 'test_accounts'}
        response = self.client.post('/api/1/accounts/protected/delete_all_accounts', headers=self.headers, json=query_params)
        return response 
    
    def delete_all_non_admin_accounts(self):
        """
        Deletes all accounts that are not admin accounts
        """
        query_params = {'filter': 'all'}
        response = self.client.post('/api/1/accounts/protected/delete_all_accounts', headers=self.headers, json=query_params)
        return response  