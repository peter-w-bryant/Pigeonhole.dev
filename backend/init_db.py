import time
import json
from pop_db import PopulateDB
from _mysql_connector import MySQLInterfaceError

def InitDB():
    repo_data = json.load(open('static_repo_data.json', 'r')) 
    pop = PopulateDB()
    success_count = 0
    try:
        for repo_url in repo_data.values():
            pop.pop_project(repo_url)            
            success_count += 1
    except MySQLInterfaceError as e:
        print("MySQLInterfaceError occured when inserting:", repo_url)
        pass  
    return success_count 

if __name__ == '__main__':
    start = time.time()
    success_count = InitDB()
    end = time.time()
    print(success_count, "repos added to DB in", end-start, "seconds.")