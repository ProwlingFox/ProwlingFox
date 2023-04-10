from anyio import sleep_forever
import components.secrets as secrets
secrets.init()

import pymongo
from time import sleep

while True:
    #Create DB Connection
    mClient = pymongo.MongoClient(secrets.secrets["database"]["credentials"])
    jobaiDB = mClient.jobai
    try:
        print("Testing DB Connection")
        mClient.admin.command('ping')
        break
    except pymongo.errors.ConnectionFailure:
        print("DB Server Cannot Connect, Retrying...")
        sleep(4)


# FAST API

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from routes import user, jobs, admin, ai

app = FastAPI()

# Middleware to allow working on multiple points, needs adjusted for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(jobs.router)
app.include_router(admin.router)
app.include_router(ai.router)

@app.get("/")
def api_info():
	return {"success": True, "message": "Job.ai API is running"}