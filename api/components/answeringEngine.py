from time import sleep
import openai
import components.secrets as secrets
openai.api_key = secrets.secrets["OpenAISecret"]

import components.schemas.job as JobSchema


from datetime import datetime
import bson

class AnsweringEngine:

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
	def answer_question(job: JobSchema.Job, user, question: str):

		# If this job has no short summary freak out
		if not job.short_description:
			raise "No Short Description :c"

		prompt = AnsweringEngine.promptGenerator("answerJobQuestionPrompt", {
			"role": job.role,
			"companyName": job.company.name,
			"jobDescription": job.short_description,
			"FullName": user["name"],
			"Email": user["email"],
			"question": question
		} )

		response = AnsweringEngine.sendSimpleChatPrompt(prompt, "answerQuestion")

		return response

	@staticmethod
	def sendCompletionPrompt(prompt, note=None, tokens = 1024)-> str:
		model = "text-davinci-003"
		try:
			sent_timestamp_ms = datetime.now()
			response = openai.Completion.create(
				model=model,
				prompt=prompt,
				max_tokens=tokens,
			)
			answer = response["choices"][0]["text"].lstrip('\n')

			from components.db import jobaiDB
			jobaiDB.request_log.insert_one({
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
			print("I actually got to the error c:")
			print(e.code)
			raise e	
	
	@staticmethod
	def sendSimpleChatPrompt(prompt, note=None, system = 'You Are A Job Application Engine', tokens = 1024)-> str:
		model = "gpt-3.5-turbo"
		attempts = 0
		while attempts < 3:
			try:
				sent_timestamp_ms = datetime.now()
				response = openai.ChatCompletion.create(
					model=model,
					messages = [
						{"role": "system", "content": system},
						{"role": "user", "content": prompt}
					],
					max_tokens=tokens,
				)
				answer = response["choices"][0]["message"]["content"]

				from components.db import jobaiDB
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
				error_message: str = e.error["message"]
				if error_message.startswith("Rate limit reached"):
					print("Rate Limited")
					sleep(20)
					attempts += 1
				else:
					raise e