from pprint import pprint
import components.secrets as secrets
import components.schemas.job as JobSchema
from components.answeringEngine import AnsweringEngine
from bson.objectid import ObjectId

secrets.init()

import components.db as db
db.init()
jobaiDB = db.jobaiDB

job_from_db = jobaiDB.jobs.find_one({"short_description": None})
job = JobSchema.Job.parse_obj(job_from_db)

job.short_description = AnsweringEngine.summarize_Job_Description(job.long_description)
self.update_short_listing(job.short_description)

pprint(job_from_db)