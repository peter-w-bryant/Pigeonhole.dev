# Flask/SQLAlchemy imports
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

# Other imports
import time
import json
import os
import sys
from dotenv import dotenv_values

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Add the parent directory to the path

# Custom imports
from utils import GitHubAPIWrapper
from utils.db import db
from utils.models import Users, Projects
from app import create_app

app = create_app()

def pop_project(gh_repo_url: str):
    """Populate the project table with data for a single project.
    
    Args:
        gh_repo_url (str): The GitHub repo URL for the project to be added to the database.
    Returns:
        insert_result (dict): A dictionary containing the result of the insert operation (success or error)
    """
 
    # Check if the repo is already in the database
    # db.cursor.execute(f"SELECT gh_repo_url FROM projects WHERE gh_repo_url = '{gh_repo_url}'")
    exists = Projects.query.filter_by(gh_repo_url=gh_repo_url).first()
    
    if exists is not None:
        return False, False
    
    gh = GitHubAPIWrapper(gh_repo_url) # GitHub API wrapper

    if gh.is_valid is False:
        return True, False
    
    # Insert the data into the database
    try:
        # DB Topics Column Names
        topics_cols = "gh_topics0, gh_topics1, gh_topics2, gh_topics3, gh_topics4, gh_topics5" 
        # DB Issues Column Names
        issues_cols = "issue_label_1, issue_label_2, issue_label_3, issue_label_4, issue_label_5, \
                       issue_label_6, issue_label_7" 
        
        # DB Issues Counts Column Names
        issues_counts_cols = "issue_label_1_count, issue_label_2_count, issue_label_3_count, \
                              issue_label_4_count, issue_label_5_count, issue_label_6_count, issue_label_7_count"
        
        # All DB Column Names
        cols = f"(gh_repo_name, gh_repo_url, gh_description, gh_username, num_stars, num_forks, num_watchers, \
                 {topics_cols}, {issues_cols}, {issues_counts_cols}, \
                 date_last_commit, date_last_merged_PR, contrib_url, new_contrib_score)" 
        # DB Topics Column Values
        topics_vals = f"N'{gh.gh_topics[0]}', N'{gh.gh_topics[1]}', N'{gh.gh_topics[2]}', N'{gh.gh_topics[3]}', \
                        N'{gh.gh_topics[4]}', N'{gh.gh_topics[5]}'" 
        # DB Issues Column Values
        issues_vals = f"N'{gh.gh_issues[0]}', N'{gh.gh_issues[1]}', N'{gh.gh_issues[2]}', N'{gh.gh_issues[3]}', \
                        N'{gh.gh_issues[4]}', N'{gh.gh_issues[5]}', N'{gh.gh_issues[6]}'"
        # DB Issues Counts Column Values
        issue_counts = f"N'{gh.gh_issues_dict[gh.gh_issues[0]]}', N'{gh.gh_issues_dict[gh.gh_issues[1]]}', \
                         N'{gh.gh_issues_dict[gh.gh_issues[2]]}', N'{gh.gh_issues_dict[gh.gh_issues[3]]}', \
                         N'{gh.gh_issues_dict[gh.gh_issues[4]]}', N'{gh.gh_issues_dict[gh.gh_issues[5]]}', \
                         N'{gh.gh_issues_dict[gh.gh_issues[6]]}'" 
        # All DB Column Values  
        values = f"(N'{gh.repo_name}', N'{gh_repo_url}', N'{gh.gh_description}', N'{gh.username}', \
                   {gh.gh_stargazers_count}, {gh.gh_forks_count}, {gh.gh_watchers_count}, \
                   {topics_vals}, {issues_vals}, {issue_counts}, N'{gh.gh_date_of_last_commit}', \
                   N'{gh.gh_date_of_last_merged_pull_request}', N'{gh.gh_contributing_url}', N'{gh.gh_new_contributor_score}')" 
            
        q = f"INSERT INTO projects {cols} VALUES {values}"
        
        # Initialize Projects object
        project = Projects(gh_repo_name=gh.repo_name, gh_repo_url=gh_repo_url, gh_description=gh.gh_description,
                            gh_username=gh.username, num_stars=gh.gh_stargazers_count, num_forks=gh.gh_forks_count,
                            num_watchers=gh.gh_watchers_count, gh_topics0=gh.gh_topics[0], gh_topics1=gh.gh_topics[1],
                            gh_topics2=gh.gh_topics[2], gh_topics3=gh.gh_topics[3], gh_topics4=gh.gh_topics[4],
                            gh_topics5=gh.gh_topics[5], issue_label_1=gh.gh_issues[0], issue_label_2=gh.gh_issues[1],
                            issue_label_3=gh.gh_issues[2], issue_label_4=gh.gh_issues[3], issue_label_5=gh.gh_issues[4],
                            issue_label_6=gh.gh_issues[5], issue_label_7=gh.gh_issues[6], issue_label_1_count=gh.gh_issues_dict[gh.gh_issues[0]],
                            issue_label_2_count=gh.gh_issues_dict[gh.gh_issues[1]], issue_label_3_count=gh.gh_issues_dict[gh.gh_issues[2]],
                            issue_label_4_count=gh.gh_issues_dict[gh.gh_issues[3]], issue_label_5_count=gh.gh_issues_dict[gh.gh_issues[4]],
                            issue_label_6_count=gh.gh_issues_dict[gh.gh_issues[5]], issue_label_7_count=gh.gh_issues_dict[gh.gh_issues[6]],
                            date_last_commit=gh.gh_date_of_last_commit, date_last_merged_PR=gh.gh_date_of_last_merged_pull_request,
                            contrib_url=gh.gh_contributing_url, new_contrib_score=gh.gh_new_contributor_score)
        
        # Add project to the database
        db.session.add(project)
        db.session.commit()

    except IndexError as ie:
        return True, False

    # Close the connection
    return False, True

