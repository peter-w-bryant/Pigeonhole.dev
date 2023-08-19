import sys
import os
import argparse
from db_crud import add_projects_to_db_from_json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # set path to backend\api
from app import create_app

def main(args):
    app = create_app()
    with app.app_context():
        add_projects_to_db_from_json(args.size, testing=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add projects to the database from JSON file.")
    parser.add_argument("size", choices=["small", "medium", "large"], help="Size of projects to add")
    args = parser.parse_args()
    main(args)