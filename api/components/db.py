from pymongo import MongoClient, database, errors
from time import sleep

class ProwlingFoxDB(database.Database):
    def __init__(self, db_name):
        from components.secrets import secrets

        while True:
            #Create DB Connection
            mongo_client = MongoClient(secrets["database"]["credentials"])
            try:
                print("Testing DB Connection")
                mongo_client.admin.command('ping')
                print("DB Connected 🙂")
                break
            except errors.ConnectionFailure:
                print("DB Server Cannot Connect, Retrying...")
                sleep(4)
        
        super().__init__(mongo_client, db_name)
        return

        

prowling_fox_db = ProwlingFoxDB("jobai")