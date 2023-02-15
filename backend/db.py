import mysql.connector
import config

class DB:
    def __init__(self):
        self.conn = mysql.connector.connect(
                        user=config.db_user,
                        password=config.db_password,
                        host=config.db_host,
                        database=config.db_database,
                        charset='utf8mb4'
                    )
        self.cursor = self.conn.cursor()

    def __exit__(self):
        self.cursor.close()
        self.conn.close() 

    def insert(self, query, args=None):
        self.cursor.execute(query, args)
        self.conn.commit() 

    def rollback(self):
        self.conn.rollback()

    def fetchall(self, table_name):
        self.cursor.execute("SELECT * FROM " + table_name)
        all_projects = self.cursor.fetchall()
        all_projects_dict = {}
        for project in all_projects:
            single_project_dict = {}
            single_project_dict["pUID"] = project[0]
            single_project_dict["gh_repo_name"]= project[1]
            single_project_dict["gh_description"]= project[2]
            single_project_dict["gh_rep_url"]= project[3]
            single_project_dict["num_stars"]= project[4]
            single_project_dict["num_forks"]= project[5]
            single_project_dict["num_watchers"]=project[6]
            single_project_dict["issue_label_1"]= project[7]
            single_project_dict["issue_label_2"]= project[8]
            single_project_dict["issue_label_3"]= project[9]
            single_project_dict["gh_username"]= project[10]
            single_project_dict["date_last_merged_PR"]: project[11]
            single_project_dict["date_last_commit"]= project[12]
            single_project_dict["image"]= project[13]
            single_project_dict["gh_topics_0"]= project[14]
            single_project_dict["gh_topics_1"]= project[15]
            single_project_dict["gh_topics_2"]= project[16]
            single_project_dict["gh_topics_3"]= project[17]
            single_project_dict["gh_topics_4"]= project[18]
            single_project_dict["gh_topics_5"]= project[19]
            all_projects_dict[single_project_dict["gh_repo_name"]] = single_project_dict

        return all_projects_dict