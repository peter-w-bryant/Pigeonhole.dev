# Path: backend\github.py
import requests
from datetime import datetime
from dotenv import dotenv_values, load_dotenv
import os
from datetime import datetime as dt
import sys
from .enrichment import get_target_issues, get_contribute_url, get_date_of_last_commit, get_date_of_last_merged_pull_request, generate_new_contributor_score, generate_collaboration_health_score

class GitHubAPIWrapper:
    def __init__(self, repo_url):
        load_dotenv()
        try:
            if not repo_url.startswith("https://github.com") or repo_url == "https://github.com":
                self.is_valid = False
            else:
                self.auth_headers = {'Authorization': 'token ' + os.environ.get('GITHUB_TOKEN')}

                self.repo_url = repo_url
                self.username = repo_url.split('/')[3]
                self.repo_name = repo_url.split('/')[4]
                self.base_url = f"https://api.github.com/repos/{self.username}/{self.repo_name}"
                self.search_url = f"https://api.github.com/search/issues?q=repo:{self.username}/{self.repo_name}"
                
                # Make request to GitHub API
                self.response = requests.get(self.base_url, headers=self.auth_headers)
                self.repo_data = self.response.json()

                if not self.verify_repo_url():
                    self.is_valid = False
                else:
                    # Qualitative Repo Data
                    self.is_valid = True
                    self.gh_description = self.get_repo_description()
                    self.gh_topics = [].extend(self.get_topics())  # Get topics / tech stack
                    
                    # Quantitative Repo Data
                    self.gh_num_commits = self.get_num_commits()
                    self.gh_num_open_issues = self.get_open_issues_count()
                    self.gh_num_contributors = self.get_num_contributors()
                    self.gh_stargazers_count = self.get_stargazers_count()
                    self.gh_forks_count = self.get_forks_count()
                    self.gh_watchers_count = self.get_watchers_count()
                    
                    # Enrichment
                    # -> Contributing URL
                    self.gh_contributing_url = get_contribute_url(self) # Get CONTRIBUTING.md URL
                    # -> Issues
                    self.gh_has_bounty_label = False              # Flag for if 'bounty' or 'bounties' exist in any issue labels, set in get_target_issues()
                    self.gh_issues_dict = get_target_issues(self) # Get the issue labels and counts for targetted labels
                    # -> Dates
                    self.gh_date_of_last_commit = get_date_of_last_commit(self)                           # Date of last commit
                    self.gh_date_of_last_merged_pull_request = get_date_of_last_merged_pull_request(self) # Date of last MERGED pull request
                    # -> Generated Scores and Analysis
                    self.gh_new_contributor_score = generate_new_contributor_score(self)     # Generate New Contributor Score
                    self.gh_collaboration_health = generate_collaboration_health_score(self) # Generate Collaboration Health Score

        except Exception as e:
            print(f"Error in GitHubAPIWrapper INIT on line {sys.exc_info()[-1].tb_lineno}:", e)
            self.is_valid = False

    def __str__(self):
        return f"{self.repo_url}"

    def verify_repo_url(self):
        """Verify if the repo url is valid"""
        try:
            if self.response.status_code != 200 or self.repo_data["message"] == "Not Found":
                return False
        except KeyError:
            return True

    def get_repo_description(self):
        return self.repo_data["description"]

    def get_stargazers_count(self):
        return self.repo_data["stargazers_count"]

    def get_forks_count(self):
        return self.repo_data["forks_count"]

    def get_watchers_count(self):
        return self.repo_data["watchers_count"]

    def get_topics(self):
        return self.repo_data["topics"]
    
    def get_open_issues_count(self):
        return self.repo_data["open_issues_count"]
    
    def get_num_commits(self):
        return self.repo_data["size"]
    
    def get_num_contributors(self):
        return self.repo_data["network_count"]