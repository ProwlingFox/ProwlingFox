from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from components import authentication
from components.user import User
from components.job import Job
from components.answeringEngine import AnsweringEngine

router = APIRouter(tags=["AI"])

class get_ai_response(BaseModel):
	jobID: str
	questionID: str

# Get AI Generated Responses for a specific question.
@router.post("/ai/respond")
@authentication.access_level("Candidate")
def get_ai_response(req: Request, r: get_ai_response):
	u = User(req.state.user_id)
	j = Job(r.jobID)
	return AnsweringEngine.answer_question(j, u, r.questionID)