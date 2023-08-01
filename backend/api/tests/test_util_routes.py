import os
import sys
import unittest
import requests
from flask import Flask
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # set path to backend\api
from utils import GitHubAPIWrapper

class GitHubAPIWrapperTestCase(unittest.TestCase):

    def test_valid_github_url(self):
        valid_url = 'https://github.com/pallets/flask'
        gh = GitHubAPIWrapper(valid_url)
        self.assertEqual(gh.is_valid, True)
        self.assertEqual(gh.username, 'pallets')
        self.assertEqual(gh.repo_name, 'flask')
        self.assertEqual(gh.base_url, 'https://api.github.com/repos/pallets/flask')
        self.assertEqual(gh.search_url, 'https://api.github.com/search/issues?q=repo:pallets/flask')
        self.assertEqual(gh.status_code, 200)

        # Test the topics attribute
        self.assertEqual(len(gh.gh_topics), 7)
        self.assertEqual(type(gh.gh_topics), list)
        self.assertEqual(gh.gh_topics, ['flask', 'jinja', 'pallets', 'python', 'web-framework', 'werkzeug', 'wsgi'])

if __name__ == '__main__':
    unittest.main()