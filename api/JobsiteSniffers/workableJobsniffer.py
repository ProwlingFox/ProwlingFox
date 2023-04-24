import requests
from datetime import datetime
import html2text
from JobsiteSniffers.baseJobsniffer import baseJobsniffer
import components.schemas.job as JobSchema

workableAPI = "https://jobs.workable.com/api/v1/"

class workableJobsniffer(baseJobsniffer):
	jobsStack = []
	jobOffset = 0
	searchFilter = "Software"

	def __init__(self, config):
		super().__init__(config)
		return

	def __iter__(self):
		return self

	def __next__(self):
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
			role_category = "Software",
			remote = "TELECOMMUTE" in rawJob["locations"],
			skills = ["Python"],
			status = JobSchema.Status.ACTIVE,
			location = "{city}, {subregion}, {countryName}".format(**rawJob["location"]),
			listing = self.generateJobListing(rawJob),
			questions = self.getQuestions(rawJob),
		)
		
	questionTypeTranslation = {
		"paragraph": JobSchema.FieldType.TEXT,
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
						question["label"] = "Create a first person personalised summary of a person who is applying to this position."
					if question["id"] == "cover_letter":
						question["label"] = "Create a cover letter for this position."
					if "onlyTrueAllowed" in question:
						qresponse = True

					if not self.questionTypeTranslation[question["type"]] :
						continue

					formattedQuestion = JobSchema.Question(
						id = question["id"],
						content = question["label"] if "label" in question else "Missing Question",
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
			"location": ""
			}
		response = requests.request("GET", workableAPI + "jobs", params=querystring)
		json = response.json()

		if json["jobs"]:
			self.jobsStack += json["jobs"]
			self.jobOffset += 10
			return True
		else:
			return False

	def uploadResume(self, jobID):
		uploadUrl = workableAPI + "jobs/" + jobID + "/form/upload/resume?contentType=application\%2Fpdf"

		resume = open("resume.pdf", "rb")
		files = {'file': resume}

		getHeaders = {"Content-Type": "application/pdf"}
		response = requests.request("GET", uploadUrl, headers=getHeaders)
		responseJson = response.json()

		payload = responseJson["uploadPostUrl"]["fields"]
		payload["Content-Type"] = "application/pdf"
		awsresponse = requests.request("POST", responseJson["uploadPostUrl"]["url"], data=payload, files=files)

		return responseJson["downloadUrl"]

	def apply(self, job):
		applicationURL = workableAPI + "jobs/" + job["exid"] + "/apply"

		body = {"candidate": []}

		for question in job["questions"]:
			if question["type"]:
				body["candidate"].append({
					"name": question["id"],
					"value": question["response"]
				})
			else:
				#Check If Looking For Known File
				if question["rawtype"] == "file":
					if question["id"] == "resume":
						body["candidate"].append({
							"name": question["id"],
							"value": {
								"url": self.uploadResume(job["exid"]),
								"name": "resume.pdf"
							}

						})
						continue
				#Check if required
				if question["required"]:
					raise Exception("Missing Type For Required Field %s on question %s" % (question["rawtype"], question["label"]))

		headers = {"Content-Type": "application/json"}
		response = requests.request("POST", applicationURL, headers=headers, json=body)
		return True

	def generateJobListing(self, rawJob):
		h = html2text.HTML2Text()
		h.ignore_links = True

		return f"""
{rawJob["title"]} at {rawJob["company"]["title"]}

{h.handle(rawJob["company"]["description"])}

{h.handle(rawJob["description"])}

{('REQUIREMENTS:' + h.handle(rawJob["requirementsSection"])) if rawJob["requirementsSection"] else ""}

Application
============
"""

