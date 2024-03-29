import datetime
import logging
import re
from typing import List
import bson
from bson.objectid import ObjectId

from fastapi import HTTPException
from pydantic import ValidationError
from schemas.job import ApplicationStatus

import schemas.job as JobSchema
import schemas.user as UserSchema

from components.user import User
from components.answeringEngine import AnsweringEngine
from components.db import prowling_fox_db


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

		job.questions = self.preprocess_questions(job.questions)

		# This Is An Ugly Hack But it rlly needs to be capped (Approx Caps to 2000 tokens)
		prompt_vars =  {"full_description": job.long_description[:8000]}

		if (not job.short_description):
			prompt = AnsweringEngine.promptGenerator("summarizeJobDescription", prompt_vars)
			job.short_description = AnsweringEngine.sendSimpleChatPrompt(prompt, "summarizeJobDescription", tokens = 300)

		prompt = AnsweringEngine.promptGenerator("multiPreprocess", prompt_vars)

		job.requirements = []
		job.key_points = []

		# Attempts to preprocess a bunch of these
		answers = AnsweringEngine.sendSimpleChatPrompt(prompt, "multiPreprocess", tokens = 300)
		if answers:
			logging.info(answers)
			answers: List[str] = re.split("\d\. ", answers)
			# Remove trailing blank if exists
			if answers[0].strip() == "":
				answers.pop(0)
			logging.info(answers)

			job.role_description = answers[0].strip()
			for bullet_point in answers[1].splitlines():
				if len(bullet_point) > 5: # Basic Garbage Check
					job.requirements.append(bullet_point.removeprefix("- "))
			for bullet_point in answers[2].splitlines():
				if len(bullet_point) > 5: # Basic Garbage Check
					job.key_points.append(bullet_point.removeprefix("- "))
			

		if (not job.role_description):
			logging.info("Had To Regen Role Description")
			prompt = AnsweringEngine.promptGenerator("shortRoleSummary", prompt_vars)
			job.role_description = AnsweringEngine.sendSimpleChatPrompt(prompt, "shortRoleSummary", tokens = 100)

		# Needs converted to an array of strings
		if (not job.requirements or not len(job.requirements) > 3):
			logging.info("Had To Regen Requirements")
			prompt = AnsweringEngine.promptGenerator("roleRequirements", prompt_vars)
			response = AnsweringEngine.sendSimpleChatPrompt(prompt, "roleRequirements", tokens = 300)
			
			if response:
				for bullet_point in response.splitlines():
					if len(bullet_point) > 5: # Basic Garbage Check
						job.requirements.append(bullet_point.removeprefix("- "))
		
		# Needs converted to an array of strings
		if (not job.key_points or not len(job.key_points) > 3):
			logging.info("Had To Regen Oppertunities")
			prompt = AnsweringEngine.promptGenerator("roleKeyPoints", prompt_vars)
			response = AnsweringEngine.sendSimpleChatPrompt(prompt, "roleKeyPoints", tokens = 300)
			if response:
				for bullet_point in response.splitlines():
					if len(bullet_point) > 5: # Basic Garbage Check
						job.key_points.append(bullet_point.removeprefix("- "))

		# Validate Pre-Processing Went Well
		if None in [job.short_description, job.role_description] or len(job.requirements) < 3 or len(job.key_points) < 3:
			self.upsert_job({
				"job_processing_failure": True,
				"job_processing": False
			})
			return

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
				logging.warning("question allready filled: " + question.id)
				continue

			if question.type == JobSchema.FieldType.TEXT:
				prompt_vars = {
					"question": question.ai_prompt or question.content,
					"available_variables": ",".join(UserSchema.UserDataFields.__fields__.keys()) + "," + ",".join(special_case_fields)
				}
				logging.info("Question:" + question.content)
				prompt = AnsweringEngine.promptGenerator("questionPreprocessor", prompt_vars)
				instructions = "You Are Matching Questions To Variables, Do not use more than 5 additional words"
				response = AnsweringEngine.sendSimpleChatPrompt(prompt, "questionPreprocessor",system=instructions,  force_single_line=True, tokens = 10)
				# TODO: Add better code here to validate the response can be parsed
				if "N/A" in response.upper():
					logging.info("Cant Be Substituded")
					continue
				if "{" in response and "}" in response:
					question.response = response
					logging.info("Can Be Substituded with" + response)
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

		question_responses["status"] = ApplicationStatus.REVIEWED
		question_responses["application_reviewed_ts"] = datetime.datetime.now()

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
			}, {
				"$set": {
					'status': ApplicationStatus.REQUESTED if requestApply else ApplicationStatus.READ,
					'application_read_ts': datetime.datetime.now(),
					'application_requested_ts': datetime.datetime.now(),
				}
			}, upsert=True)
		return True
	
