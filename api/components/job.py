from pymongo import errors as Mongoerrors
from bson.objectid import ObjectId


class Job:
	def __init__(self, job_id):
		self.job_id = job_id
		return

	def get_details(self):
		from api import jobaiDB
		job_from_db = jobaiDB.jobs.find_one({"_id": ObjectId(self.job_id)}, limit=10)
	
		job = {
			"job_id": str(job_from_db['_id']),
			"jobTitle": job_from_db['jobTitle'],
			"company": job_from_db['company'],
			"longListing": job_from_db['longListing'],
			"questions": job_from_db['questions']
		}

		return {'success': True, 'data': job}

	def apply_to_role(self, questionResponses):
		return
