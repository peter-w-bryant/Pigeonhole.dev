import os
import sys
import unittest

import requests
from dotenv import load_dotenv
from flask import Flask

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # set path to backend\api
from scripts import (
    add_project_to_db,
    add_projects_to_db_from_json,
    delete_all_projects_from_db,
    delete_project_from_db,
    read_all_project_data_json,
)


class AddProjectToDbTestCases(unittest.TestCase):

    def test_valid_github_url(self):
        app = create_app()
        with app.app_context():
            valid_url = 'https://github.com/pallets/flask/'
            delete_project_from_db(valid_url)       # ensure the project isn't already in the database
            response = add_project_to_db(valid_url, 1) # add the project to the database
            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['message'], 'Project added successfully.')
            self.assertEqual(type(response['project_dict']), dict)
            delete_project_from_db(valid_url)       # delete the project from the database
            
    def test_insert_duplicate_project(self):
        app = create_app()
        with app.app_context():
            valid_url = 'https://github.com/pallets/flask/'
            delete_project_from_db(valid_url)       # ensure the project isn't already in the database
            response = add_project_to_db(valid_url, 1) # add the project to the database
            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['message'], 'Project added successfully.')
            response = add_project_to_db(valid_url, 1) # add the project to the database
            self.assertEqual(response['status'], 'error')
            self.assertEqual(response['message'], 'Project already exists in the database.')
            delete_project_from_db(valid_url)       # delete the project from the database

    def test_invalid_github_url(self):
        app = create_app()
        with app.app_context():
            invalid_url = 'https://github.com/not_a_user/not_a_project/'
            delete_project_from_db(invalid_url)       # ensure the project isn't already in the database
            response = add_project_to_db(invalid_url, 1) # add the project to the database
            self.assertEqual(response['status'], 'error')
            self.assertEqual(response['message'], 'Invalid GitHub repository URL.')

# class AddProjectsToDbFromJsonTestCases(unittest.TestCase):

#     def test_valid_small_json(self):
#         app = create_app()
#         with app.app_context():
#             delete_all_projects_from_db() # ensure the database is empty
#             add_projects_to_db_from_json()

class ReadAllProjectDataJsonTestCases(unittest.TestCase):

    def test_valid_json(self):
        app = create_app()
        with app.app_context():
            response = read_all_project_data_json()
            self.assertEqual(type(response), dict)
            self.assertEqual('status' not in response.keys(), True) # check that the response is not an error

if __name__ == '__main__':
    unittest.main()