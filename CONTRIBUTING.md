-[Running the API server locally](#Running-the-API-server-locally)
	- [Environment Setup](#environment-setup)
	- [Create a local SQLite DB instance](#Create-a-local-SQLite-DB-instance)
	- [Populate the Database with Sample Project Data](#Populate-the-Database-with-Sample-Project-Data)
	- [Modify .demo-env](#Modify-demo-env) 
	- [Create a Docker image and run the image in a container](#Create-a-Docker-image-and-run-the-image-in-a-container)

# Running the API server locally

## Environment Setup
Run the following commands in a bash shell to clone the repository, create a Python virtual environment and install all required dependencies:
```bash
git clone https://github.com/peter-w-bryant/Pigeonhole.dev.git
cd Pigeonhole.dev/backend
python3 -m venv ./env
source env/Scripts/activate
pip install -r requirements.txt
```
## Create a local SQLite DB instance
The deployed backend requires access to a private DB resource; in order to run the API server locally, we recommend creating a local SQLite DB instance at ```Pigeonhole.dev/backend/api```. First, navigate to this directory and open the Python interactive shell,
```bash
cd Pigeonhole.dev/backend/api
python3
```
and within the Python interactive shell, run:
```python
from app import create_app
from utils.db import db
app = create_app()
with app.app_context():
  db.create_all()
```
and then ensure a `database.db` file is created within the `/instance` directory.
## Modify .demo-env
To run this project, you will need to set a number of environment variables. I have provided a file, ```backend/.demo-env```, which contains the following variable definitions,
```
# GitHub OAuth app credentials
GITHUB_CLIENT_ID=''
GITHUB_CLIENT_SECRET=''

# GitHub personal access token with user:email scope
GITHUB_TOKEN=''

# Database URI (default is our local SQLite DB instance)
DATABASE_URI='sqlite:///.db'

# App secret key
SECRET_KEY=''
JWT_SECRET_KEY=''

# Admin credentials for testing
ADMIN_USERNAME=''
ADMIN_PASSWORD=''
```

You should replace these empty strings and rename the file `backend/.demo-env`. Note that `ADMIN_USERNAME` and `ADMIN_PASSWORD` should be the login credentials of a registered admin, these two fields are only required for running unit tests. Our `config.py` file will reference these environment variables, so make sure they are instantiated before running the project.
## Populate the Database with Sample Project Data
We have provided a script to populate the DB with data from static JSON files. Run the following commands from the ```/api``` directory to populate the DB with sample data,

```python
python3 scripts/populate_db.py small
```
You have the option to pass a command line argument of either "small", "medium",  or "large" to populate a different number of projects (the default is the small project list).
#### Create a Docker image and run the image in a container
To start the API server locally, create a Docker image and running the image in a container. Do this by running the following commands in the `Pigeonhole.dev` directory,

```bash
docker build -t ph .
docker run -p 5000:5000 ph
```
You should now have your Flask server running in the container, and you can make request to the API, see https://localhost:5000/apidocs.