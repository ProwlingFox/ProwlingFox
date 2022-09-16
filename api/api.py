import pymongo

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
from routes import user

import components.secrets as secrets
secrets.init()


#Create DB Connection
mClient = pymongo.MongoClient(secrets.secrets["database"]["credentials"])
jobaiDB = mClient.jobai

try:
	print("Testing DB Connection")
	mClient.admin.command('ping')
except pymongo.errors.ConnectionFailure:
	raise Exception("DB Server Cannot Connect")

app = FastAPI()
app.include_router(user.router)