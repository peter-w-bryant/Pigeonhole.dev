from flask_login import UserMixin
from utils.db import db
from utils.auth import bcrypt

class Projects(db.Model):
    __tablename__ = 'projects'
    pUID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    gh_repo_name = db.Column(db.String(100), nullable=False)
    gh_description = db.Column(db.String(300), nullable=False)
    gh_repo_url = db.Column(db.String(150), nullable=False)
    num_stars = db.Column(db.Integer, nullable=False)
    num_forks = db.Column(db.Integer, nullable=False)
    num_watchers = db.Column(db.Integer, nullable=False)
    # issue_label_1 = db.Column(db.String(45), nullable=True)
    # issue_label_2 = db.Column(db.String(45), nullable=True)
    # issue_label_3 = db.Column(db.String(45), nullable=True)
    # issue_label_4 = db.Column(db.String(45), nullable=True)
    # issue_label_5 = db.Column(db.String(45), nullable=True)
    # issue_label_6 = db.Column(db.String(45), nullable=True)
    # issue_label_7 = db.Column(db.String(45), nullable=True)
    # issue_label_1_count = db.Column(db.Integer, nullable=True)
    # issue_label_2_count = db.Column(db.Integer, nullable=True)
    # issue_label_3_count = db.Column(db.Integer, nullable=True)
    # issue_label_4_count = db.Column(db.Integer, nullable=True)
    # issue_label_5_count = db.Column(db.Integer, nullable=True)
    # issue_label_6_count = db.Column(db.Integer, nullable=True)
    # issue_label_7_count = db.Column(db.Integer, nullable=True)
    gh_username = db.Column(db.String(100), nullable=False)
    date_last_merged_PR = db.Column(db.String(45), nullable=False)
    date_last_commit = db.Column(db.String(45), nullable=False)
    # gh_topics0 = db.Column(db.String(30), nullable=True)
    # gh_topics1 = db.Column(db.String(30), nullable=True)
    # gh_topics2 = db.Column(db.String(30), nullable=True)
    # gh_topics3 = db.Column(db.String(30), nullable=True)
    # gh_topics4 = db.Column(db.String(30), nullable=True)
    # gh_topics5 = db.Column(db.String(30), nullable=True)
    contrib_url = db.Column(db.String(150), nullable=False)
    new_contrib_score = db.Column(db.Float, nullable=False)

    def __str__(self):
        return f"Project('{self.pUID}', '{self.gh_repo_name}', '{self.gh_repo_url}')"
    
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
    email = db.Column(db.String(50), unique=True)

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

class SavedProjects(db.Model):
    __tablename__ = 'saved_projects'
    spUID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    UID = db.Column(db.Integer, db.ForeignKey('users.UID'), nullable=False)
    pUID = db.Column(db.Integer, db.ForeignKey('projects.pUID'), nullable=False)
