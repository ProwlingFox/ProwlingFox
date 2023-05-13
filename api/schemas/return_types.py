from pydantic import BaseModel
from typing import List

from schemas.job import JobSimplified

class get_job_reccomendations_return(BaseModel):
	jobs: List[JobSimplified]
	totalJobs: int