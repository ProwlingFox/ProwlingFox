import io
from typing import Any
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from components.authentication import access_level

import schemas.job as JobSchema
from components.user import User


router = APIRouter(tags=["Applications"])

@router.get("/applications")
@access_level("Authenticated")
def get_user_applications(req: Request, showSent: bool = False):
	u = User(req.state.user_id)
	return u.get_applications(showSent)

@router.get("/applications/{job_id}")
@access_level("Authenticated")
def get_user_applications(req: Request, job_id: str):
	u = User(req.state.user_id)
	return u.get_application(job_id)

# Export Applications as File
@router.get("/applications/export", response_class=StreamingResponse)
@access_level("Authenticated")
def export_applications(req: Request):
	u = User(req.state.user_id)
	stream = io.StringIO(u.export_applications_as_csv())
	response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
	response.headers["Content-Disposition"] = "attachment; filename=Applications.csv"
	return response

# Update Application State
# Login User Using Password
class application_state(BaseModel):
	state: int

@router.post("/applications/{job_id}/setstate")
@access_level("Authenticated")
def update_application_state(req: Request, job_id: str, s: application_state):
	u = User(req.state.user_id)
	return u.set_application_state(job_id, s.state)