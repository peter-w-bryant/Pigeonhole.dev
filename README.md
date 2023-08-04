# pigeonhole.dev
An enriched Dockerized GitHub API proxy for open-source project discovery built with Flask and Azure Postgres Database. Deployed with Azure Container Instances and load tested with k6. 

# Table of Contents
1. [Usage](#Usage)

## Usage
Create a SQLite DB instance by stepping into the ```/api``` directory and executing the following commands in Python interactive mode,

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