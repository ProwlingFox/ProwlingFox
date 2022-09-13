#Start Logger
import logger as lg
lg.init()
logger = lg.log;

import json, argparse, asyncio
from pymongo import MongoClient

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


def main():
	mClient = MongoClient(secrets["database"]["credentials"])
	jobaiDB = mClient.jobai
	jobsCollection = jobaiDB.jobs

	testJob = {
		"jobTitle": "Software Engineer",
		"company": "Docket Technologies Inc",
	}

	insertID = jobsCollection.insert_one(testJob).inserted_id

	return

if __name__ == "__main__":
	parseArgs()

	try:
		main()
	except KeyboardInterrupt:
		print("Exiting Gracefully (Kbd Interrupt)...")
	except Exception as e:
		logger.trace()