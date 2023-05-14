import logging
from time import sleep
from typing import List
from numpy import dot
from numpy.linalg import norm
import openai
from schemas.configurations import B64_File
from components.secrets import secrets
openai.api_key = secrets["OPENAI_KEY"]

import schemas.job as JobSchema
import schemas.user as UserSchema

from datetime import datetime

class AnsweringEngine:

	# Should Probable be moved out of this class
	@staticmethod
	def answer_question(job: JobSchema.Job, user: UserSchema.User, question: JobSchema.Question):

		# If this job has no short summary freak out
		if not job.short_description:
			raise "No Short Description :c"
		
		if question.response:
			return None
			# return AnsweringEngine.generate_prefilled_response(user, question)

		if question.type == JobSchema.FieldType.TEXT or question.type == JobSchema.FieldType.LONG_TEXT:
			prompt = AnsweringEngine.promptGenerator("answerJobQuestionPrompt", {
				"role": job.role,
				"companyName": job.company.name,
				"jobDescription": job.short_description,
				"FullName": user.name,
				"Email": user.email,
				"question": question.ai_prompt or question.content
			} )

			return AnsweringEngine.sendSimpleChatPrompt(prompt, "answerQuestion")
	
		return None

	@staticmethod
	def generate_prefilled_response(user: UserSchema.User, question: JobSchema.Question):
		string = question.response
		
		if string == "{resume}":
			return B64_File(file_name=user.data.resume.file_name, data=f"preset:{user.id},resume").dict()

		for key, value in user.data:
			string = string.replace("{" + key + "}", str(value))

		# Email is a special case, Potentially replaced later as an email aggregator
		string = string.replace("{email}", str(user.email))
		return string

	@staticmethod
	def promptGenerator(promptName, variableDict):
		with open('prompts/'+promptName, 'r') as f:
			rawPrompt = f.read()

		variableNames = set(var.split('}}')[0] for var in rawPrompt.split('{{') if '}}' in var)

		text = rawPrompt
		for variableName in variableNames:
			if variableName in variableDict:
				text = text.replace('{{' + variableName + '}}', variableDict[variableName])
		return text

	@staticmethod
	def getEmbedding(prompt: str, note=None):
		model = "text-embedding-ada-002"
		attempts = 0
		while attempts < 3:
			try:
				sent_timestamp_ms = datetime.now()
				response = openai.Embedding.create(
					input=prompt,
					model="text-embedding-ada-002"
				)

				from components.db import prowling_fox_db as jobaiDB
				jobaiDB.openai_request_log.insert_one({
					"sent_ts": sent_timestamp_ms,
					"model": model,
					"success": True,
					"prompt_tokens": response["usage"]["prompt_tokens"],
					"completion_tokens": 0,
					"total_tokens": response["usage"]["total_tokens"],
					"note": note
				})

				return response["data"][0]["embedding"]
			except openai.OpenAIError as e:
				attempts += 1
				logging.warning("OpenAI Embedding Request Rate Limited")
				sleep(1)

	@staticmethod
	def cosine_similarity(vector1: List[float], vector2: List[float]) -> int:
		return dot(vector1, vector2)/(norm(vector1)*norm(vector2))

	@staticmethod
	def sendCompletionPrompt(prompt: str, note=None, tokens = 1024)-> str:
		model = "text-davinci-003"
		try:
			sent_timestamp_ms = datetime.now()
			response = openai.Completion.create(
				model=model,
				prompt=prompt,
				max_tokens=tokens,
			)
			answer = response["choices"][0]["text"].lstrip('\n')

			from components.db import prowling_fox_db as jobaiDB
			jobaiDB.openai_request_log.insert_one({
				"sent_ts": sent_timestamp_ms,
				"model": model,
				"success": True,
				"prompt_tokens": response["usage"]["prompt_tokens"],
				"completion_tokens": response["usage"]["completion_tokens"],
				"total_tokens": response["usage"]["total_tokens"],
				"note": note
			})

			return answer
		except openai.OpenAIError as e:
			logging.warning("I actually got to the error c:")
			logging.warning(e.code)
			raise e	
	
	@staticmethod
	def sendSimpleChatPrompt(prompt: str, note=None, force_single_line = False, system = 'You are applying to the following job. You should answer as though you are the person applying. DO NOT SAY "As An AI" or anything like that.' , tokens = 1024)-> str:
		model = "gpt-3.5-turbo"
		attempts = 0
		while attempts < 5:
			try:
				sent_timestamp_ms = datetime.now()
				response = openai.ChatCompletion.create(
					model=model,
					messages = [
						{"role": "system", "content": system},
						{"role": "user", "content": prompt}
					],
					max_tokens=tokens,
					stop= "\n" if force_single_line else None
				)
				answer = response["choices"][0]["message"]["content"]

				from components.db import prowling_fox_db as jobaiDB
				jobaiDB.openai_request_log.insert_one({
					"sent_ts": sent_timestamp_ms,
					"model": model,
					"success": True,
					"prompt_tokens": response["usage"]["prompt_tokens"],
					"completion_tokens": response["usage"]["completion_tokens"],
					"total_tokens": response["usage"]["total_tokens"],
					"note": note
				})

				return answer
			except openai.OpenAIError as e:
				if "message" in e.error:
					error_message: str = e.error["message"]
					if error_message.startswith("Rate limit reached") or error_message.startswith("That model is currently overloaded"):
						logging.warning("OpenAI Chat Prompt Request Rate Limited")
						sleep(20)
						attempts += 1
						continue
				logging.error("Other Issue With OPENAI Call")
				attempts += 1
				continue
