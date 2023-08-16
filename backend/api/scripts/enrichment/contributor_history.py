import requests

def get_num_unique_contributors(self):
    """Get the number of unique contributors"""
    try:
        contributors_json = requests.get(self.base_url + "/contributors", headers=self.auth_headers).json()
        num_contributors = len(contributors_json)
    except Exception as e:
        print(self.repo_name, e)
        num_contributors = 0
    return num_contributors