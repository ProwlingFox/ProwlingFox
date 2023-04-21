import asyncio
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from components.authentication import access_level

import components.schemas.job as JobSchema

from components.user import User
from components.job import Job

router = APIRouter(tags=["Jobs"])

# Get Summary Of Reccomended Jobs
@router.get("/jobs")
@access_level("Candidate")
def get_job_reccomendations(req: Request) -> List[JobSchema.JobSimplified]:
	u = User(req.state.user_id)
	return u.get_job_reccomendations()


# Get Specific Job Details
@router.get("/jobs/{job_id}")
@access_level("Candidate")
def get_job_details(job_id: str) -> JobSchema.Job:
	j = Job(job_id)
	return j.get_details()


# Mark A Job As Read
class mark_as_read(BaseModel):
	requestApply: bool
	

@router.post("/jobs/{job_id}/mark")
@access_level("Candidate")
def mark_as_read(req: Request, job_id: str, m: mark_as_read):
	u = User(req.state.user_id)
	j = Job(job_id)
	return j.mark_role_as_read(u, m.requestApply)
	# j.testBasic() 


# Apply To A Job
class Response(BaseModel):
    id: str
    response: Any
    
class apply_to_job(BaseModel):
	responses: List[Response]

@router.post("/jobs/{job_id}/apply")
@access_level("Candidate")
def get_job_details(job_id: str, a: apply_to_job):
	j = Job(job_id)
	return j.apply_to_role(a.responses)
