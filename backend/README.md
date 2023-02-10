# pigeonhole.dev
An aggregated list of open source projects with issues looking for contributors.

## Usage
First clone this repo,
```{bash}
git clone https://github.com/peter-w-bryant/pigeonhole.dev.git
```
then enter the `pigeonhole.dev/backend` directory, create a virtual environment, activate it, and install all dependencies,
```{bash}
cd pigeonhole.dev/backend
python3 -m venv ./env
env/Scripts/activate
pip3 install -r requirements.txt
```
Populate the DB with an single public repository's information by passing the public GitHub URL to the `pop_project()` function defined in the `PopulateDB` class,
```{python3}
repo = 'https://github.com/pallets/flask'
pop = PopulateDB()
pop.pop_project(repo)
```
Alternatively, populate the DB with a collection of repositories that are stored in `static_repo_data.json` by running the `init_db.py` script.
```{python3}
python3 init_db.py
```
