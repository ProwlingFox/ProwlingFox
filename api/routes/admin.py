from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from components import authentication

from components.metrics import metrics

router = APIRouter(tags=["Admin"])

#Question Types

# class responses(BaseModel):
# 	string: str = None
# 	boolean: str = None
# 	integer: str = None
# 	decimal: str = None
# 	multiple_choice: str = None

# class questionType(BaseModel):
# 	title: str
# 	key_words: List[str]
# 	response: responses


# Get Specific Job Details
@router.get("/admin/metrics")
@authentication.access_level("Admin")
def active_jobs_metric():
	return {
		"activeJobsCount": metrics.count_active_jobs(),
		"userCount": metrics.count_users(),
		"jobApplicationCount": metrics.count_applications()
	}

# Get Specific Job Details
@router.get("/admin/questionTypes")
@authentication.access_level("Admin")
def get_question_types():
	return None

# Create New Question Type
@router.post("/admin/questionTypes")
@authentication.access_level("Admin")
def create_question_type():
	return None


# Update Question Type Response and Keywords
@router.put("/admin/questionTypes")
@authentication.access_level("Admin")
def update_question_type():
	return None