def pop_projects_from_json(source_json_path = False, testing: bool = False):
    """Populate the project table with projects links from a json file.

    Args:
        source_json_path (str): absolute path to the source JSON file, default is None.
        testing (bool): flag to enable testing outputs 
    Returns:
        success_count (int): number of projects successfully added to the database
    """
    if testing:
        start = time.time()

    if not source_json_path:
        parent_dir = os.path.dirname(os.getcwd())
        file_path = os.path.join(parent_dir, 'api', 'resources', 'repo_scrapers', 'small_repo_data.json')
    else: 
        file_path = os.path.join(parent_dir, 'api', 'resources', 'repo_scrapers', source_json_path)
    
    repo_data = json.load(open(file_path, 'r')) 
    failed_repos = {}
    success_count = 0
    duplicates_count = 0
    try:
        for repo_url in repo_data.values():
            error, added = pop_project(repo_url)
            if error is True and added is False:
                failed_repos[repo_url.split('/')[-1]] = repo_url
            elif error is False and added is False:
                duplicates_count += 1
            elif error is False and added is True:
                success_count += 1

    except Exception as e:
        print(e)
        # Write failed repos to a file
        with open(os.path.join(os.getcwd(), 'api', 'resources', 'sample_data', 'failed_repos.json'), 'w') as f:
            json.dump(failed_repos, f, indent=4)

    if testing:
        end = time.time()
        print(f"Time taken: {end - start} seconds. Added {success_count} projects, {duplicates_count} duplicates found.")

    return success_count

def delete_projects():
    """Delete all projects from the database"""
    try:
        num_rows_deleted = db.session.query(Projects).delete()
        db.session.commit()
        print(f"{num_rows_deleted} projects deleted.")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    gh_repo_url  = 'https://github.com/rocketchat/rocket.chat'  
    print("Populating Projects table...")
    with app.app_context():
        # pop_project(gh_repo_url) # solo project pop
        pop_projects_from_json(testing= True)  # JSON project pops
        # delete_projects() # delete all projects
