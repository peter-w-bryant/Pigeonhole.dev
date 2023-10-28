import time
import json
import os
import sys
from dotenv import load_dotenv
from icecream import ic

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Add the parent directory to the path

from scripts.github_api_wrapper import GitHubAPIWrapper

PATH_TO_STATIC_JSON = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static_data")
PATH_TO_PROJECTS_JSON = os.path.join(PATH_TO_STATIC_JSON, "projects.json")
PATH_TO_FAILED_REPOS_JSON = os.path.join(PATH_TO_STATIC_JSON, 'failed_repos.json')

# CREATE
def add_project_to_static_json(gh_repo_url: str, user_id=1):
    """Populate the project table with data for a single project.
    :param gh_repo_url: GitHub repository URL
    :return: True if successful, False otherwise
    """
    
    with open(PATH_TO_PROJECTS_JSON, "r") as f:
        project_data = json.load(f)
    
    if gh_repo_url in project_data:
        return False, "Project already exists in database!"
    
    gh = GitHubAPIWrapper(gh_repo_url)

    if not gh.is_valid:
        return False, "Invalid GitHub URL!"
    
    try:
        project_data[gh_repo_url] = gh.to_dict()
        with open(PATH_TO_PROJECTS_JSON, "w") as f:
            json.dump(project_data, f, indent=4)

    except Exception as e:
        print("Exception in add_project_to_static_json():")
        print(e, "on line", sys.exc_info()[-1].tb_lineno)
        return False, "Error adding project to database!"

    return True, "Project added to database!"

def add_batch_projects_to_static_json(num_projects = -1, static_json_filename="small_repo_data.json"):
    """Populate the project table with projects links from a json file.

    Args:
        source_json_path (str): absolute path to the source JSON file, default is None.
        testing (bool): flag to enable testing outputs 
    Returns:
        success_count (int): number of projects successfully added to the database
    """
    load_dotenv()

    PATH_TO_STATIC_JSON_PROJECT_URLS = os.path.join(PATH_TO_STATIC_JSON, "sample_repo_url_maps", static_json_filename)

    # Read only the first num_projects from the file
    target_repo_url_dict = {}
    with open(PATH_TO_STATIC_JSON_PROJECT_URLS, 'r') as f:
        repo_urls = json.load(f)
        
        # If num_projects is -1, read all projects, otherwise read only the first num_projects
        if num_projects != -1:
            target_repo_url_dict = {key: repo_urls[key] for key in list(repo_urls)[:num_projects]}
        else:
            target_repo_url_dict = {key: repo_urls[key] for key in list(repo_urls)}

    failed_repos = {}
    try:
        for repo_url in target_repo_url_dict.values():
            project_added, response_msg = add_project_to_static_json(repo_url) # todo: change user_id to a random number
            if not project_added:
                failed_repos[repo_url.split('/')[-1]] = repo_url + ' | Response Message: ' + response_msg
        return True

    except Exception as e:
        print("Exception in add_batch_projects_to_static_json():")
        print(e, "on line", sys.exc_info()[-1].tb_lineno)
        
        # Write failed repos to a file
        with open(PATH_TO_FAILED_REPOS_JSON, 'w') as f:
            json.dump(failed_repos, f, indent=4)

    return False

# READ
def read_all_projects_from_static_json():
    """Read all projects from the static projects.json file.
    :return: A dictionary of all projects
    """
    with open(PATH_TO_PROJECTS_JSON, "r") as f:
        project_data = json.load(f)
    return project_data

def read_one_project_from_static_json(gh_repo_url: str):
    """Read a single project from the static projects.json file.
    :param gh_repo_url: GitHub repository URL
    :return: A dictionary of the project
    """
    with open(PATH_TO_PROJECTS_JSON, "r") as f:
        project_data = json.load(f)
    return project_data[gh_repo_url]

# TODO: UPDATE

# DELETE
def delete_project_from_static_json(gh_repo_url: str):
    """Delete a project from the static projects.json file.
    :param gh_repo_url: GitHub repository URL
    :return: True if successful, False otherwise
    """
    with open(PATH_TO_PROJECTS_JSON, "r") as f:
        project_data = json.load(f)
    
    if gh_repo_url not in project_data:
        return False, "Project does not exist in database!"
    
    try:
        del project_data[gh_repo_url]
        with open(PATH_TO_PROJECTS_JSON, "w") as f:
            json.dump(project_data, f, indent=4)

    except Exception as e:
        print("Exception in delete_project_from_static_json():")
        print(e, "on line", sys.exc_info()[-1].tb_lineno)
        return False, "Error deleting project from database!"

    return True, "Project deleted from database!"

def delete_all_projects_from_static_json():
    """Delete all projects from the static projects.json file.
    :return: True if successful, False otherwise
    """
    try:
        with open(PATH_TO_PROJECTS_JSON, "w") as f:
            json.dump({}, f, indent=4)

    except Exception as e:
        print("Exception in delete_all_projects_from_static_json():")
        print(e, "on line", sys.exc_info()[-1].tb_lineno)
        return False, "Error deleting all projects from database!"

    return True, "All projects deleted from database!"