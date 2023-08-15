import os
import sys
import unittest
import requests
from flask import Flask
from dotenv import load_dotenv

from datetime import datetime as dt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # set path to backend\api
from app import create_app
from scripts import GitHubAPIWrapper, read_all_project_data_json, add_project_to_db, add_projects_to_db_from_json, delete_project_from_db, delete_all_projects_from_db
from utils.models import Projects, ProjectIssues, ProjectTopics

# class GitHubAPIWrapperTestCases(unittest.TestCase):

#     def test_valid_github_url(self):
#         valid_url = 'https://github.com/pallets/flask'
#         gh = GitHubAPIWrapper(valid_url)
#         self.assertEqual(gh.is_valid, True)
#         self.assertEqual(gh.username, 'pallets')
#         self.assertEqual(gh.repo_name, 'flask')
#         self.assertEqual(gh.base_url, 'https://api.github.com/repos/pallets/flask')
#         self.assertEqual(gh.search_url, 'https://api.github.com/search/issues?q=repo:pallets/flask')
#         self.assertEqual(gh.status_code, 200)

#         # Test the topics attribute
#         self.assertEqual(len(gh.gh_topics) > 0, True) 
#         self.assertEqual(type(gh.gh_topics), list)

#         # Test the issues attribute
#         self.assertEqual(type(gh.gh_issues_dict), dict)

#         # Test repo counts
#         self.assertEqual(gh.gh_stargazers_count > 0, True)
#         self.assertEqual(gh.gh_forks_count > 0, True)
#         self.assertEqual(gh.gh_watchers_count > 0, True)

#         self.assertEqual(gh.gh_contributing_url, "") # Test CONTRIBUTING.md
#         self.assertEqual(gh.gh_new_contributor_score > 0, True) # Test new contributor score

#     def test_valid_github_url_with_issues(self):
#         valid_url = 'https://github.com/tensorflow/tensorflow'
#         gh = GitHubAPIWrapper(valid_url)
#         self.assertEqual(gh.is_valid, True)
#         self.assertEqual(gh.username, 'tensorflow')
#         self.assertEqual(gh.repo_name, 'tensorflow')
#         self.assertEqual(gh.base_url, 'https://api.github.com/repos/tensorflow/tensorflow')
#         self.assertEqual(gh.search_url, 'https://api.github.com/search/issues?q=repo:tensorflow/tensorflow')
#         self.assertEqual(gh.status_code, 200)

#         # Test the topics attribute
#         self.assertEqual(type(gh.gh_topics), list)

#         # Test the issues attribute
#         self.assertEqual(type(gh.gh_issues_dict), dict)

#         # Test repo counts
#         self.assertEqual(gh.gh_stargazers_count > 0, True)
#         self.assertEqual(gh.gh_forks_count > 0, True)
#         self.assertEqual(gh.gh_watchers_count > 0, True)

#         self.assertEqual(gh.gh_contributing_url == "https://github.com/tensorflow/tensorflow/blob/master/CONTRIBUTING.md", True) # Test CONTRIBUTING.md
#         self.assertEqual(gh.gh_new_contributor_score > 0, True) # Test new contributor score

#     def test_invalid_github_url(self):
#         invalid_url = 'bad_url'
#         gh = GitHubAPIWrapper(invalid_url)
#         self.assertEqual(gh.is_valid, False)
#         invalid_url = 'https://github.com'
#         gh = GitHubAPIWrapper(invalid_url)
#         self.assertEqual(gh.is_valid, False)
#         invalid_url = 'https://github.com/not_a_user/not_a_repo'
#         gh = GitHubAPIWrapper(invalid_url)
#         self.assertEqual(gh.is_valid, False)
#         invalid_url = 'https://github.com/pigeonhole.dev' # missing username
#         gh = GitHubAPIWrapper(invalid_url)
#         self.assertEqual(gh.is_valid, False)

class GitHubAPIWrapperTestCases(unittest.TestCase):

    def test_valid_github_url(self):
        app = create_app()
        with app.app_context():
            delete_all_projects_from_db(testing=True)
            # valid_url = 'https://github.com/pytorch/pytorch'
            valid_url = 'https://github.com/up-for-grabs/up-for-grabs.net'
            # valid_url = 'https://github.com/SSENSE/vue-carousel/'
            # valid_url = 'https://github.com/urllib3/urllib3/'
            # valid_url = 'https://github.com/SeleniumHQ/selenium'
            # valid_url = 'https://github.com/pypa/setuptools/'
            # valid_url = 'https://github.com/JuliaPlots/Plots.jl/'
            current_time = dt.now()
            gh = GitHubAPIWrapper(valid_url)
            print(f"gh_new_contributor_score = {gh.gh_new_contributor_score}")
            # print(f"Contains bounties: {gh.gh_has_bounty_label}")
            end_time = dt.now()

if __name__ == '__main__':
    unittest.main()