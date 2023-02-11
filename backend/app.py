from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash

import config
from github import GitHubAPI
from db import DB
from pop_db import PopulateDB

app = Flask(__name__)

@app.route('/add-project', methods=['GET', 'POST'])
def AddNewProject():
    """Add a new project to the database given a ?gh_url=GIT_HUB_REPO_URL"""
    if request.method == 'GET': # will be POST in production
        gh_url = request.args.get('gh_url')
        gh_url = "https://github.com/pallets/flask" # valid repo for testing
        gh = GitHubAPI(gh_url)
        is_valid = gh.verify_repo_url()
        if not is_valid:
            return {"error": "Invalid GitHub URL"}
        else:
            insert_result = PopulateDB().pop_project(gh_url)
            return insert_result
            
@app.route('/all-projects', methods=['GET', 'POST'])
def AllProjectData():
    """Get all project data from the database"""
    if request.method == 'GET':
        all_projects = DB().fetchall("projects")
        DB().__exit__
        return jsonify(all_projects)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
