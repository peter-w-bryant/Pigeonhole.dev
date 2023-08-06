from flask_login import UserMixin
from utils.db import db
from utils.auth import bcrypt

class Projects(db.Model):
    __tablename__ = 'projects'
    pUID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    UID = db.Column(db.Integer, db.ForeignKey('users.UID'), nullable=False) # foreign key for which user added the project
    gh_repo_url = db.Column(db.String(150), nullable=False)
    gh_repo_name = db.Column(db.String(100), nullable=False)
    gh_username = db.Column(db.String(100), nullable=False)
    gh_description = db.Column(db.String(300), nullable=True)

    # project stats
    num_stars = db.Column(db.Integer, nullable=False)
    num_forks = db.Column(db.Integer, nullable=False)
    num_watchers = db.Column(db.Integer, nullable=False)

    # project activity
    date_last_merged_PR = db.Column(db.String(45), nullable=False)
    date_last_commit = db.Column(db.String(45), nullable=False)

    # project contributors
    contrib_url = db.Column(db.String(150), nullable=True)
    new_contrib_score = db.Column(db.Float, nullable=True)

    def to_dict(self):
        return {
            'pUID': self.pUID,
            'UID': self.UID,
            'gh_repo_url': self.gh_repo_url,
            'gh_repo_name': self.gh_repo_name,
            'gh_username': self.gh_username,
            'gh_description': self.gh_description,
            'num_stars': self.num_stars,
            'num_forks': self.num_forks,
            'num_watchers': self.num_watchers,
            'date_last_merged_PR': self.date_last_merged_PR,
            'date_last_commit': self.date_last_commit,
            'contrib_url': self.contrib_url,
            'new_contrib_score': self.new_contrib_score
        }
    
    def get_all_projects(self):
        return Projects.query.all()
    
class ProjectIssues(db.Model):
    # project id from projects table
    __tablename__ = 'project_issues'
    piUID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    pUID = db.Column(db.Integer, db.ForeignKey('projects.pUID'), nullable=False)
    issue_label = db.Column(db.String(45), nullable=False)
    issue_label_count = db.Column(db.Integer, nullable=False)

class ProjectTopics(db.Model):
    # project id from projects table
    __tablename__ = 'project_topics'
    ptUID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    pUID = db.Column(db.Integer, db.ForeignKey('projects.pUID'), nullable=False)
    topic = db.Column(db.String(30), nullable=False)

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    UID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_test_account = db.Column(db.Boolean, default=False)

    def __str__(self):
        return f"User('{self.username}', '{self.password}', '{self.email}')"
    
    def get_id(self):
        return self.UID
    
    def check_password(self, password):
        if bcrypt.check_password_hash(self.password, password):
            return True
        return False
    
    def print_all_users():
        for user in Users.query.all():
            print(user)

class AdminSecretKeys(db.Model):
    __tablename__ = 'admin_secret_keys'
    askUID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    hashed_secret_key = db.Column(db.String(50), unique=True, nullable=False)

class SavedProjects(db.Model):
    __tablename__ = 'saved_projects'
    spUID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    UID = db.Column(db.Integer, db.ForeignKey('users.UID'), nullable=False)
    pUID = db.Column(db.Integer, db.ForeignKey('projects.pUID'), nullable=False)
