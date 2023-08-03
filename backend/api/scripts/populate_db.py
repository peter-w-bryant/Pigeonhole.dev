import sys
import os
from db_crud import add_projects_to_db_from_json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # set path to backend\api
from app import create_app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        add_projects_to_db_from_json()