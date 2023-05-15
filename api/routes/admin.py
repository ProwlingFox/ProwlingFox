from fastapi import APIRouter
from components import authentication

from components.metrics import metrics

router = APIRouter(tags=["Admin"])

# Get Specific Job Details
@router.get("/admin/metrics")
@authentication.access_level("Admin")
def active_jobs_metric():
	return {
		"activeJobsCount": metrics.count_active_jobs(),
		"processedJobsCount": metrics.count_processed_jobs(),
		"userCount": metrics.count_users(),
		"jobApplicationCount": metrics.count_applications()
	}
