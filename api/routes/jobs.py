from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from components import authentication

from components.user import User

router = APIRouter(tags=["Jobs"])

# Get Jobs
@router.get("/jobs")
@authentication.access_level("Candidate")
def get_job_reccomendations(req: Request):
	u = User(req.state.user_id)
	return u.get_job_reccomendations()