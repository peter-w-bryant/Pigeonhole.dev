import time
import json
import os
import sys
from dotenv import dotenv_values
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Add the parent directory to the path

from scripts.github_api_wrapper import GitHubAPIWrapper
from utils.db import db
from utils.models import Users, Projects


def add_project_to_db(gh_repo_url: str):
    """Populate the project table with data for a single project.
    :param gh_repo_url: GitHub repository URL
    :return: True if successful, False otherwise
    """

    print("gh_repo_url: ", gh_repo_url)

    exists = Projects.query.filter_by(gh_repo_url=gh_repo_url).first() # Check if the repo is already in the database

    print("exists: ", exists)
    
    if exists is not None:
        return {"status": "error", "message": "Project already exists in the database."}
    
    gh = GitHubAPIWrapper(gh_repo_url) # GitHub API wrapper

    if gh.is_valid is False:
        return {"status": "error", "message": "Invalid GitHub repository URL."}
    
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
        
        print(len(gh.gh_topics), len(gh.gh_issues))
        print(gh.gh_topics)
        print(gh.gh_issues)

        # DB Topics Column Values
        # topics_vals = f"N'{gh.gh_topics[0]}', N'{gh.gh_topics[1]}', N'{gh.gh_topics[2]}', N'{gh.gh_topics[3]}', \
        #                 N'{gh.gh_topics[4]}', N'{gh.gh_topics[5]}'"

        topics_vals = ""
        for topic in gh.gh_topics:
            topics_vals += f"N'{topic}', "
        topics_vals = topics_vals[:-2]  # remove the last comma and space

        # DB Issues Column Values
        # issues_vals = f"N'{gh.gh_issues[0]}', N'{gh.gh_issues[1]}', N'{gh.gh_issues[2]}', N'{gh.gh_issues[3]}', \
        #                 N'{gh.gh_issues[4]}', N'{gh.gh_issues[5]}', N'{gh.gh_issues[6]}'"

        issues_vals = ""
        for issue in gh.gh_issues:
            issues_vals += f"N'{issue}', "
        issues_vals = issues_vals[:-2]  # remove the last comma and space


        # DB Issues Counts Column Values
        # issue_counts = f"N'{gh.gh_issues_dict[gh.gh_issues[0]]}', N'{gh.gh_issues_dict[gh.gh_issues[1]]}', \
        #                  N'{gh.gh_issues_dict[gh.gh_issues[2]]}', N'{gh.gh_issues_dict[gh.gh_issues[3]]}', \
        #                  N'{gh.gh_issues_dict[gh.gh_issues[4]]}', N'{gh.gh_issues_dict[gh.gh_issues[5]]}', \
        #                  N'{gh.gh_issues_dict[gh.gh_issues[6]]}'"
        
        issue_counts = ""
        if gh.gh_issues_dict == {}:
            for issue in gh.gh_issues:
                issue_counts += f"N'0', "
        else:
            for issue in gh.gh_issues:
                issue_counts += f"N'{gh.gh_issues_dict[issue]}', "
        issue_counts = issue_counts[:-2]  

        # All DB Column Values  
        values = f"(N'{gh.repo_name}', N'{gh_repo_url}', N'{gh.gh_description}', N'{gh.username}', \
                   {gh.gh_stargazers_count}, {gh.gh_forks_count}, {gh.gh_watchers_count}, \
                   {topics_vals}, {issues_vals}, {issue_counts}, N'{gh.gh_date_of_last_commit}', \
                   N'{gh.gh_date_of_last_merged_pull_request}', N'{gh.gh_contributing_url}', N'{gh.gh_new_contributor_score}')" 
            
        q = f"INSERT INTO projects {cols} VALUES {values}"
        
        print("f1")
        # Initialize Projects object
        project = Projects(gh_repo_name=gh.repo_name, gh_repo_url=gh_repo_url, gh_description=gh.gh_description, gh_username=gh.username, 
                           num_stars=gh.gh_stargazers_count, num_forks=gh.gh_forks_count, num_watchers=gh.gh_watchers_count, 
                            gh_topics0=gh.gh_topics[0], gh_topics1=gh.gh_topics[1], gh_topics2=gh.gh_topics[2], gh_topics3=gh.gh_topics[3], 
                            gh_topics4=gh.gh_topics[4], gh_topics5=gh.gh_topics[5], issue_label_1=gh.gh_issues[0], issue_label_2=gh.gh_issues[1], 
                            issue_label_3=gh.gh_issues[2], issue_label_4=gh.gh_issues[3], issue_label_5=gh.gh_issues[4],
                            issue_label_6=gh.gh_issues[5], issue_label_7=gh.gh_issues[6], issue_label_1_count=gh.gh_issues_dict[gh.gh_issues[0]],
                            issue_label_2_count=gh.gh_issues_dict[gh.gh_issues[1]], issue_label_3_count=gh.gh_issues_dict[gh.gh_issues[2]],
                            issue_label_4_count=gh.gh_issues_dict[gh.gh_issues[3]], issue_label_5_count=gh.gh_issues_dict[gh.gh_issues[4]],
                            issue_label_6_count=gh.gh_issues_dict[gh.gh_issues[5]], issue_label_7_count=gh.gh_issues_dict[gh.gh_issues[6]],
                            date_last_commit=gh.gh_date_of_last_commit, date_last_merged_PR=gh.gh_date_of_last_merged_pull_request,
                            contrib_url=gh.gh_contributing_url, new_contrib_score=gh.gh_new_contributor_score)
        
        print("f2")
        # Add project to the database
        db.session.add(project)
        db.session.commit()

    except IndexError as ie:
        return {'status': 'error', 'message': 'IndexError: ' + str(ie)}

    # Close the connection
    return {'status': 'success', 'message': 'Project added successfully'}

