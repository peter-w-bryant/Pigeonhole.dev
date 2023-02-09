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

    def pop_project(self, gh_username, repo_name):
        """Populate the project table"""
        gh = GitHubAPI(gh_username, repo_name) # GitHub API wrapper

        # Get the data from GitHub API
        gh_repo_url = gh.get_repo_url()
        gh_description = gh.get_repo_description()
        gh_stargazers_count = gh.get_stargazers_count()
        gh_forks_count = gh.get_forks_count()
        gh_watchers_count = gh.get_watchers_count()

        # Insert the data into the database
        try:
            cursor = self.conn.cursor()
            cols = "(gh_repo_name, gh_repo_url, gh_description, gh_username, num_stars, num_forks, num_watchers)"
            values = f"(N'{repo_name}', N'{gh_repo_url}', N'{gh_description}', N'{gh_username}', {gh_stargazers_count}, {gh_forks_count}, {gh_watchers_count})"
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
    pop.pop_project('up-for-grabs', 'up-for-grabs.net')