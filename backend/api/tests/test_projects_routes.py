import os
import sys
import unittest
import requests
from flask import Flask
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # set path to backend\api
from app import create_app
from scripts import read_all_project_data_json, add_project_to_db, add_projects_to_db_from_json, delete_project_from_db, delete_all_projects_from_db

class ProjectsTestCase(unittest.TestCase):

    def test_all_projects(self):
        app = create_app()
        with app.test_client() as client:
            response = client.get('/api/1/projects/all-projects')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(type(response.json), dict)

            # Todo test query parameters: per_page, page, max_issues_per_project, max_topics_per_project

    def test_add_new_project(self):
        app = create_app()
        with app.app_context() as db_client:
            # ensure the project is not in the database
            valid_url = 'https://github.com/pallets/flask'
            response = delete_project_from_db(valid_url)
            invalid_url = 'bad_url'

            with app.test_client() as client:
                # Test valid project url
                response = client.post(f'/api/1/projects/add-project', json={'gh_url': valid_url})
                response_json = response.json
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response_json['status'], 'success')
                self.assertEqual(response_json['message'], 'Project added to database!')

                # Test project that is already in the database
                response = client.post(f'/api/1/projects/add-project', json={'gh_url': valid_url})
                response_json = response.json
                self.assertEqual(response.status_code, 409)
                self.assertEqual(response_json['status'], 'error')
                self.assertEqual(response_json['message'], 'Project already exists in database!')
                delete_project_from_db(valid_url)

                # Test invalid project url
                response = client.post(f'/api/1/projects/add-project', json={'gh_url': invalid_url})
                response_json = response.json
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response_json['status'], 'error')
                self.assertEqual(response_json['message'], 'Invalid GitHub URL!')

if __name__ == '__main__':
    unittest.main()