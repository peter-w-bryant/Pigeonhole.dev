from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash

from sqlalchemy import create_engine, asc, desc, func, distinct
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.serializer import loads, dumps

# from database_setup import Base, Things

import random
import string
import logging
import json
import httplib2
import requests
import mysql.connector



import config
from github import GitHubAPI

app = Flask(__name__)

conn = mysql.connector.connect(
                        user=config.db_user,
                        password=config.db_password,
                        host=config.db_host,
                        database=config.db_database,
                        charset='utf8mb4'
                    )
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

@app.route('/all-projects', methods=['GET', 'POST'])
def AllProjectData():
    return "test"

@app.route('/project/<pUID>', methods=['GET', 'POST'])
def SingleProjectData(pUID):
    github = GitHubAPI('up-for-grabs', 'up-for-grabs.net')
    print(github.get_stargazers_count())
    return str(github.get_stargazers_count())

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
