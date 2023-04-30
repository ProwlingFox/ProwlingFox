import base64
import requests
from datetime import datetime
import html2text
from JobsiteSniffers.baseJobsniffer import baseJobsniffer
import schemas.job as JobSchema
from schemas.configurations import City


workableAPI = "https://jobs.workable.com/api/v1/"

class workableJobsniffer(baseJobsniffer):
	jobsStack = []
	jobOffset = 0
	duplicate_entries = 0
	searchFilter = "Software"
	locationFilter = "UK"

	def __init__(self, config):
		super().__init__(config)
		return

	def getOneJob(self):
		#Refill queue if needed or end the itterator
		if not self.jobsStack:
			if not self.refillStack():
				raise StopIteration
			
		#Return a Job From The Stack In Expected Format
		return self.formatJob( self.jobsStack.pop() )

	def formatJob(self, rawJob):
		datetime_obj = datetime.fromisoformat(rawJob["created"][:-1])
		epoch_time = int(datetime_obj.timestamp())

		logo = rawJob["company"]["image"] if "image" in rawJob["company"] else None
		tagline = rawJob["company"]["socialSharingDescription"] if "socialSharingDescription" in rawJob["company"] else None
		website = rawJob["company"]["url"] if "url" in rawJob["company"] else None

		company = JobSchema.Company (
			name = rawJob["company"]["title"],
			logo = logo,
			website = website,
			tagline = tagline
		)

		return JobSchema.Job (
			source = self.__class__.__name__ ,
			ext_ID = rawJob["id"],
			added_ts=0,
			last_updated_ts=0,
			long_description=self.generateJobListing(rawJob),
			created_ts= epoch_time,
			company = company,
			role = rawJob["title"],
			remote = "TELECOMMUTE" in rawJob["locations"],
			skills = ["Python"],
			status = JobSchema.Status.ACTIVE,
			location = City(city=rawJob["location"]["city"], region=rawJob["location"]["subregion"], country=rawJob["location"]["countryName"]),
			listing = self.generateJobListing(rawJob),
			questions = self.getQuestions(rawJob),
		)
		
	questionTypeTranslation = {
		"paragraph": JobSchema.FieldType.LONG_TEXT,
		"boolean": JobSchema.FieldType.CHECKBOX,
		"text": JobSchema.FieldType.TEXT,
		"number": JobSchema.FieldType.NUMBER,
		"email": JobSchema.FieldType.TEXT,
		"phone": JobSchema.FieldType.TEXT,
		"multiple": JobSchema.FieldType.MULTIPLE_CHOICE,
		"dropdown": JobSchema.FieldType.MULTIPLE_CHOICE,
		"date": JobSchema.FieldType.DATE,
		"group": None,
		"file": JobSchema.FieldType.FILE
	}

	def getQuestions(self, rawJob):
			questionsURL = workableAPI + "jobs/" + rawJob["id"] + "/form"
			response = requests.request("GET", questionsURL)
			responseJson = response.json()

			questions = []

			for section in responseJson:
				for question in section["fields"]:
					qresponse = None
					if question["id"] == "summary":
						question["ai"] = "Create a first person personalised summary of a person who is applying to this position."
					if question["id"] == "cover_letter":
						question["ai"] = "Create a cover letter for this position."
					if question["id"] == "gdpr":
						question["label"] = "I have read, understand and accept the content of this Privacy Notice and consent to the processing of my data as part of this application."
					if "onlyTrueAllowed" in question:
						qresponse = True

					if not self.questionTypeTranslation[question["type"]] :
						continue

					formattedQuestion = JobSchema.Question(
						id = question["id"],
						content = question["label"] if "label" in question else "Missing Question",
						ai_prompt = question["ai"] if "ai" in question else None,
						type = self.questionTypeTranslation[question["type"]],
						required = question["required"],
						raw_data= {
							'raw_question_type': question["type"]
						}
					)

					if 'options' in question:
						formattedQuestion.choices = []
						for c in question["options"]:
							formattedQuestion.choices.append(
								JobSchema.Choice(
									id = c["name"],
									content = c["value"]
							))


					questions.append(formattedQuestion)

			return questions

	def refillStack(self):
		querystring = {
			"remote": False,
			"offset":self.jobOffset,
			"query":self.searchFilter,
			"location": self.locationFilter
			}
		response = requests.request("GET", workableAPI + "jobs", params=querystring)
		json = response.json()

		if json["jobs"]:
			self.jobsStack += json["jobs"]
			self.jobOffset += 10
			return True
		else:
			return False

	def uploadResume(self, data_url:str, job_id):
		# Process File
		# Strip MIME Types
		header, encoded = data_url.split(",", 1)

		if "base64" not in header:
			raise ValueError("Not a base64-encoded data URL")
		
		mimetype = header.split(";")[0].split(":")[1]
		file = base64.b64decode(encoded)


		uploadUrl = f"{workableAPI}jobs/{job_id}/form/upload/resume?contentType={mimetype}"

		files = {'file': file}

		getHeaders = {"Content-Type": mimetype}
		response = requests.request("GET", uploadUrl, headers=getHeaders)
		responseJson = response.json()

		payload = responseJson["uploadPostUrl"]["fields"]
		payload["Content-Type"] = mimetype
		awsresponse = requests.request("POST", responseJson["uploadPostUrl"]["url"], data=payload, files=files)

		return responseJson["downloadUrl"]

	def apply(self, job: JobSchema.Job, application: JobSchema.Application):
		applicationURL = f"{workableAPI}jobs/{job.ext_ID}/apply"

		body = {"candidate": []}

		for question in job.questions:
			if not question.type == JobSchema.FieldType.FILE:
				body["candidate"].append({
					"name": question.id,
					"value": application.responses[question.id]
				})
			else:
				body["candidate"].append({
					"name": question.id,
					"value": {
						"url": self.uploadResume(application.responses[question.id]["data"], job.ext_ID),
						"name": application.responses[question.id]["file_name"]
					}
				})

		headers = {"Content-Type": "application/json"}
		response = requests.request("POST", applicationURL, headers=headers, json=body)
		return response

	def generateJobListing(self, rawJob):
		h = html2text.HTML2Text()
		h.ignore_links = True

		return f"""
{rawJob["title"]} at {rawJob["company"]["title"]}

{h.handle(rawJob["company"]["description"])}

{h.handle(rawJob["description"])}

{('REQUIREMENTS:' + h.handle(rawJob["requirementsSection"])) if rawJob["requirementsSection"] else ""}

{('BENIFITS:' + h.handle(rawJob["benefitsSection"])) if rawJob["benefitsSection"] else ""}
"""