import time
import json
import mysql.connector
from _mysql_connector import MySQLInterfaceError
from mysql.connector.errors import DatabaseError

import config
from github import GitHubAPI

class DB:
    def __init__(self):
        self.conn = mysql.connector.connect(
                        user=config.db_user,
                        password=config.db_password,
                        host=config.db_host,
                        database=config.db_database,
                        charset='utf8mb4',
                        collation='utf8mb4_unicode_ci'
                    )
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close() 

    def insert(self, query, args=None):
        self.cursor.execute(query, args)
        self.conn.commit() 

    def rollback(self):
        self.conn.rollback()

    def fetchall(self, table_name: str):
        """Fetch all data from the projects table.

        Returns:
            all_projects_dict (dict): A dictionary of dictionaries containing all the data from the projects table.
        """

        self.cursor.execute("SELECT * FROM " + table_name)
        all_projects = self.cursor.fetchall()
        all_projects_dict = {}
        for project in all_projects:
            single_project_dict = {}
            single_project_dict["pUID"] = project[0]
            single_project_dict["gh_repo_name"]= project[1]
            single_project_dict["gh_description"]= project[2]
            single_project_dict["gh_rep_url"]= project[3]
            single_project_dict["num_stars"]= project[4]
            single_project_dict["num_forks"]= project[5]
            single_project_dict["num_watchers"]=project[6]
            single_project_dict["issue_label_1"]= project[7]
            single_project_dict["issue_label_2"]= project[8]
            single_project_dict["issue_label_3"]= project[9]
            single_project_dict["issue_label_4"]= project[10]
            single_project_dict["issue_label_5"]= project[11]
            single_project_dict["issue_label_6"]= project[12]
            single_project_dict["issue_label_7"]= project[13]
            single_project_dict["issue_label_1_count"]= project[14]
            single_project_dict["issue_label_2_count"]= project[15]
            single_project_dict["issue_label_3_count"]= project[16]
            single_project_dict["issue_label_4_count"]= project[17]
            single_project_dict["issue_label_5_count"]= project[18]
            single_project_dict["issue_label_6_count"]= project[19]
            single_project_dict["issue_label_7_count"]= project[20]
            single_project_dict["gh_username"]= project[21]
            single_project_dict["date_last_merged_PR"]= project[22]
            single_project_dict["date_last_commit"]= project[23]
            single_project_dict["gh_topics_0"]= project[24]
            single_project_dict["gh_topics_1"]= project[25]
            single_project_dict["gh_topics_2"]= project[26]
            single_project_dict["gh_topics_3"]= project[27]
            single_project_dict["gh_topics_4"]= project[28]
            single_project_dict["gh_topics_5"]= project[29]
            single_project_dict["gh_contributing_url"]= project[30]
            all_projects_dict[single_project_dict["gh_repo_name"]] = single_project_dict

        return all_projects_dict

    def pop_project(self, gh_repo_url: str):
        """Populate the project table with data for a single project.
        
        Args:
            gh_repo_url (str): The GitHub repo URL for the project to be added to the database.

        Returns:
            insert_result (dict): A dictionary containing the result of the insert operation (success or error)
        """

        db = self

        # Check if the repo is already in the database
        db.cursor.execute(f"SELECT gh_repo_url FROM projects WHERE gh_repo_url = '{gh_repo_url}'")
            
        if db.cursor.fetchone() is not None:
            return {"error": "Repo already in database"}

        gh = GitHubAPI(gh_repo_url) # GitHub API wrapper

        gh_repo_name = gh.repo_name
        gh_username = gh.username

        # Get the data from GitHub API
        gh_description = gh.get_repo_description()

        # Topics / tech stack
        gh_topics = [''] * 6 # empty list of 6 strings to store the topics
        gh_topics[:len(gh.get_topics())] = gh.get_topics() # get the topics

        # Issues / labels
        gh_issues_dict = gh.get_issues()
        gh_issues = list(gh_issues_dict.keys())

        # Stars, forks, watchers count
        gh_stargazers_count = gh.get_stargazers_count()
        gh_forks_count = gh.get_forks_count()
        gh_watchers_count = gh.get_watchers_count()

        # Date of last commit
        gh_date_of_last_commit = gh.get_date_of_last_commit()

        # Data of last MERGED pull request
        gh_date_of_last_merged_pull_request = gh.get_date_of_last_merged_pull_request()

        # Get CONTRIBUTING.md URL
        gh_contributing_url = gh.get_contribute_url()

        # Insert the data into the database
        try:
            db.conn.reconnect()

            topics_cols = "gh_topics0, gh_topics1, gh_topics2, gh_topics3, gh_topics4, gh_topics5" # Topic column names
            issues_cols = "issue_label_1, issue_label_2, issue_label_3, issue_label_4, issue_label_5, issue_label_6, issue_label_7" # Issues column names
            issues_counts_cols = "issue_label_1_count, issue_label_2_count, issue_label_3_count, issue_label_4_count, issue_label_5_count, issue_label_6_count, issue_label_7_count"
            
            cols = f"(gh_repo_name, gh_repo_url, gh_description, gh_username, num_stars, num_forks, num_watchers, {topics_cols}, {issues_cols}, {issues_counts_cols}, date_last_commit, date_last_merged_PR, contrib_url)" # All column names

            topics_vals = f"N'{gh_topics[0]}', N'{gh_topics[1]}', N'{gh_topics[2]}', N'{gh_topics[3]}', N'{gh_topics[4]}', N'{gh_topics[5]}'" # Topic values

            issues_vals = f"N'{gh_issues[0]}', N'{gh_issues[1]}', N'{gh_issues[2]}', N'{gh_issues[3]}', N'{gh_issues[4]}', N'{gh_issues[5]}', N'{gh_issues[6]}'" # Issues values

            issue_counts = f"N'{gh_issues_dict[gh_issues[0]]}', N'{gh_issues_dict[gh_issues[1]]}', N'{gh_issues_dict[gh_issues[2]]}', N'{gh_issues_dict[gh_issues[3]]}', \
                             N'{gh_issues_dict[gh_issues[4]]}', N'{gh_issues_dict[gh_issues[5]]}', N'{gh_issues_dict[gh_issues[6]]}'" 
                             
            values = f"(N'{gh_repo_name}', N'{gh_repo_url}', N'{gh_description}', N'{gh_username}', {gh_stargazers_count}, {gh_forks_count}, {gh_watchers_count}, {topics_vals}, {issues_vals}, {issue_counts}, N'{gh_date_of_last_commit}', N'{gh_date_of_last_merged_pull_request}', N'{gh_contributing_url}')" # All values
                
            q = f"INSERT INTO projects {cols} VALUES {values}"
            db.insert(q)

        except IndexError as ie:
            #print(ie)
            pass

        except MySQLInterfaceError as msqle:
            print("MySQLInterfaceError occured when inserting:", gh_repo_url)
            db.rollback()

        except DatabaseError as dbe:
            # If the error is due to incorrect string value 
            if dbe.errno == mysql.connector.errorcode.ER_TRUNCATED_WRONG_VALUE_FOR_FIELD:
                print(dbe)
                print("DatabaseError occured when inserting:", gh_repo_url)
                db.rollback()
        
        # Close the connection
        return {"success": "Repo added to database"}

    def pop_projects_from_json(self, testing: bool = False):
        """Populate the project table with projects links from a json file.
        
        Returns:
            int: Number of projects successfully added to the database
        """
        if testing:
            start = time.time()
        
        db = self
        repo_data = json.load(open('static_repo_data.json', 'r')) 
        
        success_count = 0
        try:
            for repo_url in repo_data.values():
                db.pop_project(repo_url)            
                success_count += 1
        except MySQLInterfaceError as e:
            print("MySQLInterfaceError occured when inserting:", repo_url)
            pass 
        if testing:
            end = time.time()
            print(f"Time taken: {end - start} seconds. Added {success_count} projects.")
        return success_count

if __name__ == "__main__":
    # gh_repo_url = 'https://github.com/up-for-grabs/up-for-grabs.net'
    # gh_repo_url = "https://github.com/Kentico/ems-extension-marketplace"    
    with DB() as db:
        db.pop_projects_from_json(True)
        # db.pop_projects_from_json(testing=True)
