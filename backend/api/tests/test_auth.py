import os
import sys
import unittest
import requests
from flask import Flask
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # set path to backend\api
from app import create_app

class AuthTestCase(unittest.TestCase):

    def test_login(self):
        app = create_app()
        with app.test_client() as client:

            # Test with valid credentials
            response = client.post('/login', json={'username': 'p', 'password': 'p'})
            self.assertEqual(response.status_code, 200)
            self.assertIn('access_token', response.json)

            # Test with invalid credentials (wrong password)
            response = client.post('/login', json={'username': 'p', 'password': 'wrongpassword'})
            response_json = response.json
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response_json['error'], 'Invalid username or password')

            # Test with invalid credentials (wrong username)
            response = client.post('/login', json={'username': 'wrongusername', 'password': 'p'})
            response_json = response.json
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response_json['error'], 'Invalid username or password')

    def test_logout(self):
        app = create_app()
        with app.test_client() as client:

            # Test without logging in
            response = client.get('/logout')
            self.assertEqual(response.status_code, 401)

            # Login first, extract JWT token
            response = client.post('/login', json={'username': 'p', 'password': 'p'})
            access_token = response.json['access_token']
            self.assertEqual(response.status_code, 200)
            self.assertIn('access_token', response.json)

            # Log out user using JWT token
            headers = {'Authorization': f'Bearer {access_token}'}
            response = client.post('/logout', headers=headers)
            response_json = response.json
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response_json['message'], 'User logged out')

            # Test with invalid JWT token
            response = client.post('/login', json={'username': 'p', 'password': 'p'})
            self.assertEqual(response.status_code, 200)
            self.assertIn('access_token', response.json)
            headers = {'Authorization': f'Bearer invalidtoken'}
            response = client.post('/logout', headers=headers)
            self.assertEqual(response.status_code, 422) # 422 Unprocessable Entity

            # Test with no JWT token
            response = client.post('/login', json={'username': 'p', 'password': 'p'})
            response = client.post('/logout')
            response_json = response.json
            self.assertEqual(response.status_code, 401) # 401 Unauthorized
        
    def test_github_login(self):
        load_dotenv()
            
        # grab the client ID and secret from the environment
        client_id = os.environ.get('GITHUB_CLIENT_ID')
        client_secret = os.environ.get('GITHUB_CLIENT_SECRET')
        redirect_uri = 'http://127.0.0.1:3000/registration'

        # redirect to the authorization URL
        auth_url = f'https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=user'
        print(f'URL to authorize the app: {auth_url}')

        # obtain the temporary code from the redirect URL
        code = input('Enter code from the redirect URL: ')

        # exchange temporary code for access token
        token_url = 'https://github.com/login/oauth/access_token'
        token_params = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'redirect_uri': redirect_uri
        }

        token_headers = {'Accept': 'application/json'}
        token_response = requests.post(token_url, params=token_params, headers=token_headers)
        access_token = token_response.json().get('access_token')

        # fetch the user's profile the with access token
        profile_url = 'https://api.github.com/user'
        profile_headers = {'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}
        profile_response = requests.get(profile_url, headers=profile_headers)
        username = profile_response.json().get('login')
        self.assertEqual(username, 'peter-w-bryant')

        # test login with GitHub
        app = create_app()
        with app.test_client() as client:
            print("Testing route!")
            login_params = {'code': code}
            response = client.get('/github_login', json=login_params)
            print(response.json)
            self.assertEqual(response.status_code, 200)
            self.assertIn('access_token', response.json)

if __name__ == '__main__':
    unittest.main()