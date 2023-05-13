from typing import Any
from fastapi import APIRouter, Request
from pydantic import BaseModel
from components.metrics import metrics
from components.authentication import access_level

import schemas.job as JobSchema

from components.user import User
from components.job import Job

router = APIRouter(tags=["Jobs"])

# Get Summary Of Reccomended Jobs
@router.get("/jobs")
@access_level("Candidate")
def get_job_reccomendations(req: Request):
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


# Apply To A Job

class apply_to_job(BaseModel):
	responses: Any

@router.post("/jobs/{job_id}/apply")
@access_level("Candidate")
def apply_to_job(req: Request, job_id: str, a: apply_to_job):
	j = Job(job_id)
	u = User(req.state.user_id)
	return j.apply_to_role(u, a.responses)

@router.get("/roles")
@access_level("Candidate")
def get_roles():
	return metrics.get_roles()

@router.get("/locations")
@access_level("Candidate")
def get_locations():
	return metrics.get_locations()