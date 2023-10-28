# Path: backend\github.py
import json
import os
import sys

import requests
from dotenv import dotenv_values, load_dotenv
from github import Auth, Github

from scripts.enrichment import (
    generate_collaboration_health_score,
    generate_new_contributor_score,
    get_contribute_url,
    get_date_of_last_commit,
    get_num_commits,
    get_pr_analysis,
    get_target_issues,
)


class GitHubAPIWrapper:
    def __init__(self, repo_url):
        load_dotenv()
        try:
            if not repo_url.startswith("https://github.com") or repo_url == "https://github.com":
                self.is_valid = False
            else:
                self.username = repo_url.split('/')[3]
                self.repo_name = repo_url.split('/')[4]

                # New PyGithub API
                auth = Auth.Token(os.environ.get('GITHUB_TOKEN'))
                self.g = Github(auth=auth)
                self.repo = self.g.get_repo(f"{self.username}/{self.repo_name}")

                # Old GitHub API
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
                    
                    # Quantitative Repo Data
                    self.gh_num_open_issues = self.repo.open_issues_count
                    self.gh_stargazers_count = self.repo.stargazers_count
                    self.gh_forks_count = self.repo.forks_count
                    self.gh_watchers_count = self.repo.watchers_count
                    
                    try:
                        self.gh_num_contributors = self.repo.get_contributors().totalCount # Get number of contributors
                    except Exception as e:
                        print(f"Error in GitHubAPIWrapper INIT on line {sys.exc_info()[-1].tb_lineno}:", e)
                        self.gh_num_contributors = 100
                    
                    self.gh_topics = self.repo.get_topics()

                    # Enrichment
                    self.gh_contributing_url = get_contribute_url(self) # Get CONTRIBUTING.md URL
                    self.gh_num_commits = get_num_commits(self)         # Get number of commits

                    # self.gh_pr_dict = get_pr_analysis(self)
                    self.gh_has_bounty_label = False                             # Flag for if 'bounty' or 'bounties' exist in any issue labels, set in get_target_issues()
                    self.gh_issues_dict = get_target_issues(self)                # Get the issue labels and counts for targetted labels
                    self.gh_date_of_last_commit = get_date_of_last_commit(self)  # Date of last commit
                    self.gh_new_contributor_score = generate_new_contributor_score(self)     # Generate New Contributor Score
                    self.gh_collaboration_health = generate_collaboration_health_score(self) # Generate Collaboration Health Score

        except Exception as e:
            print(f"Error in GitHubAPIWrapper INIT on line {sys.exc_info()[-1].tb_lineno}:", e)
            self.is_valid = False

    def __str__(self):
        return f"{json.dumps(self.to_dict(), indent=4)}"
    
    def to_dict(self):
        return {

                "repo_name": self.repo_name,
                "username": self.username,
                "repo_url": self.repo_url,
                "gh_description": self.gh_description,
                "gh_topics": self.gh_topics,
                "gh_date_of_last_commit": self.gh_date_of_last_commit,
                "gh_contributing_url": self.gh_contributing_url,
                "gh_has_bounty_label": self.gh_has_bounty_label,
                "gh_issues_dict": self.gh_issues_dict,
                "gh_num_commits": self.gh_num_commits,
                "gh_num_open_issues": self.gh_num_open_issues,
                "gh_num_contributors": self.gh_num_contributors,
                "gh_stargazers_count": self.gh_stargazers_count,
                "gh_forks_count": self.gh_forks_count,
                "gh_watchers_count": self.gh_watchers_count,
                "gh_new_contributor_score": self.gh_new_contributor_score,
                "gh_collaboration_health": self.gh_collaboration_health
        }

    def verify_repo_url(self):
        """Verify if the repo url is valid"""
        try:
            if self.response.status_code != 200 or self.repo_data["message"] == "Not Found":
                return False
        except KeyError:
            return True

    def get_repo_description(self):
        return self.repo_data["description"]

    def get_topics(self):
        return self.repo_data["topics"]
    
    def get_open_issues_count(self):
        return self.repo_data["open_issues_count"]
    
    def get_pr_count(self):
        return self.repo_data["pulls_count"]