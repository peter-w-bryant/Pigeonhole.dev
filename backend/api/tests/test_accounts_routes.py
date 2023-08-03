import os
import sys
import unittest
import requests
from flask import Flask
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # set path to backend\api
from app import create_app

class RegisterAccountTestCase(unittest.TestCase):

    def test_register_valid_account(self):
        app = create_app()
        with app.test_client() as client:
            valid_account = {'username': 'p', 'password': 'p', 'email': 'peter.bryant@gatech.edu'}
            response = client.post('/api/1/accounts/delete_account', json=valid_account) # ensure the account does not already exist

            # Test register with valid credentials with no account already existing
            response = client.post('/api/1/accounts/register', json=valid_account)
            self.assertEqual(response.status_code, 200)
            self.assertIn('access_token', response.json)

            # Test register with valid credentials with account already existing
            response = client.post('/api/1/accounts/register', json=valid_account)
            self.assertEqual(response.status_code, 409)
            self.assertIn('error', response.json)
            self.assertEqual(response.json['error'], 'Username already exists!')

    def test_register_invalid_account(self):
        app = create_app()
        with app.test_client() as client:

            # Test register with no username
            invalid_account = {'username': '', 'password': 'p', 'email': 'bad_email'}
            response = client.post('/api/1/accounts/register', json=invalid_account)
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response.json)
            self.assertEqual(response.json['error'], 'Username, password, and email cannot be empty!')

            # Test register with no password
            invalid_account = {'username': 'p', 'password': '', 'email': 'bad_email'}
            response = client.post('/api/1/accounts/register', json=invalid_account)
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response.json)
            self.assertEqual(response.json['error'], 'Username, password, and email cannot be empty!')

            # Test register with no email
            invalid_account = {'username': 'p', 'password': 'p', 'email': ''}
            response = client.post('/api/1/accounts/register', json=invalid_account)
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response.json)
            self.assertEqual(response.json['error'], 'Username, password, and email cannot be empty!')

            # Test register with invalid request body
            invalid_json = {'wrong_key': 'p', 'password': 'p', 'email': 'bad_email'} # wrong_key instead of username
            response = client.post('/api/1/accounts/register', json=invalid_json)
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response.json)
            self.assertEqual(response.json['error'], 'Invalid payload, username, password, and email required i request body.')

if __name__ == "__main__":
    unittest.main()