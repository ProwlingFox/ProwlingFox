from pydantic import BaseModel
from typing import List, Any, Optional

from schemas.job import JobSimplified

class get_job_reccomendations_return(BaseModel):
	jobs: List[JobSimplified]
	totalJobs: int