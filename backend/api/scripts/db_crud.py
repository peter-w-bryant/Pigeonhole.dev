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
from utils.models import Users, Projects, ProjectIssues, ProjectTopics

def add_project_to_db(gh_repo_url: str, user_id: int):
    """Populate the project table with data for a single project.
    :param gh_repo_url: GitHub repository URL
    :return: True if successful, False otherwise
    """

    exists = Projects.query.filter_by(gh_repo_url=gh_repo_url).first() # Check if the repo is already in the database

    if exists is not None:
        return {"status": "error", "message": "Project already exists in the database."}
    
    gh = GitHubAPIWrapper(gh_repo_url) 

    if not gh.is_valid:
        return {"status": "error", "message": "Invalid GitHub repository URL."}
    
    # Insert the data into the database
    try:
        # __projects__ table        
        project = Projects(UID=user_id, gh_repo_url=gh.repo_url, gh_repo_name=gh.repo_name, gh_username=gh.username, gh_description=gh.gh_description, \
                           num_stars=gh.gh_stargazers_count, num_forks=gh.gh_forks_count, num_watchers=gh.gh_watchers_count, \
                           date_last_merged_PR=gh.gh_date_of_last_merged_pull_request, date_last_commit=gh.gh_date_of_last_commit, \
                           contrib_url=gh.gh_contributing_url, new_contrib_score=gh.gh_new_contributor_score)
        db.session.add(project)
        db.session.flush() 
        pUID = project.pUID

        # ___project_topics___ table
        for issue in gh.gh_issues_dict:
            project_issue = ProjectIssues(pUID=pUID, issue_label=issue, issue_label_count=gh.gh_issues_dict[issue])
            db.session.add(project_issue)

        # __project_issues__ table
        for topic in gh.gh_topics:
            project_topic = ProjectTopics(pUID=pUID, topic=topic)
            db.session.add(project_topic)

        db.session.commit()

    except IndexError as ie:
        db.session.rollback()
        return {'status': 'error', 'message': 'IndexError: ' + str(ie)}
    
    except Exception as e:
        db.session.rollback()
        return {'status': 'error', 'message': 'Error: ' + str(e)}

    # Close the connection
    return_dict = {'status': 'success', 'message': 'Project added successfully.', 'project_dict': project.to_dict()}
    db.session.close()
    return return_dict

def add_projects_to_db_from_json(small_repo_data = True, testing: bool = False):
    """Populate the project table with projects links from a json file.

    Args:
        source_json_path (str): absolute path to the source JSON file, default is None.
        testing (bool): flag to enable testing outputs 
    Returns:
        success_count (int): number of projects successfully added to the database
    """
    if testing:
        start = time.time()

    parent_dir = os.path.dirname(os.getcwd())
    if small_repo_data: file_path = os.path.join(parent_dir, 'api', 'resources', 'repo_scrapers', 'small_repo_data.json')
    else: file_path = os.path.join(parent_dir, 'api', 'resources', 'repo_scrapers', 'static_repo_data.json')
    
    with open(file_path, 'r') as f:
        repo_data = json.load(f)

    failed_repos = {}
    success_count = 0
    duplicates_count = 0
    try:
        for repo_url in repo_data.values():
            response_dict = add_project_to_db(repo_url, user_id=1) # todo: change user_id to a random number
            response_msg = response_dict['message']
            if response_msg == 'Project added successfully.':
                success_count += 1
            elif response_msg == 'Project already exists in the database.':
                duplicates_count += 1
            else:
                failed_repos[repo_url.split('/')[-1]] = repo_url + ' | Response Message: ' + response_msg

    except Exception as e:
        print(e)
        # Write failed repos to a file
        failed_repo_file_path = os.path.join(os.getcwd(), 'resources', 'sample_data', 'failed_repos.json')
        with open(failed_repo_file_path, 'w') as f:
            json.dump(failed_repos, f, indent=4)

    if testing:
        end = time.time()
        print(f"Time taken: {end - start} seconds. Added {success_count} projects, {duplicates_count} duplicates found.")

    return success_count

