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
        return self.cursor.fetchall()