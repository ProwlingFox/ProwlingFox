# 3rd Party Imports
import json, openai
from time import sleep

# Error Handling Imports
from pymongo import errors as MongoErrors

# Initiialisation Imports
import components.secrets as s
s.init()
secrets = s.secrets

import components.db as db
db.init()
jobaiDB = db.jobaiDB

# Class Imports
from components.answeringEngine import AnsweringEngine
from components.job import Job
from components.user import User

# Configuration
openai.api_key = secrets["OpenAISecret"]

# Schema/Typing Imports
from typing import Iterator, List
import schemas.job as JobSchema
from schemas.configurations import Role

def reset_processing():
    # update all records, mark them as not currently being processed
    jobaiDB.applications.update_many({
        "application_processing": True
    },{
        '$set': {'application_processing': False}
    })
    jobaiDB.jobs.update_many({
        "job_processing": True
    },{
        '$set': {'job_processing': False}
    })
    return

def solve_application(application: JobSchema.Application):
    job = Job(application.job_id).get_details()
    user = User(application.user_id).get_info()

    answered_questions = {}

    for question in job.questions:
        print("answering question:", question.id)
        if question.type == JobSchema.FieldType.TEXT or question.type == JobSchema.FieldType.LONG_TEXT:
            answer = AnsweringEngine.answer_question(job, user, question)
            print(answer)
        else:
            answer = None

        answered_questions[question.id] = answer

    jobaiDB.applications.update_one({
        "_id": application.id,
        "application_requested": True,
        "application_processing": True,
        "application_processed": False
    },
    {
        '$set': {
            'responses': answered_questions,
            "application_processing": False,
            "application_processed": True
        }
    })
    return

def preprocess_job(job: JobSchema.Job):
    global role_embeddings
    j = Job(job.id)
    print("preprocessing job: ", job.id)
    j.preprocess_job(role_embeddings)
    return

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
		raise

def updateOneJob(snifferIter: Iterator ):
    try:
        job = JobSchema.Job.parse_obj(next(snifferIter))
        resp = jobaiDB.jobs.insert_one(job.dict())
        print(f"Inserted Job From {job.company.name} Into DB | ID:{resp.inserted_id}")
    except MongoErrors.DuplicateKeyError:
        print("Job Allready Existed")
    return

def fillRoleEmbeddings():
    jobaiDB.roles.delete_many({})
    with open("roleslist.md") as roles_list:
        current_sector = "Misc."
        
        while True:
            line = roles_list.readline().removesuffix('\n')
            if not line:
                break

            if line.startswith("#"):
                current_sector = line.removeprefix("# ")
                continue

            embeding = AnsweringEngine.getEmbedding(current_sector + " " + line, "GenerateRoleEmbedings")
            
            role = Role(
                role=line,
                sector=current_sector,
                embedding=embeding
            )

            jobaiDB.roles.insert_one(role.dict())
            print("inserted", line)
    return

def getRoleEmbeddings() -> List[Role]:
    return list(map(lambda x: Role.parse_obj(x),  jobaiDB.roles.find({}) ))



process_queue = {
    "application_processor": [],
    "job_preprocessor": []
}

process_functions = {
    "job_preprocessor": preprocess_job,
    "application_processor": solve_application
}

jobSniifferIters = [
    iter(loadJobSniffer("workableJobsniffer"))
]

# Load into memory to prevent expensive db calls, (Eventually lets implement a vector DB)
role_embeddings=getRoleEmbeddings()

def main():
    while True:
        # Work Out What Tasks to do
        # Tasks Include:
        # - Loading More Jobs into the system
        for jobSnifferIter in jobSniifferIters:
            updateOneJob(jobSnifferIter)

        # - Pre-Resolving said jobs
        job_to_preprocess_from_db = jobaiDB.jobs.find_one_and_update({
            "job_processing": {"$ne": True},
            "short_description": None
        },{
            '$set': {'job_processing': True}
        })

        if job_to_preprocess_from_db:
            process_queue["job_preprocessor"].append( JobSchema.Job.parse_obj(job_to_preprocess_from_db) )
        

        # - Answering Applications
        application_from_db = jobaiDB.applications.find_one_and_update({
            "application_requested": True,
            "application_processing": False,
            "application_processed": False,
            "application_sent": False
        },
        {
            '$set': {'application_processing': True}
        })

        if application_from_db:
            process_queue["application_processor"].append( JobSchema.Application.parse_obj(application_from_db) )

        # For now, just round robin things in the queue, rlly needs a balancer and to be made asyncio lol, tho rn we're being rate limited
        for process_type in process_queue:
            typed_process_queue = process_queue[process_type]
            if (len(typed_process_queue) > 0):
                process_functions[process_type](typed_process_queue.pop(0))


        sleep(0.5)
        print("Done One Round")
        continue

if __name__ == "__main__":
    try:
        reset_processing()
        # fillRoleEmbeddings()
        main()
    except KeyboardInterrupt:
        print("Exiting Gracefully (Kbd Interrupt)...")
    except Exception as e:
        raise e