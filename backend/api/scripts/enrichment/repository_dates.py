import requests

def get_date_of_last_commit(self):
    """Get the date of the last commit"""
    try:
        commits_json = requests.get(self.base_url + "/commits", headers=self.auth_headers).json()
        date_of_last_commit = commits_json[0]["commit"]["author"]["date"].split("T")[0]
    except Exception as e:
        print(self.repo_name, e)
        date_of_last_commit = ""
    return date_of_last_commit