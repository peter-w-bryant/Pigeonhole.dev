import os
import sys
import unittest
import requests
from flask import Flask
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # set path to backend\api
from app import create_app

key_list = ['date_last_commit', 'date_last_merged_PR', 'gh_contributing_url', 'gh_description', 'gh_rep_url',
            'gh_repo_name', 'gh_topics_0', 'gh_topics_1', 'gh_topics_2', 'gh_topics_3', 
            'gh_topics_4', 'gh_topics_5', 'gh_username', 'issue_label_1', 'issue_label_1_count',
            'issue_label_2', 'issue_label_2_count', 'issue_label_3', 'issue_label_3_count', 'issue_label_4', 
            'issue_label_4_count', 'issue_label_5', 'issue_label_5_count', 'issue_label_6', 'issue_label_6_count', 
            'issue_label_7', 'issue_label_7_count', 'new_contrib_score', 'num_forks', 'num_stars', 
            'num_watchers', 'pUID']

class ProjectsTestCase(unittest.TestCase):

    # def test_all_projects(self):
    #     app = create_app()
    #     with app.test_client() as client:
    #         response = client.get('/all-projects')
    #         response_json = response.json
    #         self.assertEqual(response.status_code, 200)
    #         for key in key_list:
    #             self.assertIn(key, response_json['Cardinal'].keys())

    def test_add_new_project(self):
        app = create_app()
        with app.test_client() as client:

            # Test invalid project url
            # invalid_url = 'bad_url'
            # response = client.get(f'/add-project?gh_url={invalid_url}')
            # response_json = response.json
            # self.assertEqual(response.status_code, 400)
            # self.assertIn('error', response_json.keys())
            # self.assertEqual(response_json['error'], 'Invalid GitHub URL')

            # Test project that is already in the database
            # valid_url = 'https://github.com/JuliaLang/julia'
            # response = client.get(f'/add-project?gh_url={valid_url}')
            # response_json = response.json
            # self.assertEqual(response.status_code, 409)
            # self.assertIn('error', response_json.keys())
            # self.assertEqual(response_json['error'], 'Project already exists in database')

            # Test valid project url, not in database
            valid_url = 'https://github.com/pallets/flask'
            response = client.get(f'/add-project?gh_url={valid_url}')
            response_json = response.json
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', response_json.keys())

if __name__ == '__main__':
    unittest.main()