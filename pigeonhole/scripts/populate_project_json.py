import sys
import os
import argparse
from json_crud import add_project_to_static_json, add_batch_projects_to_static_json, \
    delete_project_from_static_json, delete_all_projects_from_static_json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # set path to backend\api
from app import create_app

def main(args):
    app = create_app()
    with app.app_context():
        # repo_url = "https://github.com/peter-w-bryant/Pigeonhole.dev"
        # add_project_to_static_json(repo_url)
        delete_all_projects_from_static_json()
        add_batch_projects_to_static_json(num_projects=3)
        # delete_project_from_static_json(repo_url)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add projects to the database from JSON file.")
    parser.add_argument("size", type=int, help="Number of projects to add", default=-1, nargs='?')
    args = parser.parse_args()
    if args.size < 1:
        args.size = -1
    main(args)