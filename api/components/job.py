from email.policy import strict
import re
from urllib import response
from fastapi import HTTPException
from pymongo import errors as Mongoerrors
from bson.objectid import ObjectId
from pydantic import ValidationError

import asyncio
from components.user import User
import components.schemas.job as JobSchema
from components.answeringEngine import AnsweringEngine

class Job:
	job_data: JobSchema.Job = None

	def __init__(self, job_id: str | ObjectId):
		self.id = ObjectId(job_id) if type(job_id) is str else job_id
		return

	def preprocess_job(self):
		job = self.get_details()

		if job.short_description:
			print("It looks like this job has allready been processed. JobID:", self.id)

		prompt_vars =  {"full_description": job.long_description}

		prompt = AnsweringEngine.promptGenerator("summarizeJobDescription", prompt_vars)
		job.short_description = AnsweringEngine.sendSimpleChatPrompt(prompt, "summarizeJobDescription", tokens = 300)

		prompt = AnsweringEngine.promptGenerator("shortRoleSummary", prompt_vars)
		job.role_description = AnsweringEngine.sendSimpleChatPrompt(prompt, "shortRoleSummary", tokens = 100)

		# Needs converted to an array of strings
		prompt = AnsweringEngine.promptGenerator("roleRequirements", prompt_vars)
		response = AnsweringEngine.sendSimpleChatPrompt(prompt, "roleRequirements", tokens = 300)
		job.requirements = []
		for bullet_point in response.splitlines():
			job.requirements.append(bullet_point.removeprefix("- "))
		
		# Needs converted to an array of strings
		prompt = AnsweringEngine.promptGenerator("roleKeyPoints", prompt_vars)
		response = AnsweringEngine.sendSimpleChatPrompt(prompt, "roleKeyPoints", tokens = 300)
		job.key_points = []
		for bullet_point in response.splitlines():
			job.key_points.append(bullet_point.removeprefix("- "))
		


		self.upsert_job({
			"short_description": job.short_description,
			"role_description": job.role_description,
			"requirements": job.requirements,
			"key_points": job.key_points,
			"job_processing": False
		})
		return

	def preprocess_questions(self, question):


		return

	def get_details(self) -> JobSchema.Job:
		if self.job_data:
			return self.job_data
		
		from api import jobaiDB
		
		job_from_db = jobaiDB.jobs.find_one({"_id": self.id})
		job = JobSchema.Job.parse_obj(job_from_db)
		self.job_data = job

		return job

	def apply_to_role(self, questionResponses):
		print(questionResponses)
		# Validate Responses
		
		# Save Application To DB
		
		return 

	def upsert_job(self, fieldsToUpdate):
		from api import jobaiDB
		update_response = jobaiDB.jobs.update_one(
			{"_id":self.id}, 
			{"$set": fieldsToUpdate}
		, upsert=True)
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
	
	