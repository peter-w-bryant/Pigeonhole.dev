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
def get_date_of_last_merged_pull_request(self):
    """Get the date of the last merged pull request"""
    try:
        pulls_json = requests.get(self.search_url + "+is:pr+is:merged", headers=self.auth_headers).json()
        date_of_last_merged_pull_request = pulls_json["items"][0]["closed_at"].split("T")[0]
    except IndexError as ie:
        date_of_last_merged_pull_request = ""
    except KeyError as ke:
        date_of_last_merged_pull_request = ""
    except Exception as e:
        template = "get_date_of_last_merged_pull_request(): An exception of type {0} occurred. Arguments:\n{1!r}" # !r is used to get the raw representation of the argument
        message = template.format(type(e).__name__, e.args) # type(e).__name__ gets the name of the exception type and e.args gets the arguments passed to the exception
    return date_of_last_merged_pull_request