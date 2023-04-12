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
		job_from_db = jobaiDB.jobs.find_one({"_id": ObjectId(self.id)})

		if not job_from_db["shortListing"]:
			job_from_db["shortListing"] = AnsweringEngine.summarize_Job_Description(job_from_db["longListing"])
			self.update_short_listing(job_from_db["shortListing"])


		try:
			company = JobSchema.Company (
				name = job_from_db['company']
			)

			job = JobSchema.Job (
				id = str(job_from_db['_id']),
				role = job_from_db['jobTitle'],
				source = job_from_db['source'],
				ext_ID = job_from_db['exid'],
				company = company,
				longListing = job_from_db['longListing'],
				short_description = job_from_db.get('shortListing'),
				questions = job_from_db['questions'],
				added_ts = 0,
				last_updated_ts = 0,
				created_ts = 0,
				location = "Hell",
				role_category = "Software",
				skills = ["python", "Netscape Navigator"],
				status = JobSchema.Status.ACTIVE
			)
		except ValidationError as e:
			job = e.errors()


		return job

	def apply_to_role(self, questionResponses):
		return 

	def update_short_listing(self, newShortListing):
		from api import jobaiDB
		update_response = jobaiDB.jobs.update_one({"_id":ObjectId(self.id)}, {"$set": {"shortListing":newShortListing}}, upsert=True)
		return
	
	def mark_role_as_read(self, user: User, favourite: bool):
		from api import jobaiDB
		jobaiDB.user_jobs.update_one(
			{
				"job_id":ObjectId(self.id),
				"user_id":ObjectId(user.user_id),
			}, {
				"$set": {
					"read": True,
					"favourite": favourite
				}
			}, upsert=True)
		return
	
class Question:
	def __init__(self):
		pass