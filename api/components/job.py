from typing import List
import bson
from bson.objectid import ObjectId

from fastapi import HTTPException
from pydantic import ValidationError

from schemas.configurations import Role
import schemas.job as JobSchema
import schemas.user as UserSchema

from components.user import User
from components.answeringEngine import AnsweringEngine
from components.db import prowling_fox_db

from pprint import pprint

class Job:
	job_data: JobSchema.Job = None

	def __init__(self, job_id: str | ObjectId):
		try:
			self.id = ObjectId(job_id) if type(job_id) is str else job_id
		except bson.errors.InvalidId as e:
			raise HTTPException(status_code=400, detail="MALFOMED_BSON_ID")
		return

	def preprocess_job(self):
		job = self.get_details()

		if job.short_description:
			print("It looks like this job has allready been processed. JobID:", self.id)

		job.questions = self.preprocess_questions(job.questions)

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
			"questions": list(map(lambda x: x.dict(), job.questions)),
			"job_processing": False
		})
		return

	def preprocess_questions(self, questions: List[JobSchema.Question]):
		special_case_fields = ["email"]


		for question in questions:
			# This Allows JobSniffers to prefil questions too
			if question.response:
				print("question allready filled: ", question.id)
				continue

			if question.type == JobSchema.FieldType.TEXT:
				prompt_vars = {
					"question": question.ai_prompt or question.content,
					"available_variables": ",".join(UserSchema.UserDataFields.__fields__.keys()) + "," + ",".join(special_case_fields)
				}
				print("Question:", question.content)
				prompt = AnsweringEngine.promptGenerator("questionPreprocessor", prompt_vars)
				instructions = "You Are Matching Questions To Variables, Do not use more than 5 additional words"
				response = AnsweringEngine.sendSimpleChatPrompt(prompt, "questionPreprocessor",system=instructions,  force_single_line=True, tokens = 10)
				# TODO: Add better code here to validate the response can be parsed
				if "N/A" in response.upper():
					print("Cant Be Substituded")
					continue
				if "{" in response and "}" in response:
					question.response = response
					print("Can Be Substituded with", response)
				continue
		return questions

	def get_details(self) -> JobSchema.Job:
		if self.job_data:
			return self.job_data
				
		job_from_db = prowling_fox_db.jobs.find_one({"_id": self.id})

		if not job_from_db:
			raise HTTPException(status_code=400, detail="JOB_NOT_FOUND")

		try:
			job = JobSchema.Job.parse_obj(job_from_db)
			self.job_data = job
		except ValidationError as e:
			raise HTTPException(status_code=500, detail="JOB_EXISTS_BUT_IS_INVALID")

		return job

	def apply_to_role(self, user: UserSchema.User, raw_question_responses):
		# Validate Responses
		job = self.get_details()
		
		errors = {
			"missingResponse": [],
			"invalidType": []
		}

		question_responses = {}

		for question in job.questions:
			if question.required and (not raw_question_responses[question.id]):
				errors["missingResponse"].append(question.id)

			question_responses["responses." + question.id] = raw_question_responses[question.id]

		question_responses["application_reviewed"] = True

		# Save Application To DB
		prowling_fox_db.applications.update_one({
			"job_id": job.id,
			"user_id": user.user_id
		},{
			"$set": question_responses,
		})
		
		return 

	def upsert_job(self, fieldsToUpdate):
		update_response = prowling_fox_db.jobs.update_one(
			{"_id":self.id}, 
			{"$set": fieldsToUpdate}
		, upsert=True)
		return

	def mark_role_as_read(self, user: User, requestApply: bool = False):
		prowling_fox_db.applications.update_one(
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
	
