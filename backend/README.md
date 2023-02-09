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
Populate the DB by passing the public URL of any GitHub repository in the main function of `pop_db.py`,
```{python3}
repo = 'https://github.com/pallets/flask'
pop = PopulateDB()
pop.pop_project(repo)
```
