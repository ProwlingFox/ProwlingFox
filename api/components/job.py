from pymongo import errors as Mongoerrors
from bson.objectid import ObjectId


from components.user import User
from components.schemas.job import *

class Job:
	def __init__(self, job_id):
		self.id = job_id
		return

	def get_details(self):
		from api import jobaiDB
		job_from_db = jobaiDB.jobs.find_one({"_id": ObjectId(self.job_id)})
	
		job = Job( {
			"job_id": str(job_from_db['_id']),
			"jobTitle": job_from_db['jobTitle'],
			"company": job_from_db['company'],
			"longListing": job_from_db['longListing'],
			"shortListing": job_from_db.get('shortListing'),
			"questions": job_from_db['questions']
		} )

		return job

	def apply_to_role(self, questionResponses):
		return 

	def update_short_listing(self, newShortListing):
		from api import jobaiDB
		update_response = jobaiDB.jobs.update_one({"_id":ObjectId(self.job_id)}, {"$set": {"shortListing":newShortListing}}, upsert=True)
		return
	
	def mark_role_as_read(self, user: User, favourite: bool):
		from api import jobaiDB
		jobaiDB.user_jobs.update_one(
			{
				"job_id":ObjectId(self.job_id),
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