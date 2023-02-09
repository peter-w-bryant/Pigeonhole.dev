import random
import string
import logging
import json
import httplib2
import requests

import mysql.connector

import config
from github import GitHubAPI

class PopulateDB:
    """Populate the database with data from GitHub API"""
    def __init__(self):
        self.conn = mysql.connector.connect(
                        user=config.db_user,
                        password=config.db_password,
                        host=config.db_host,
                        database=config.db_database
                    )

    def pop_project(self, gh_repo_url):
        """Populate the project table"""
        gh = GitHubAPI(gh_repo_url) # GitHub API wrapper

        gh_repo_name = gh.repo_name
        gh_username = gh.username

        # Get the data from GitHub API
        gh_description = gh.get_repo_description()

        # Topics / tech stack
        gh_topics = [''] * 6 # empty list of 6 strings to store the topics
        gh_topics[:len(gh.get_topics())] = gh.get_topics() # get the topics

        # Issues / labels
        gh_issues = [''] * 3 # empty list of 3 strings to store the issues
        gh_issues[:len(gh.get_issues())] = gh.get_issues() # get the issues

        # Stars, forks, watchers count
        gh_stargazers_count = gh.get_stargazers_count()
        gh_forks_count = gh.get_forks_count()
        gh_watchers_count = gh.get_watchers_count()

        # Date of last commit
        gh_date_of_last_commit = gh.get_date_of_last_commit()

        # Data of last MERGED pull request
        gh_date_of_last_merged_pull_request = gh.get_date_of_last_merged_pull_request()

        # Insert the data into the database
        try:
            cursor = self.conn.cursor()

            topics_cols = "gh_topics0, gh_topics1, gh_topics2, gh_topics3, gh_topics4, gh_topics5" # Topic column names
            issues_cols = "issue_label_1, issue_label_2, issue_label_3" # Issues column names
            cols = f"(gh_repo_name, gh_repo_url, gh_description, gh_username, num_stars, num_forks, num_watchers, {topics_cols}, {issues_cols}, date_last_commit, date_last_merged_PR)" # All column names

            topics_vals = f"N'{gh_topics[0]}', N'{gh_topics[1]}', N'{gh_topics[2]}', N'{gh_topics[3]}', N'{gh_topics[4]}', N'{gh_topics[5]}'" # Topic values
            issues_vals = f"N'{gh_issues[0]}', N'{gh_issues[1]}', N'{gh_issues[2]}'" # Issues values
            values = f"(N'{gh_repo_name}', N'{gh_repo_url}', N'{gh_description}', N'{gh_username}', {gh_stargazers_count}, {gh_forks_count}, {gh_watchers_count}, {topics_vals}, {issues_vals}, N'{gh_date_of_last_commit}', N'{gh_date_of_last_merged_pull_request}')" # All values
            
            q = f"INSERT INTO projects {cols} VALUES {values}"
            cursor.execute(q)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        
        # Close the connection
        self.conn.close()

if __name__ == '__main__':
    pop = PopulateDB()
    pop.pop_project('https://github.com/up-for-grabs/up-for-grabs.net')