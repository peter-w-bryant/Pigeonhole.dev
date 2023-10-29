from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_login import login_required
from icecream import ic

import pigeonhole.api_docs
from pigeonhole.scripts import (
    GitHubAPIWrapper,
    add_project_to_static_json,
    read_all_projects_from_static_json,
)

projects = Blueprint('projects', __name__) # blueprint for auth routes

@projects.route('/search', methods=['POST'])
def search_projects():
    data = request.get_json()
    query = data.get('query', '').lower()
    
    projects = read_all_projects_from_static_json()
    
    for project_url, project_dict in projects.items():
        if query in project_dict['repo_name'].lower():
            ic(project_dict)
            return jsonify(project_dict)

    return {}

@projects.route('/projects/add-project', methods=['POST'])
@jwt_required()
def create_a_new_project():
    """
    Adds a new project to the database given a GitHub URL.
    """
    if request.method == 'POST':
        current_user_UID = get_jwt_identity()
        gh_url = request.get_json()['gh_url']
        gh = GitHubAPIWrapper(gh_url)
        if not gh.is_valid:
            return jsonify({'status': 'error', 'message': 'Invalid GitHub URL!'}), 400
        
        project = Projects.query.filter_by(gh_repo_url=gh.repo_url).first()    
        if project is not None:
            return jsonify({'status': 'error', 'message': 'Project already exists in database!'}), 409
        
        response = add_project_to_db(gh.repo_url, current_user_UID)
        if response['status'] == 'success':
            return jsonify({'status': 'success', 'message': 'Project added to database!', 'project_dict': response['project_dict']}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Error adding project to database!'}), 500

create_a_new_project.__doc__ = pigeonhole.api_docs.create_project_doc.__doc__

@projects.route('/projects/all-projects', methods=['GET'])
def read_all_project_data():
    """
    Returns all project data in the database as a JSON object or an error message if there was an error retrieving the data
    ---
    tags:
      - Projects
    parameters:
      - name: per_page
        in: query
        type: integer
        required: false
        default: 10
        description: Number of results to return per page (max 100).
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: Page number to return.
      - name: max_issues_per_project
        in: query
        type: string or integer
        required: false
        default: all
        description: Maximum number of issues to return per project. Either provide an integer number of issues per project, or 'all' for all issues per project (can exceed 100). If the number of issues provided is negative, the default of 10 will be used.
      - name: max_topics_per_project
        in: query
        type: string or integer
        required: false
        default: all
        description: Maximum number of topics to return per project. Either provide an integer number of topics per project, or 'all' for all topics per project. If the number of topics provided is negative, the default of 10 will be used.
    responses:
      200:
        description: Project data returned successfully.
      500:
        description: Error retrieving project data.
    """
    if request.method == 'GET':
        # Get query parameters
        per_page = request.args.get('per_page', default=10, type=int)
        page = request.args.get('page', default=1, type=int)
        max_issues_per_project = request.args.get('max_issues_per_project', default='all', type=str)
        max_topics_per_project = request.args.get('max_topics_per_project', default='all', type=str)

        # Ensure per_page is between 1 and 100
        if per_page > 100:
            per_page = 100
        elif per_page < 1:
            per_page = 10

        # Ensure page is greater than 0
        if page < 1:
            page = 1

        # Ensure max_issues_per_project is >= 0
        if max_issues_per_project != 'all':
            max_issues_per_project = int(max_issues_per_project)
            if max_issues_per_project < 0:
                max_issues_per_project = 10

        # Ensure max_topics_per_project is >= 0
        if max_topics_per_project != 'all':
            max_topics_per_project = int(max_topics_per_project)
            if max_topics_per_project < 0:
                max_topics_per_project = 10

        print("Calling response dict")
        all_projects = read_all_projects_from_static_json()
        return all_projects, 200