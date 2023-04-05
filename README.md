# pigeonhole.dev
An aggregated list of open source projects with issues looking for contributors.

# Table of Contents
1. [Usage](#Usage)

## Usage
In order to run this project in ```development mode``` locally, first clone this repo and step into the project directory,

```bash
git clone https://github.com/peter-w-bryant/pigeonhole.dev.git
cd pigeonhole.dev
```
Next, initializing and running the backend and frontend servers.

### Backend Setup
First, step into the backend directory, create/activate a Python virtual environment, and install all dependencies.

```bash
cd backend
python3 -m venv ./env
env/Scripts/activate
pip install -r requirements.txt
```
Next, initialize a local SQLite DB instance by stepping into the ```/api``` directory and executing the following commands in Python interactive mode,

```bash
cd api
python3
```
now from interactive mode,
```python
from app import create_app
from utils.db import db
app = create_app()
with app.app_context():
  db.create_all()
```
this will create a SQLite DB instance named ```database.db``` in the ```/backend/api/instance```. Check that your DB was created correctly by checking that executing the following commands from your terminal,
```bash
cd instance
sqlite3 database.db
sqlite> .tables
```
you should then see ```projects  users``` indicating that both the projects and users tables were created successfully. To populate the projects table, you need to run the ```scripts/database.py``` script while in the ```backend/api```. You should go to the main method located in this script and make sure it contains,
```python
with app.app_context():
  pop_projects_from_json()
```
this will populate the database with the projects stored in ```small_repo_data.json```, but you can also pass in the name of another JSON file which contains more projects. You can run,
```python
with app.app_context():
  pop_projects_from_json("static_repo_data.json")
```
which has many more projects to populate the database with.
