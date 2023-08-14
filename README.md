# Pigeonhole.dev
An aggregated list of open source projects with issues looking for contributors.

# Table of Contents
1. [Usage](#Usage)

## Pigeonhole.dev API v1.0.0
### Run the API server locally
#### Create a local SQLite DB instance
The backend requires access to a private Azure PostgreSQL DB instance, so in order to run the API server locally I recommend creating a local SQLite DB instance, and adding the following to the ```/api/config.py``` file,
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/database.db'
```
and commenting out the following line,
```python
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
```

Initialize a local SQLite DB instance by stepping into the ```/api``` directory and executing the following commands in Python interactive mode,

```python
from app import create_app
from utils.db import db
app = create_app()
with app.app_context():
  db.create_all()
```
We have provided a script to populate the DB with data from static JSON files. Run the following commands from the ```/api``` directory to populate the DB with sample data,

```python
<replace>
```

#### Create a Docker image and run the image in a container
Run the API server locally by cloning the repo, creating a Docker image and running the image in a container.

```bash
git clone https://github.com/peter-w-bryant/pigeonhole.dev.git
cd pigeonhole.dev
docker build -t ph .
docker run -p 5000:5000 ph
```

#### API Documentation
Access the API documentation at ```http://localhost:5000/api/v1.0/apidocs```.