def add_projects_to_db_from_json(source_json_path = False, testing: bool = False):
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

        file_path = os.path.join(parent_dir, 'backend', 'api', 'resources', 'repo_scrapers', 'small_repo_data.json')
    else: 
        file_path = os.path.join(parent_dir, 'backend', 'api', 'resources', 'repo_scrapers', source_json_path)
    
    repo_data = json.load(open(file_path, 'r')) 
    failed_repos = {}
    success_count = 0
    duplicates_count = 0
    try:
        for repo_url in repo_data.values():
            error, added = add_project_to_db(repo_url)
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

def fetch_all_projects():
    """Fetch all data from the projects table.
    :return: A dictionary of dictionaries containing all the data from the projects table.
    """
    all_projects = Projects.query.all()
    all_projects_dict = {}
    for project in all_projects:
        single_project_dict = {}
        single_project_dict["pUID"]= project.pUID
        single_project_dict["gh_repo_name"]= project.gh_repo_name
        single_project_dict["gh_description"]= project.gh_description
        single_project_dict["gh_rep_url"]= project.gh_repo_url
        single_project_dict["num_stars"]= project.num_stars
        single_project_dict["num_forks"]= project.num_forks
        single_project_dict["num_watchers"]= project.num_watchers
        single_project_dict["issue_label_1"]= project.issue_label_1
        single_project_dict["issue_label_2"]= project.issue_label_2
        single_project_dict["issue_label_3"]= project.issue_label_3
        single_project_dict["issue_label_4"]= project.issue_label_4
        single_project_dict["issue_label_5"]= project.issue_label_5
        single_project_dict["issue_label_6"]= project.issue_label_6
        single_project_dict["issue_label_7"]= project.issue_label_7
        single_project_dict["issue_label_1_count"]= project.issue_label_1_count
        single_project_dict["issue_label_2_count"]= project.issue_label_2_count
        single_project_dict["issue_label_3_count"]= project.issue_label_3_count
        single_project_dict["issue_label_4_count"]= project.issue_label_4_count
        single_project_dict["issue_label_5_count"]= project.issue_label_5_count
        single_project_dict["issue_label_6_count"]= project.issue_label_6_count
        single_project_dict["issue_label_7_count"]= project.issue_label_7_count
        single_project_dict["gh_username"]= project.gh_username
        single_project_dict["date_last_merged_PR"]= project.date_last_merged_PR
        single_project_dict["date_last_commit"]= project.date_last_commit
        single_project_dict["gh_topics_0"]= project.gh_topics0
        single_project_dict["gh_topics_1"]= project.gh_topics1
        single_project_dict["gh_topics_2"]= project.gh_topics2
        single_project_dict["gh_topics_3"]= project.gh_topics3
        single_project_dict["gh_topics_4"]= project.gh_topics4
        single_project_dict["gh_topics_5"]= project.gh_topics5
        single_project_dict["gh_contributing_url"]= project.contrib_url
        single_project_dict["new_contrib_score"]= project.new_contrib_score
        all_projects_dict[single_project_dict["gh_repo_name"]] = single_project_dict
    return all_projects_dict

# if __name__ == "__main__":
    # gh_repo_url  = 'https://github.com/rocketchat/rocket.chat'  
    # print("Populating Projects table...")
    # with app.app_context():
    #     # add_project_to_db(gh_repo_url) # solo project pop
    #     add_projects_to_db_from_json(testing= True)  # JSON project pops
    #     # delete_projects() # delete all projects
