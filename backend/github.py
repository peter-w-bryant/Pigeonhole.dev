# Path: backend\github.py
import requests
import config

class GitHubAPI:
    """GitHub API wrapper class"""
    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.username = repo_url.split('/')[3]
        self.repo_name = repo_url.split('/')[4]
        self.base_url = f"https://api.github.com/repos/{self.username}/{self.repo_name}"
        self.search_url = f"https://api.github.com/search/issues?q=repo:{self.username}/{self.repo_name}"
        self.auth_headers = {'Authorization': 'token ' + config.github_token}
        self.repo_data = requests.get(self.base_url, headers=self.auth_headers).json()

    def get_repo_description(self):
        """Get the repo description"""
        return self.repo_data["description"]

    def get_stargazers_count(self):
        """Get the number of stargazers (people who starred the repo)"""
        return self.repo_data["stargazers_count"]

    def get_forks_count(self):
        """Get the number of forks (people who forked the repo)"""
        return self.repo_data["forks_count"]

    def get_watchers_count(self):
        """Get the number of watchers (people who watched the repo)"""
        return self.repo_data["watchers_count"]

    def get_open_issues_count(self):
        """Get the number of open issues"""
        return self.repo_data["open_issues_count"]

    def get_topics(self):
        """Get the topics"""
        return self.repo_data["topics"]
    
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
            except Exception as e:
                print(e)
                pass
        return issue_labels

    def get_date_of_last_commit(self):
        """Get the date of the last commit"""
        commits_json = requests.get(self.base_url + "/commits", headers=self.auth_headers).json()
        date_of_last_commit = commits_json[0]["commit"]["author"]["date"].split("T")[0]
        return date_of_last_commit

    def get_date_of_last_merged_pull_request(self):
        """Get the date of the last merged pull request"""
        pulls_json = requests.get(self.search_url + "+is:pr+is:merged", headers=self.auth_headers).json()
        date_of_last_merged_pull_request = pulls_json["items"][0]["closed_at"].split("T")[0]
        return date_of_last_merged_pull_request

# if __name__ == '__main__':
#     repo_url = 'https://github.com/up-for-grabs/up-for-grabs.net'
#     gh = GitHubAPI(repo_url)
#     gh.get_date_of_last_merged_pull_request() 
    

    

    