# Path: backend\github.py
import requests
from datetime import datetime
from dotenv import dotenv_values, load_dotenv
import os
from datetime import datetime as dt

from .enrichment import generate_new_contributor_score, generate_collaboration_health_score

new_contrib_issue_list = ['good first issue', 'up-for-grabs', 'help wanted', 'easy to fix',
                          'easy', 'starter-task', 'contribution-starter', 'level:starter',
                          'newbie', 'beginner experience', 'beginners', 'beginner friendly',
                          'beginner-friendly-issues', 'beginner-task', 'difficulty:beginner',
                          'difficulty:easy', 'easy pick', 'easy-pickings', 'first-timers-only',
                          'junior job', 'needs help', 'learning opportunity', 'documentation',
                          'bug', 'enhancement', 'refactor', 'needs investigation', 'testing'
                          'minor', 'trivial']

class GitHubAPIWrapper:
    """
    GitHub API wrapper class
    """
    def __init__(self, repo_url):
        load_dotenv()
        try:
            if not repo_url.startswith("https://github.com") or repo_url == "https://github.com":
                self.is_valid = False
            else:
                self.repo_url = repo_url
                self.username = repo_url.split('/')[3]
                self.repo_name = repo_url.split('/')[4]
                self.base_url = f"https://api.github.com/repos/{self.username}/{self.repo_name}"
                self.search_url = f"https://api.github.com/search/issues?q=repo:{self.username}/{self.repo_name}"
                self.auth_headers = {'Authorization': 'token ' + os.environ.get('GITHUB_TOKEN')}
                self.response = requests.get(self.base_url, headers=self.auth_headers)
                self.status_code = self.response.status_code
                self.repo_data = self.response.json()
                self.gh_has_bounty_label = False
  
                if not self.verify_repo_url():
                    self.is_valid = False
                else:
                    self.is_valid = True
                    self.gh_description = self.get_repo_description()
                    self.gh_num_contributors = self.get_num_contributors()
                    self.gh_stargazers_count = self.get_stargazers_count()
                    self.gh_forks_count = self.get_forks_count()
                    self.gh_watchers_count = self.get_watchers_count()
                    self.gh_date_of_last_commit = self.get_date_of_last_commit()                           # Date of last commit
                    self.gh_date_of_last_merged_pull_request = self.get_date_of_last_merged_pull_request() # Data of last MERGED pull request
                    self.gh_contributing_url = self.get_contribute_url()                                   # Get CONTRIBUTING.md URL

                    # Topics / tech stack
                    self.gh_topics = []
                    self.gh_topics.extend(self.get_topics())

                    # Issues / labels
                    self.gh_issues_dict = self.get_issues()

                    # Enrichment
                    self.gh_collaboration_health = generate_collaboration_health_score(self) # Generate Collaboration Health Score
                    self.gh_new_contributor_score = generate_new_contributor_score(self) # Generate New Contributor Score

        except IndexError as ie:
            # print("IndexError in GitHubAPIWrapper INIT:", ie)
            self.is_valid = False
        
        except Exception as e:
            print("Error in GitHubAPIWrapper INIT:", e)
            self.is_valid = False

    def __str__(self):
        return f"{self.repo_url} - {self.gh_description}"

    def verify_repo_url(self):
        """Verify if the repo url is valid"""
        try:
            if self.repo_data["message"] == "Not Found":
                return False
        except KeyError:
            return True

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
    
    def get_num_contributors(self):
        """Get the number of contributors"""
        return self.repo_data["network_count"]

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

    def get_issues(self):
        """Gets all the open issue labels and the counts of all issue labels for a given repository.

        Returns:
        issue_label_counts(dict): a dictionary with keys corresponding to unique issue labels whose values are the count
        of open issues that have that label tag.
        """
        issue_label_counts = {}
        issue_id_lookup = {}

        for issue_label in new_contrib_issue_list:
            is_valid_page = True
            page = 0
            while is_valid_page:
                page += 1
                query_url = f"{self.base_url}/issues?state=open&per_page=100&page={page}&labels={issue_label}"
                issues_json = requests.get(query_url, headers=self.auth_headers).json()
                if issues_json == []:
                    if page != 1:
                        is_valid_page = False
                    break
                for issue in issues_json:
                    try:
                        if issue['id'] not in issue_id_lookup.keys():
                            issue_id_lookup[issue['id']] = True
                            # add only the issue labels that are in our list of new contributor issue labels
                            for i in range(len(issue['labels'])):
                                label_name = issue['labels'][i]['name'].lower()
                                # if the issue label is not in our dictionary, add it
                                if label_name not in issue_label_counts.keys():
                                    # if the issue label is in our list of new contributor issue labels or if it relates to bounties, add it
                                    if (label_name in new_contrib_issue_list):
                                        issue_label_counts[label_name] = 1
                                    elif('bounty' in label_name) or ('bounties' in label_name):
                                        self.gh_has_bounty_label = True
                                        issue_label_counts[label_name] = 1
                                # if the issue label is in our dictionary, increment the count
                                else:
                                    issue_label_counts[label_name] += 1
                    except Exception as e:
                        # print(e)
                        pass

        return self.get_issues_reorder_keys(issue_label_counts)
    
    def get_issues_reorder_keys(self, issue_dict):
        """Reorders a dictionary of issue label count pairs so that our most important issue
        tags appear first. 

        Args:
        issue_dict(dict): a dictionary with keys corresponding to unique issue labels whose values are the count

        Returns:
        resorted_issue_dict(dict): a dictionary with keys corresponding to unique issue labels whose values are the count
        """
        resorted_issue_dict = {}
        for key in new_contrib_issue_list:
            if key in issue_dict.keys():
                resorted_issue_dict[key] = issue_dict[key]

        # add the rest of the keys
        for key in issue_dict.keys():
            if key not in resorted_issue_dict.keys():
                resorted_issue_dict[key] = issue_dict[key]        

        return resorted_issue_dict

    def get_contribute_url(self):
        """Get the CONTRIBUTING.md url"""
        contribute_url = self.repo_data["html_url"] + "/blob/master/CONTRIBUTING.md"
        if requests.get(contribute_url).status_code == 404:
            return ""
        else:
            return contribute_url