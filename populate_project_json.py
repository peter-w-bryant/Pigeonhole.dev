import sys
import os
import argparse
from pigeonhole.scripts.json_crud import add_project_to_static_json, add_batch_projects_to_static_json, \
    delete_project_from_static_json, delete_all_projects_from_static_json

from pigeonhole import create_app

def main(args):
    app = create_app()
    with app.app_context():
        # repo_url = "https://github.com/peter-w-bryant/Pigeonhole.dev"
        # add_project_to_static_json(repo_url)
        delete_all_projects_from_static_json()
        add_batch_projects_to_static_json(num_projects=args.size, static_json_filename="medium_repo_data.json")
        # delete_project_from_static_json(repo_url)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add projects to the database from JSON file.")
    parser.add_argument("size", type=int, help="Number of projects to add", default=-1, nargs='?')
    args = parser.parse_args()
    if args.size < 1:
        args.size = -1
    main(args)