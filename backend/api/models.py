from flask_login import UserMixin
from db import db

class Projects(db.Model):
    __tablename__ = 'projects'
    pUID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    gh_repo_name = db.Column(db.String(100), nullable=False)
    gh_description = db.Column(db.String(300), nullable=False)
    gh_repo_url = db.Column(db.String(150), nullable=False)
    num_stars = db.Column(db.Integer, nullable=False)
    num_forks = db.Column(db.Integer, nullable=False)
    num_watchers = db.Column(db.Integer, nullable=False)
    issue_label_1 = db.Column(db.String(45), nullable=False)
    issue_label_2 = db.Column(db.String(45), nullable=False)
    issue_label_3 = db.Column(db.String(45), nullable=False)
    issue_label_4 = db.Column(db.String(45), nullable=False)
    issue_label_5 = db.Column(db.String(45), nullable=False)
    issue_label_6 = db.Column(db.String(45), nullable=False)
    issue_label_7 = db.Column(db.String(45), nullable=False)
    issue_label_1_count = db.Column(db.Integer, nullable=False)
    issue_label_2_count = db.Column(db.Integer, nullable=False)
    issue_label_3_count = db.Column(db.Integer, nullable=False)
    issue_label_4_count = db.Column(db.Integer, nullable=False)
    issue_label_5_count = db.Column(db.Integer, nullable=False)
    issue_label_6_count = db.Column(db.Integer, nullable=False)
    issue_label_7_count = db.Column(db.Integer, nullable=False)
    gh_username = db.Column(db.String(100), nullable=False)
    date_last_merged_PR = db.Column(db.String(45), nullable=False)
    date_last_commit = db.Column(db.String(45), nullable=False)
    gh_topics0 = db.Column(db.String(30), nullable=False)
    gh_topics1 = db.Column(db.String(30), nullable=False)
    gh_topics2 = db.Column(db.String(30), nullable=False)
    gh_topics3 = db.Column(db.String(30), nullable=False)
    gh_topics4 = db.Column(db.String(30), nullable=False)
    gh_topics5 = db.Column(db.String(30), nullable=False)
    contrib_url = db.Column(db.String(150), nullable=False)
    new_contrib_score = db.Column(db.Float, nullable=False)

    def __str__(self):
        return f"Project('{self.pUID}', '{self.gh_repo_name}', '{self.gh_repo_url}')"
    
    def get_all_projects(self):
        return Projects.query.all()

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
    
    def get_all_users(self):
        return Users.query.all()