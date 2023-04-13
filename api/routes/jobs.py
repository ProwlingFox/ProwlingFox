from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from components import authentication

from components.user import User
from components.job import Job

router = APIRouter(tags=["Jobs"])

# Get Summary Of Reccomended Jobs
@router.get("/jobs")
@authentication.access_level("Candidate")
def get_job_reccomendations(req: Request):
	u = User(req.state.user_id)
	return u.get_job_reccomendations()


# Get Specific Job Details
@router.get("/jobs/{job_id}")
@authentication.access_level("Candidate")
def get_job_details(job_id: str):
	j = Job(job_id)
	return j.get_details()


# Mark A Job As Read
class mark_as_read(BaseModel):
	favourite: bool

@router.get("/jobs/{job_id}/mark")
@authentication.access_level("Candidate")
def mark_as_read(req: Request, job_id: str, m: mark_as_read):
	u = User(req.state.user_id)
	j = Job(job_id)
	return j.mark_role_as_read(u, m.favourite)


# Apply To A Job
@router.get("/jobs/{job_id}/apply")
@authentication.access_level("Candidate")
def get_job_details(job_id: str):
	j = Job(job_id)
	return j.get_details()
