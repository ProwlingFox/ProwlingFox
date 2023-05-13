from components.secrets import secrets
from components.db import prowling_fox_db as jobaiDB
# FAST API

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import user, jobs, admin

if secrets["DEVELOPMENT"] == "TRUE":
    app = FastAPI(
        title="ProwlingFox (DEV)",
        version="0.1.0",
        debug= True,
    )
else:
    app = FastAPI(
        title="ProwlingFox",
        version="0.1.0",
        debug= False,
        docs_url=None,
        redoc_url=None
    )

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

@app.get("/")
def api_info():
	return {"success": True, "message": "ProwlingFox API is running"}