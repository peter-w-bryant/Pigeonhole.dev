import requests
from flask import (
    Blueprint,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from icecream import ic

import pigeonhole.api_docs

index = Blueprint('index', __name__) # blueprint for auth routes

@index.route('/', methods=['GET', 'POST'])
def get_index():
    
    # Build all projects payload
    all_projects_response = requests.get('http://localhost:5000/api/projects/all-projects')
    if all_projects_response.status_code == 200:
        all_projects_json = all_projects_response.json()
    else:
        all_projects_json = {}
    
    if request.method == 'POST':
        return render_template('index.html', projects=all_projects_json)

    return render_template('index.html', projects=all_projects_json)