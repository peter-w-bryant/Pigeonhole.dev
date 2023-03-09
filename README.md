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
> from app import create_app
> from utils.db import db
> app = create_app()
> with app.app_context():
>    db.create_all()
```
this will create a SQLite DB instance named ```database.db``` in the ```/backend/api/instance```. Check that your DB was created correctly by checking that the executing the following commands from your terminal,
```bash
cd instance
sqlite3 database.db
sqlite> .tables
```
you should then see ```projects  users``` indicating that both the projects and users tables were created successfully. 
