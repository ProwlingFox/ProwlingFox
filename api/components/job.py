from typing import List
from bson.objectid import ObjectId

from components.schemas.configurations import Role
from components.user import User
import components.schemas.job as JobSchema
import components.schemas.user as UserSchema
from components.answeringEngine import AnsweringEngine

class Job:
	job_data: JobSchema.Job = None

	def __init__(self, job_id: str | ObjectId):
		self.id = ObjectId(job_id) if type(job_id) is str else job_id
		return

	def preprocess_job(self, role_embeddings: List[Role]):
		def getClosestRole(role: str, predefined_roles: List[Role]) -> Role:
			role_embedding = AnsweringEngine.getEmbedding(role, "MatchRole")

			bestMatch = {
				"role": None,
				"cos_sim": 0
			}

			for predefined_role in predefined_roles:
				cos_sim = AnsweringEngine.cosine_similarity(predefined_role.embedding, role_embedding)
				if cos_sim > bestMatch["cos_sim"]:
					bestMatch = {
						"role": predefined_role,
						"cos_sim": cos_sim
					}
			
			return bestMatch["role"]

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

		role = getClosestRole(job.role, role_embeddings)

		self.upsert_job({
			"short_description": job.short_description,
			"role_description": job.role_description,
			"requirements": job.requirements,
			"key_points": job.key_points,
			"role_category": role.role,
			"sector_category": role.sector,
			"questions": list(map(lambda x: x.dict(), job.questions)),
			"job_processing": False
		})
		return

	def preprocess_questions(self, questions: List[JobSchema.Question]):
		special_case_fields = ["email"]


		for question in questions:
			# This Allows JobSniffers to prefil questions too
			if question.response:
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
	
