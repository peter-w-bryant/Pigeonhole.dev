# Path: backend\github.py
import requests
import config

class GitHubAPI:
    """GitHub API wrapper class"""
    def __init__(self, username, repo_name):
        self.username = username
        self.repo_name = repo_name
        self.base_url = f"https://api.github.com/repos/{self.username}/{self.repo_name}"
        self.auth_headers = {'Authorization': 'token ' + config.github_token}
        self.repo = requests.get(self.base_url, headers=self.auth_headers).json()

    def get_repo_url(self):
        """Get the repo URL"""
        return self.repo["html_url"]

    def get_repo_description(self):
        """Get the repo description"""
        return self.repo["description"]

    def get_stargazers_count(self):
        """Get the number of stargazers (people who starred the repo)"""
        return self.repo["stargazers_count"]

    def get_forks_count(self):
        """Get the number of forks (people who forked the repo)"""
        return self.repo["forks_count"]

    def get_watchers_count(self):
        """Get the number of watchers (people who watched the repo)"""
        return self.repo["watchers_count"]

    def get_open_issues_count(self):
        """Get the number of open issues"""
        return self.repo["open_issues_count"]

    def get_topics(self):
        """Get the topics"""
        return self.repo["topics"]
    
    def get_issues(self):
        """Get the issues"""
        issues_json = requests.get(self.base_url + "/issues", headers=self.auth_headers).json()
        issue_labels = []
        for issue in issues_json:
            try:
                if issue['labels']:
                    for i in range(len(issue['labels'])):
                        if issue['labels'][i]['name'] not in issue_labels:
                            issue_labels.append(issue['labels'][i]['name'])
            except: 
                pass
        return issue_labels

if __name__ == '__main__':
    gh = GitHubAPI('up-for-grabs', 'up-for-grabs.net') # GitHub API wrapper
    gh.get_issues()
    

    

    