def delete_project_from_db(gh_repo_url: str):
    """Delete a project from the database.
    :param gh_repo_url: GitHub repository URL
    :return: True if successful, False otherwise
    """
    try:
        project = Projects.query.filter_by(gh_repo_url=gh_repo_url).first()
        if project is None:
            return {"status": "error", "message": "Project does not exist in the database."}
        pUID = project.pUID
        # delete related records from other tables
        ProjectIssues.query.filter_by(pUID=pUID).delete()
        ProjectTopics.query.filter_by(pUID=pUID).delete()
        # delete project from Projects table
        db.session.delete(project)
        db.session.commit()
        return {"status": "success", "message": "Project deleted successfully."}
    except Exception as e:
        return {"status": "error", "message": "Error: " + str(e)}

def delete_all_projects_from_db(testing=False):
    """Delete all projects from the database"""
    try:
        projects_num_rows_deleted = db.session.query(Projects).delete()
        projects_issues_num_rows_deleted = db.session.query(ProjectIssues).delete()
        projects_topics_num_rows_deleted = db.session.query(ProjectTopics).delete()
        db.session.commit()
        
        if testing:
            print(f"Deleted {projects_num_rows_deleted} rows from the projects table.")
            print(f"Deleted {projects_issues_num_rows_deleted} rows from the project_issues table.")
            print(f"Deleted {projects_topics_num_rows_deleted} rows from the project_topics table.")
    except Exception as e:
        print(e)

def read_all_project_data_json(per_page=10, page_num=1, max_issues_per_project='all', max_topics_per_project='all'):
    """
    Fetch all data from the projects table.
    :param per_page: The number of results to return per page. (default is 10)
    :param page_num: The page number to start retrieving results. (default is 1)
    :param max_issues_per_project: The maximum number of issues to return per project. (default is 5)
    :return: A dictionary of dictionaries containing all the data from the projects table, or an error message.
    """
    all_projects_dict = {}

    # Retrieve the current page of results
    try:
        projects_page = Projects.query.paginate(page=page_num, per_page=per_page)
    except Exception as e:
        return {"status": "error", "message": "Page not found."}
    
    # Add the projects from the current page to the dictionary
    for project in projects_page.items:
        single_project_dict = {}

        # ___projects___ table
        single_project_dict["pUID"]= project.pUID
        single_project_dict["gh_rep_url"]= project.gh_repo_url
        single_project_dict["gh_repo_name"]= project.gh_repo_name
        single_project_dict["gh_username"]= project.gh_username
        single_project_dict["gh_description"]= project.gh_description
        
        single_project_dict["num_stars"]= project.num_stars
        single_project_dict["num_forks"]= project.num_forks
        single_project_dict["num_watchers"]= project.num_watchers
        
        single_project_dict["date_last_merged_PR"]= project.date_last_merged_PR
        single_project_dict["date_last_commit"]= project.date_last_commit
        single_project_dict["gh_contributing_url"]= project.contrib_url
        single_project_dict["new_contrib_score"]= project.new_contrib_score

        # ___project_issues___ table
        project_issues = ProjectIssues.query.filter_by(pUID=project.pUID).all()
        if max_issues_per_project == 'all':
            for i in range(len(project_issues)):
                single_project_dict[f"issue_label_{i+1:02d}"]= project_issues[i].issue_label
                single_project_dict[f"issue_label_{i+1:02d}_count"]= project_issues[i].issue_label_count
        else:
            for i in range(len(project_issues)):
                if i >= max_issues_per_project:
                    break
                single_project_dict[f"issue_label_{i+1:02d}"]= project_issues[i].issue_label
                single_project_dict[f"issue_label_{i+1:02d}_count"]= project_issues[i].issue_label_count

        # ___project_topics___ table
        project_topics = ProjectTopics.query.filter_by(pUID=project.pUID).all()
        if max_topics_per_project == 'all':
            for i in range(len(project_topics)):
                single_project_dict[f"gh_topics_{i:02d}"]= project_topics[i].topic
        else:
            for i in range(len(project_topics)):
                if i >= max_topics_per_project:
                    break
                single_project_dict[f"gh_topics_{i:02d}"]= project_topics[i].topic
                
        all_projects_dict[project.pUID] = single_project_dict
    return all_projects_dict