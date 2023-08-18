import requests

def get_num_commits(self):
    """Get the number of commits"""
    try:
        commits_json = requests.get(self.base_url + "/commits", headers=self.auth_headers).json()
        num_commits = len(commits_json)
    except Exception as e:
        print(self.repo_name, e)
        num_commits = 0
    return num_commits