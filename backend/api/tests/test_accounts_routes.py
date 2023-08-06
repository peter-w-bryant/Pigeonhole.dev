import os
import sys
import unittest
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # set path to backend\api
from app import create_app
from utils.db import db
from utils.models import Users
from utils.admin_session import AdminSession

class RegisterAccountTestCase(unittest.TestCase):

    def test_register_valid_account(self):
        load_dotenv()

        # Delete all non-admin accounts
        with AdminSession() as admin_session:
            response = admin_session.delete_all_non_admin_accounts()
        self.assertEqual(response.status_code, 200)

        app = create_app()
        with app.test_client() as client:

            valid_account = {'username': 'p', 'password': 'p', 'email': 'peter.bryant@gatech.edu'}

            # Test register with valid credentials with no account already existing
            response = client.post('/api/1/accounts/register', json=valid_account)
            self.assertEqual(response.status_code, 200)
            self.assertIn('access_token', response.json)

            # Test register with valid credentials with account already existing
            response = client.post('/api/1/accounts/register', json=valid_account)
            self.assertEqual(response.status_code, 409)
            self.assertIn('error', response.json)
            self.assertEqual(response.json['error'], 'Username already exists!')

            # Login to the account and extract the access token
            response = client.post('/api/1/auth/login', json=valid_account)
            self.assertEqual(response.status_code, 200)
            self.assertIn('access_token', response.json)
            access_token = response.json['access_token']

            # Delete the account to return to original state
            headers = {'Authorization': f'Bearer {access_token}'}
            response = client.post('/api/1/accounts/delete_account', json=valid_account, headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn('message', response.json)
            self.assertEqual(response.json['message'], 'Account deleted!')

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
            self.assertEqual(response.json['error'], 'Invalid payload, username, password, and email required in request body.')

            # Test register with invalid admin secret (should create an account, but not an admin account)
            invalid_json = {'username': 'non_admin_user', 'password': 'p', 'email': 'email.com', 'admin_secret': 'very_wrong_secret'}
            response = client.post('/api/1/accounts/register', json=invalid_json)
            self.assertEqual(response.status_code, 200)
            self.assertIn('admin_status', response.json)
            self.assertEqual(response.json['admin_status'], False)

    def test_protected_admin_delete_all_accounts(self):
        app = create_app()
        with app.test_client() as client:
            # Add two accounts to delete
            valid_account = {'username': 'new_user001', 'password': 'password', 'email': 'new_email001.com'}
            valid_account2 = {'username': 'new_user002', 'password': 'password', 'email': 'new_email002.com'}
            response = client.post('/api/1/accounts/register', json=valid_account)
            self.assertEqual(response.status_code, 200)
            self.assertIn('access_token', response.json)
            response = client.post('/api/1/accounts/register', json=valid_account2)
            self.assertEqual(response.status_code, 200)
            self.assertIn('access_token', response.json)

            # Test delete all accounts with invalid admin credentials
            with AdminSession() as admin_session:
                response = admin_session.delete_all_non_admin_accounts()
            self.assertEqual(response.status_code, 200)

            # Check that there are no users in the database with is_admin = false
            accounts = Users.query.filter_by(is_admin=False).all()
            self.assertEqual(len(accounts), 0)

if __name__ == "__main__":
    unittest.main()