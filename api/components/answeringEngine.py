import openai
import components.secrets as secrets
from prompts.promptParser import promptGenerator
openai.api_key = secrets.secrets["OpenAISecret"]

from datetime import datetime
import bson

class AnsweringEngine:

	@staticmethod
	def answer_question(job, user, quesitionID):
		jobDetails = job.get_details()
		userDetails = user.get_info()

		# If this job has no short summary generate one now
		if not jobDetails["shortListing"]:
			jobDetails["shortListing"] = AnsweringEngine.summarize_Job_Description(jobDetails["longListing"])
			job.update_short_listing(jobDetails["shortListing"])

		prompt = promptGenerator("answerJobQuestionPrompt", {
			"role": jobDetails["jobTitle"],
			"companyName": jobDetails["company"],
			"jobDescription": jobDetails["shortListing"],
			"FullName": userDetails["name"],
			"Email": userDetails["email"],
			"question": next((obj["question"] for obj in jobDetails["questions"] if obj["id"] == quesitionID), None)
		} )

		response = AnsweringEngine.sendSimpleChatPrompt(prompt, "answerQuestion")

		return response

	@staticmethod
	def summarize_Job_Description(fullDescription):
		prompt = promptGenerator("summarizeJobDescription", {"fullDescription": fullDescription})
		response = AnsweringEngine.sendSimpleChatPrompt(prompt, "summarizeJobDescription", tokens = 300)
		return response

	@staticmethod
	def sendCompletionPrompt(prompt, note=None, tokens = 1024):
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
			print(e)
			raise e		
	
	@staticmethod
	def sendSimpleChatPrompt(prompt, note=None, system = 'You Are A Job Application Engine', tokens = 1024):
		model = "gpt-3.5-turbo"
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
			print("I actually got to the chat error c:")
			print(e)
			raise e