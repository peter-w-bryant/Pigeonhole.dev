import requests  

def get_contribute_url(self):
    """Get the CONTRIBUTING.md url"""
    contribute_url = self.repo_data["html_url"] + "/blob/master/CONTRIBUTING.md"
    if requests.get(contribute_url).status_code == 404:
        return ""
    else:
        return contribute_url