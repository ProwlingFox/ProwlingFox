from fastapi import APIRouter
from components.user import User
from components.authentication import access_level

from components.metrics import metrics

router = APIRouter(tags=["Admin"])

# Get Specific Job Details
@router.get("/admin/metrics")
@access_level("Admin")
def active_jobs_metric():
	return {
		"activeJobsCount": metrics.count_active_jobs(),
		"processedJobsCount": metrics.count_processed_jobs(),
		"userCount": metrics.count_users(),
		"jobApplicationCount": metrics.count_applications(),
		"averageAIQuestionsPerJob": metrics.get_average_questions(),
		"openAIUsage": metrics.get_openAI_usage(),
	}

@router.get("/admin/users")
@access_level("Admin")
def get_users():
	return User.get_user_list()
