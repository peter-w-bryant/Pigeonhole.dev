# pigeonhole.dev
An aggregated list of open source projects with issues looking for contributors.

## Usage
### Cloning repo & Installing Dependencies
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
### Populating the Database
Populate the DB with an single public repository's information by passing the public GitHub URL to the `pop_project()` function defined in the `DB` class,
```{python3}
with DB() as db:
  db.pop_project('https://github.com/GITHUB-USERNAME/REPO-NAME')
```
Alternatively, populate the DB with a collection of repositories that are stored in `static_repo_data.json` by running the `pop_projects_from_json()` function defined in the `DB` class,
```{python3}
with DB() as db:
  db.pop_projects_from_json()
```
Example of `static_repo_data.json`:
```{json}
{
    "flask": "https://github.com/pallets/flask",
    "up_for_grabs": "https://github.com/up-for-grabs/up-for-grabs.net",
    "pytorch": "https://github.com/pytorch/pytorch",
    "huggingface_datasets": "https://github.com/huggingface/datasets",
    "fastapi": "https://github.com/huggingface/datasets",
    "s2n_tls" : "https://github.com/aws/s2n-tls",
    "tensorflow": "https://github.com/tensorflow/tensorflow",
    "go_ethereum": "https://github.com/ethereum/go-ethereum",
    "node_js": "https://github.com/nodejs/node",
    "kubernetes": "https://github.com/kubernetes/kubernetes",
    "julia": "https://github.com/JuliaLang/julia",
    "rust": "https://github.com/rust-lang/rust",
    "pandas": "https://github.com/pandas-dev/pandas",
    "cyprus": "https://github.com/cypress-io/cypress",
    "mastodon": "https://github.com/mastodon/mastodon",
    "typescript": "https://github.com/microsoft/TypeScript",
    "vscode": "https://github.com/microsoft/vscode"
}
```
