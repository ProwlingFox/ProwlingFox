# 3rd Party Imports
import json, openai
from time import sleep

# Error Handling Imports
from pymongo import errors as MongoErrors
from JobsiteSniffers.baseJobsniffer import OutOfJobs

# Initiialisation Imports
from components.secrets import secrets
from components.db import prowling_fox_db as jobaiDB

# Class Imports
from components.answeringEngine import AnsweringEngine
from components.job import Job
from components.user import User

# Configuration
openai.api_key = secrets["OpenAISecret"]

# Schema/Typing Imports
from typing import Iterator, List
import schemas.job as JobSchema
import schemas.user as UserSchema
from schemas.configurations import Role

SECTORS_WHITELIST = ["IT and Digital Technology"]
MIN_JOB_PER_ROLE = 1

EMPTY_ROLES = []

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

def solve_application():
    application_from_db = jobaiDB.applications.find_one_and_update({
        "application_requested": True,
        "application_processing": False,
        "application_processed": False,
        "application_sent": False
    },
    {
        '$set': {'application_processing': True}
    })

    if not application_from_db:
         return
    
    application = JobSchema.Application.parse_obj(application_from_db)

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

def preprocess_job():
    job_to_preprocess_from_db = jobaiDB.jobs.find_one_and_update({
        "job_processing": {"$ne": True},
        "short_description": None
    },{
        '$set': {'job_processing': True}
    })

    if not job_to_preprocess_from_db:
        return

    job = JobSchema.Job.parse_obj(job_to_preprocess_from_db)

    global role_embeddings
    j = Job(job.id)
    print("preprocessing job: ", job.id)
    j.preprocess_job(role_embeddings)
    return

def load_jobSniffer(jobSnifferName, forceLoad=False):
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

def fillQuestionEmbeddings():
    jobaiDB.predefinedQuestions.delete_many({})
    predefined_variables = UserSchema.UserDataFields.__fields__.keys()

    for predefined_variable in predefined_variables:
        embeding = AnsweringEngine.getEmbedding(predefined_variable, "GeneratePredefinedVariableEmbedings")

        jobaiDB.predefined_variables.insert_one({
            "variable_name": predefined_variable,
            "embeding": embeding
        })
        print("inserted", predefined_variable)
    return

def getRoleEmbeddings() -> List[Role]:
    return list(map(lambda x: Role.parse_obj(x),  jobaiDB.roles.find({}) ))

def insert_one_job(sniffer, searchQuery=None):
    while True:
        try:
            job = JobSchema.Job.parse_obj(sniffer.getOneJob(searchQuery))
            resp = jobaiDB.jobs.insert_one(job.dict())
            print(f"Inserted Job From {job.company.name} Into DB | ID:{resp.inserted_id}")
            return
        except OutOfJobs:
            print("That Query Is Out Of Jobs")
            global EMPTY_ROLES
            EMPTY_ROLES.append(searchQuery)
            break
        except MongoErrors.DuplicateKeyError:
            print("Job Allready Existed")

def get_jobs():
    global SECTORS_WHITELIST, MIN_JOB_PER_ROLE
    # Get The Roles that don't have enough jobs
    roles_to_add = jobaiDB.roles.aggregate([
        {
            '$lookup': {
                'from': 'jobs', 
                'let': {
                    'role': '$role'
                }, 
                'pipeline': [
                    {
                        '$match': {
                            '$expr': {
                                '$in': [
                                    '$$role', {'$ifNull': [ "$role_category", [] ]}
                                ]
                            }
                        }
                    }, {
                        '$count': 'count'
                    }
                ], 
                'as': 'count'
            }
        }, {
            '$match': {
                'sector': {
                    '$in': SECTORS_WHITELIST
                }
            }
        }, {
            '$unwind': {
                'path': '$count', 
                'preserveNullAndEmptyArrays': True
            }
        }, {
            '$project': {
                'role': 1, 
                'sector': 1, 
                'count': '$count.count'
            }
        }, {
            '$match': {
                '$and': [
                    {'$or': [
                        { 'count': { '$lt': MIN_JOB_PER_ROLE } },
                        { 'count': { '$exists': False } },
                    ]},
                    { 'role': { '$nin': EMPTY_ROLES  }}
                ]
                
            }
        }
    ])

    if not roles_to_add:
         return
    
    roleToAdd = roles_to_add.next()["role"]

    for jobSniiffer in jobSniiffers:
        insert_one_job(jobSniiffer, searchQuery=roleToAdd)
    return

def apply_to_job():
    application_from_db = jobaiDB.applications.find_one_and_update({
        "application_reviewed": True,
        "application_sending": {"$ne": True}
    },
    {
        '$set': {'application_sending': True}
    })

    if not application_from_db:
        return

    application = JobSchema.Application.parse_obj(application_from_db)
    job = Job(application.job_id).get_details()

    jobSniffer = load_jobSniffer(job.source, True)
    resp = jobSniffer.apply(job, application)
    print(resp.text)

    jobaiDB.applications.update_one({
        "_id": application.id
    },{
         "$set": {"application_sent": True}
    })
    return


jobSniiffers = [
    load_jobSniffer("workableJobsniffer")
]

# Load into memory to prevent expensive db calls, (Eventually lets implement a vector DB)
role_embeddings=getRoleEmbeddings()

def main():
    process_functions = [
        get_jobs,
        preprocess_job,
        solve_application,
        apply_to_job,
    ]

    while True:   
        # For now, just round robin things in the queue, rlly needs a balancer and to be made asyncio lol, tho rn we're being rate limited
        for process_function in process_functions:
            process_function()
        sleep(0.5)
        print("Done One Round")
        continue

if __name__ == "__main__":
    try:
        reset_processing()
        # fillRoleEmbeddings()
        # fillQuestionEmbeddings()
        main()
    except KeyboardInterrupt:
        print("Exiting Gracefully (Kbd Interrupt)...")
    except Exception as e:
        raise e