# Flask/SQLAlchemy imports
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

# Other imports
from dotenv import dotenv_values
import time
import json
import os

# Custom imports
from .github_wrapper_util import GitHubAPIWrapper
from utils.db import db
from utils.models import Projects

def fetch_all_projects():
    """Fetch all data from the projects table.

     Returns:
        all_projects_dict (dict): A dictionary of dictionaries containing all the data from the projects table.
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

