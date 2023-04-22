import pymongo
from time import sleep
import components.secrets as secrets

jobaiDB = None

def init():
    while True:
        #Create DB Connection
        mClient = pymongo.MongoClient(secrets.secrets["database"]["credentials"])
        global jobaiDB
        jobaiDB = mClient.jobai
        try:
            print("Testing DB Connection")
            mClient.admin.command('ping')
            print("DB Connected 🙂")
            return
        except pymongo.errors.ConnectionFailure:
            print("DB Server Cannot Connect, Retrying...")
            sleep(4)