import logging
from pymongo import MongoClient, database, errors
from time import sleep

class ProwlingFoxDB(database.Database):
    def __init__(self):
        from components.secrets import secrets

        while True:
            #Create DB Connection
            mongo_client = MongoClient(secrets["DB_URI"])
            try:
                logging.info("Testing DB Connection")
                mongo_client.admin.command('ping')
                logging.info("DB Connected 🙂")
                break
            except errors.ConnectionFailure:
                logging.warning("DB Server Cannot Connect, Retrying...")
                sleep(4)
        
        super().__init__(mongo_client, secrets["DB_NAME"])
        return

        

prowling_fox_db = ProwlingFoxDB()