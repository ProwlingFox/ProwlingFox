import json, argparse, asyncio
from pprint import pprint
import traceback
from pymongo import MongoClient
from pymongo import errors as MongoErrors
import components.schemas.job as JobSchema

#Load Secret keys
fSecrets = open("secrets.json", "r")
secrets = json.load(fSecrets)
fSecrets.close()

global globalSettings;

def parseArgs():
	parser = argparse.ArgumentParser(description='Scrape Jobsites and upload them to a database')
	parser.add_argument('-v', action='store_true', default=False, required=False, help='Verbose Mode')
	globalSettings = parser.parse_args()

# Returns Itterable jobsniffer based on module name.
def loadJobSniffer(jobSnifferName, forceLoad=False):
	snifferData = secrets["sniffers"][jobSnifferName]

	if not (forceLoad or snifferData["enabled"]) :
		return False

	try:
		jsPlugin = __import__("JobsiteSniffers.%s" % jobSnifferName, globals(), locals(), [jobSnifferName], 0)
		js = getattr(jsPlugin, jobSnifferName)
		return js(secrets["sniffers"][jobSnifferName])
	except Exception as e:
		print("Error with %s Plugin" % (jobSnifferName))
		print(traceback.format_exc())
		return False


def main():
	mClient = MongoClient(secrets["database"]["credentials"])
	global jobaiDB
	jobaiDB = mClient.jobai
	jobsCollection = jobaiDB.jobs

	for sniffer in secrets["sniffers"]:
		js = loadJobSniffer(sniffer)
		if js:
			updateJobs(js)

	return

def updateJobs(sniffer):
	# Jobs need to be preprocessed before they are added to the db, the following actions need to be preformed;
	# - Shorten the Job Listing for both GPT and Display Purposes
	# - Identify The Job's Role
	# - Identify any kind of preset responses to the questions that can easily be subbed in instead of getting an answer from GPT


	jobCounter = 0;

	for job in sniffer:
		try:
			# insertJobIntoDB({
			# 	"source": sniffer.ID,
			# 	"exid": job["exid"],
			# 	"jobTitle": job["position"],
			# 	"company": job["company"],
			# 	"longListing": job["listing"],
			# 	"questions": job["questions"]
			# })

			insertJobIntoDB(job)
			jobCounter += 1
			print(f"Inserted Job From {job.company.name} Into DB | Inserted {jobCounter}")
		except MongoErrors.DuplicateKeyError:
			print("Job Allready Existed")
			continue;

		# Add A Shortened Listing To The Job
		# Classify The Job's Role
		# Classify The Job's Question Types
	return

def insertJobIntoDB(job: JobSchema.Job):
	jobsCollection = jobaiDB.jobs
	jobsCollection.insert_one(json.loads(job.json()))

if __name__ == "__main__":
	parseArgs()

	try:
		main()
	except KeyboardInterrupt:
		print("Exiting Gracefully (Kbd Interrupt)...")
	except Exception as e:
		raise e