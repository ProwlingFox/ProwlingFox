#Start Logger
import components.logger as lg
lg.init()
logger = lg.log;

import json, argparse, asyncio
from pymongo import MongoClient
from pymongo import errors as MongoErrors

#Load Secret keys
fSecrets = open("secrets.json", "r")
secrets = json.load(fSecrets)
fSecrets.close()

global globalSettings;

def parseArgs():
	parser = argparse.ArgumentParser(description='Scrape Jobsites and upload them to a database')
	parser.add_argument('-v', action='store_true', default=False, required=False, help='Verbose Mode')
	globalSettings = parser.parse_args()

	if (globalSettings.v):
		logger.setLogLevel("debug")


# Returns Itterable jobsniffer based on module name.
def loadJobSniffer(jobSnifferName, forceLoad=False):
	snifferData = secrets["sniffers"][jobSnifferName]

	if not (forceLoad or snifferData["enabled"]) :
		return False

	try:
		jsPlugin = __import__("JobsiteSniffers.%s" % jobSnifferName, globals(), locals(), [jobSnifferName], 0)
		js = getattr(jsPlugin, jobSnifferName)
		return js(secrets)
	except Exception as e:
		logger.trace()
		print("Error with %s Plugin" % (jobSnifferName))
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
	jobCounter = 0;

	for job in sniffer:
		try:
			insertJobIntoDB({
				"source": sniffer.ID,
				"exid": job["exid"],
				"jobTitle": job["position"],
				"company": job["company"],
				"longListing": job["listing"],
				"questions": job["questions"]
			})
			jobCounter += 1
			print(f"Inserted Job From {job['company']} Into DB | Inserted {jobCounter}")
		except MongoErrors.DuplicateKeyError:
			print("Job Allready Existed")
		except:
			logger.trace()

	return

def insertJobIntoDB(job):
	jobsCollection = jobaiDB.jobs
	jobsCollection.insert_one(job)

if __name__ == "__main__":
	parseArgs()

	try:
		main()
	except KeyboardInterrupt:
		print("Exiting Gracefully (Kbd Interrupt)...")
	except Exception as e:
		logger.trace()