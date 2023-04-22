from email.policy import strict
from fastapi import HTTPException
from pymongo import errors as Mongoerrors
from bson.objectid import ObjectId
from pydantic import ValidationError

import asyncio
from components.user import User
import components.schemas.job as JobSchema
from components.answeringEngine import AnsweringEngine

class Job:
	def __init__(self, job_id: str | ObjectId):
		self.id = ObjectId(job_id) if type(job_id) is str else job_id
		return

	def get_details(self) -> JobSchema.Job:
		from api import jobaiDB

		
		job_from_db = jobaiDB.jobs.find_one({"_id": self.id})
		job = JobSchema.Job.parse_obj(job_from_db)

		if not job.short_description:
			job.short_description = AnsweringEngine.summarize_Job_Description(job.long_description)
			self.update_short_listing(job.short_description)

		return job

	def apply_to_role(self, questionResponses):
		print(questionResponses)
		# Validate Responses
		
		# Save Application To DB
		
		return 

	def update_short_listing(self, newShortListing):
		from api import jobaiDB
		update_response = jobaiDB.jobs.update_one({"_id":self.id}, {"$set": {"short_description":newShortListing}}, upsert=True)
		return

	def mark_role_as_read(self, user: User, requestApply: bool = False):
		from api import jobaiDB
		jobaiDB.applications.update_one(
			{
				"job_id":self.id,
				"user_id":ObjectId(user.user_id),
				"application_processing": False,
				"application_processed": False,
				"application_sent": False
			}, {
				"$set": {
					"application_read": True,
					"application_requested": requestApply,
				}
			}, upsert=True)
		return True
	
	