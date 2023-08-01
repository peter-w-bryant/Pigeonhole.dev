import os
import sys
import unittest
import requests
from flask import Flask
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # set path to backend\api
from app import create_app
from scripts import fetch_all_projects, add_project_to_db

class AddProjectToDbTestCases(unittest.TestCase):

    def test_valid_github_url(self):
        app = create_app()
        with app.app_context():
            valid_url = 'https://github.com/pallets/flask/'
            response = add_project_to_db(valid_url)
            print(response)
 
if __name__ == '__main__':
    unittest.main()