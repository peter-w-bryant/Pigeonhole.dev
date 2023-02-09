# Path: backend\github.py
import requests
import config

class GitHubAPI:
    """GitHub API wrapper class"""
    def __init__(self, username, repo_name):
        self.username = username
        self.repo_name = repo_name
        self.base_url = "https://api.github.com/repos/{0}/{1}".format(
            self.username, self.repo_name)
        self.auth_headers = {'Authorization': 'token ' + config.github_token}

    def get_repo(self):
        """Get the repo"""
        return requests.get(self.base_url, headers=self.auth_headers).json()

    def get_repo_url(self):
        """Get the repo URL"""
        return self.get_repo()["html_url"]

    def get_repo_description(self):
        """Get the repo description"""
        return self.get_repo()["description"]

    def get_stargazers_count(self):
        """Get the number of stargazers (people who starred the repo)"""
        return self.get_repo()["stargazers_count"]

    def get_forks_count(self):
        """Get the number of forks (people who forked the repo)"""
        return self.get_repo()["forks_count"]

    def get_watchers_count(self):
        """Get the number of watchers (people who watched the repo)"""
        return self.get_repo()["watchers_count"]

    def get_open_issues_count(self):
        """Get the number of open issues"""
        return self.get_repo()["open_issues_count"]

    def get_topics(self):
        """Get the topics"""
        return self.get_repo()["topics"]
    
    def get_issues(self):
        """Get the issues"""
        return requests.get(self.base_url + "/issues", headers=self.auth_headers).json()

    

    

    