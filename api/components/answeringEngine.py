import openai
import components.secrets as secrets
from prompts.promptParser import promptGenerator
openai.api_key = secrets.secrets["OpenAISecret"]

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

		response = AnsweringEngine.sendCompletionPrompt(prompt)

		return response

	@staticmethod
	def summarize_Job_Description(fullDescription):
		prompt = promptGenerator("summarizeJobDescription", {"fullDescription": fullDescription})
		response = AnsweringEngine.sendCompletionPrompt(prompt, 300)
		return response

	@staticmethod
	def sendCompletionPrompt(prompt, tokens = 1024):
		response = openai.Completion.create(
			model="text-davinci-003",
			prompt=prompt,
			max_tokens=tokens,
		)

		print(response)
		answer = response["choices"][0]["text"].lstrip('\n')
		return answer