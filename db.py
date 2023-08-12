import mysql.connector
import os
import logging

class database:
    def __init__(self):
        try:
            USER = os.getenv('SQL_USER')
            PASSWORD = os.getenv('SQL_PASSWORD')
            HOST = os.getenv('SQL_HOST')
            PORT = os.getenv('SQL_PORT')
        except:
            print("Could not access env vars")
            return "Internal Server Error"
    
        db = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            port=PORT,
            database="notenote"
        )
        db.autocommit = True
        self.db = db
    
    def execute(self, query, params, expectoutput=True):
        cursor = self.db.cursor()
        logging.info("STARTING QUERY")
        cursor.execute(query, params)
        if expectoutput:
            results = cursor.fetchall() #VERY INNEFICIENT LOADS EVERYTHING INTO MEMORY
            logging.info("QUERY RESULT")
            logging.info(results)
            return results
        else:
            return cursor.rowcount
    
    def get_random(self, num_random):
        cursor = self.db.cursor()
        cursor.execute(("SELECT * FROM author WHERE author_name IS NOT NULL ORDER BY rand() LIMIT %s"), [num_random])
        results = cursor.fetchall()
        return results
