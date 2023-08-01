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
        self.assertEqual(len(gh.gh_topics) > 0, True)
        self.assertEqual(type(gh.gh_topics), list)
        self.assertEqual(gh.gh_topics, ['flask', 'jinja', 'pallets', 'python', 'web-framework', 'werkzeug', 'wsgi'])

        # Test the issues attribute
        self.assertEqual(len(gh.gh_issues), 0)
        self.assertEqual(type(gh.gh_issues), list)
        self.assertEqual(gh.gh_issues, [])

        # Test repo counts
        self.assertEqual(gh.gh_stargazers_count > 0, True)
        self.assertEqual(gh.gh_forks_count > 0, True)
        self.assertEqual(gh.gh_watchers_count > 0, True)

        self.assertEqual(gh.gh_contributing_url, "") # Test CONTRIBUTING.md
        self.assertEqual(gh.gh_new_contributor_score > 0, True) # Test new contributor score

    def test_valid_github_url_with_issues(self):
        valid_url = 'https://github.com/tensorflow/tensorflow'
        gh = GitHubAPIWrapper(valid_url)
        self.assertEqual(gh.is_valid, True)
        self.assertEqual(gh.username, 'tensorflow')
        self.assertEqual(gh.repo_name, 'tensorflow')
        self.assertEqual(gh.base_url, 'https://api.github.com/repos/tensorflow/tensorflow')
        self.assertEqual(gh.search_url, 'https://api.github.com/search/issues?q=repo:tensorflow/tensorflow')
        self.assertEqual(gh.status_code, 200)

        # Test the topics attribute
        self.assertEqual(len(gh.gh_topics) > 0, True)
        self.assertEqual(type(gh.gh_topics), list)
        self.assertEqual(gh.gh_topics, ['deep-learning', 'deep-neural-networks', 'distributed', 'machine-learning', 'ml', 'neural-network', 'python', 'tensorflow'])

        # Test the issues attribute
        self.assertEqual(len(gh.gh_issues) > 0, True)
        self.assertEqual(type(gh.gh_issues), list)

        # Test repo counts
        self.assertEqual(gh.gh_stargazers_count > 0, True)
        self.assertEqual(gh.gh_forks_count > 0, True)
        self.assertEqual(gh.gh_watchers_count > 0, True)

        self.assertEqual(gh.gh_contributing_url == "https://github.com/tensorflow/tensorflow/blob/master/CONTRIBUTING.md", True) # Test CONTRIBUTING.md
        self.assertEqual(gh.gh_new_contributor_score > 0, True) # Test new contributor score

if __name__ == '__main__':
    unittest.main()