import unittest
from flask import Flask

import os
import sys

# set path to backend\api
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
        
    # def test_github_login(self):
    #     with self.app.test_client() as client:
    #         response = client.get('/github_login')
    #         self.assertEqual(response.status_code, 200)
    #         self.assertEqual(response.data.decode('utf-8'), 'Something went wrong!')

    #         # Test with valid code
    #         response = client.get('/github_login?code=validcode')
    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn('auth_token', response.json)
    #         self.assertIn('username', response.json)

if __name__ == '__main__':
    unittest.main()