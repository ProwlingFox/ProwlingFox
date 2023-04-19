from pymongo import errors as Mongoerrors
from bson.objectid import ObjectId
from pydantic import ValidationError

from components.user import User
import components.schemas.job as JobSchema
from components.answeringEngine import AnsweringEngine

class Job:
	def __init__(self, job_id):
		self.id = job_id
		return

	def get_details(self):
		from api import jobaiDB

		try:
			job_from_db = jobaiDB.jobs.find_one({"_id": ObjectId(self.id)})
			job = JobSchema.Job.parse_obj(job_from_db)
			
			job.id = str(job_from_db["_id"])

			if not job.short_description:
				job.short_description = AnsweringEngine.summarize_Job_Description(job.long_description)
				self.update_short_listing(job.short_description)

		except ValidationError as e:
			job = e.errors()

		return job

	def apply_to_role(self, questionResponses):
		print(questionResponses)
		# Validate Responses
		
		# Save Application To DB
		
		return 

	def update_short_listing(self, newShortListing):
		from api import jobaiDB
		update_response = jobaiDB.jobs.update_one({"_id":ObjectId(self.id)}, {"$set": {"short_description":newShortListing}}, upsert=True)
		return
	
	def mark_role_as_read(self, user: User, requestApply: bool = False):
		from api import jobaiDB
		jobaiDB.applications.update_one(
			{
				"job_id":ObjectId(self.id),
				"user_id":ObjectId(user.user_id),
			}, {
				"$set": {
					"read": True,
					"requestApply": requestApply
				}
			}, upsert=True)
		return True
	
class Question:
	def __init__(self):
		pass