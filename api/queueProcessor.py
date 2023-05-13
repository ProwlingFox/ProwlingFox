# 3rd Party Imports
import datetime
import openai
import traceback
from bson import ObjectId
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
openai.api_key = secrets["OPENAI_KEY"]

# Schema/Typing Imports
from typing import List
import schemas.job as JobSchema
import schemas.user as UserSchema
from schemas.configurations import Role

SECTORS_WHITELIST = ["IT and Digital Technology"]
MIN_JOB_PER_ROLE_PER_COUNTRY = 5


EMPTY_ROLES = []

def reset_processing():
    # update all records, mark them as not currently being processed
    jobaiDB.applications.update_many({
        # "application_processing": True
    },{
        '$set': {'application_processing': False, 'application_sending': False}
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
        "application_processing": {"$ne": True},
        "application_processed":  {"$ne": True},
        "application_sent":  {"$ne": True}
    },
    {
        '$set': {
            'application_processing': True,
            'application_processing_ts': datetime.datetime.now()
        }
    })

    if not application_from_db:
         return

    application = JobSchema.Application.parse_obj(application_from_db)

    job = Job(application.job_id).get_details()
    user = User(application.user_id).get_info()

    answered_questions = {}

    for question in job.questions:
        print("answering question:", question.id)
        
        answer = AnsweringEngine.answer_question(job, user, question)
        print(answer)

        answered_questions[question.id] = answer

    jobaiDB.applications.update_one({
        "_id": application.id,
        "application_requested": True,
        "application_processing": True,
        "application_processed": {"$ne": True}
    },
    {
        '$set': {
            'responses': answered_questions,
            "application_processing": False,
            "application_processed": True,
            'application_processed_ts': datetime.datetime.now()
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
    j.preprocess_job()
    return

def load_jobSniffer(jobSnifferName):
	try:
		jsPlugin = __import__("JobsiteSniffers.%s" % jobSnifferName, globals(), locals(), [jobSnifferName], 0)
		js = getattr(jsPlugin, jobSnifferName)
		return js()
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

def insert_one_job(sniffer, searchQuery=None, locationQuery=None):
    while True:
        try:
            job = JobSchema.Job.parse_obj(sniffer.getOneJob(searchQuery, locationQuery))
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
            '$match': {
                'sector': {
                    '$in': SECTORS_WHITELIST
                }
            }
        }, {
            '$project': {
                'role': 1
            }
        }, {
            '$lookup': {
                'from': 'locations', 
                'pipeline': [], 
                'as': 'locations'
            }
        }, {
            '$unwind': {
                'path': '$locations'
            }
        }, {
            '$project': {
                'role': 1, 
                'country_code': '$locations.country_code'
            }
        }, {
            '$lookup': {
                'from': 'jobs', 
                'let': {
                    'role': '$role', 
                    'country_code': '$country_code'
                }, 
                'pipeline': [
                    {
                    '$lookup': {
                        'from': "applications",
                        'localField': "_id",
                        'foreignField': "job_id",
                        'as': "application",
                    },
                    },
                    {
                    '$match': {
                        'application': {
                            '$size': 0,
                        },
                    },
                    },
                    {
                        '$match': {
                            '$expr': {
                                '$and': [
                                    {
                                        '$in': [
                                            '$$role', '$role_category'
                                        ]
                                    }, {
                                        '$eq': [
                                            '$location.country', '$$country_code'
                                        ]
                                    }
                                ]
                            }
                        }
                    }
                ], 
                'as': 'jobs'
            }
        }, {
            '$project': {
                'role': 1, 
                'country_code': 1, 
                'count': {
                    '$size': '$jobs'
                }
            }
        }, {
            '$match': {
                '$and': [
                    {
                        'count': {
                            '$lt': MIN_JOB_PER_ROLE_PER_COUNTRY
                        }
                    }, {
                        'role': {
                            '$nin': EMPTY_ROLES
                        }
                    }
                ]
            }
        }
    ])

    if not roles_to_add:
         return

    try:
        toAdd = roles_to_add.next()
    except StopIteration:
        return

    for jobSniiffer in jobSniiffers:
        insert_one_job(jobSniiffer, searchQuery=toAdd["role"], locationQuery=toAdd["country_code"])
    return

def apply_to_job():
    application_from_db = jobaiDB.applications.find_one_and_update({
        "application_reviewed": True,
        "application_sending": {"$ne": True},
        "application_sent": {"$ne": True}
    },
    {
        '$set': {
            'application_sending': True,
            'application_sending_ts': datetime.datetime.now()
        }
    })

    if not application_from_db:
        return

    application = JobSchema.Application.parse_obj(application_from_db)
    job = Job(application.job_id).get_details()

    jobSniffer = load_jobSniffer(job.source)
    resp = jobSniffer.apply(job, application)

    application_failed = False
    if resp.status_code == 404:
        application_failed = True
        mark_job_inactive(job.id)
        print("Application Failed")

    jobaiDB.applications.update_one({
        "_id": application.id
    },{
         "$set": {
             "application_sent": True,
             "application_sent_ts": datetime.datetime.now(),
             'application_sending': False,
             "application_failed": application_failed
        }
    })
    return

def mark_job_inactive(job_id):
    jobaiDB.jobs.update_one(
        {"_id": ObjectId(job_id)},
        {
            "$set": {"status": JobSchema.Status.INACTIVE}
        }
    )
    return

def preprocess_job_embeddings():
    global role_embeddings
    job_from_db = jobaiDB.jobs.find_one_and_update({
        'job_processing': {'$ne': True},
        'sector_category': None,
        'role_category': None
    },
    {
        '$set': {'job_processing': True}
    })

    if not job_from_db:
        return

    job = JobSchema.Job.parse_obj(job_from_db)

    def getCloseRoles(role: str, predefined_roles: List[Role]):
        COS_SIM_EPSILON = 0.02

        role_embedding = AnsweringEngine.getEmbedding(role, "MatchRole")

        cos_sims = []

        for predefined_role in predefined_roles:
            cos_sim = AnsweringEngine.cosine_similarity(predefined_role.embedding, role_embedding)
            cos_sims.append({
                "role": predefined_role.role,
                "sector": predefined_role.sector,
                "cos_sim": cos_sim
            })
        
        cos_sims.sort(key=lambda x: x["cos_sim"], reverse=True)

        best = cos_sims[0]["cos_sim"]
        sector = cos_sims[0]["sector"]
        topRoles = list(map(
                lambda y: y["role"],
                filter(
                    lambda x: x["cos_sim"] > best - COS_SIM_EPSILON, 
                    cos_sims
                )
            ))
        return topRoles, sector
    
    roles, sector = getCloseRoles(job.role, role_embeddings)

    j = Job(job.id)
    j.upsert_job({
        "role_category": roles,
        "sector_category": sector,
        "job_processing": False
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
        preprocess_job_embeddings, #Embeds are so much faster, meaning we can actually use them in our search
        preprocess_job,
        solve_application,
        apply_to_job,
    ]

    while True:
        # For now, just round robin things in the queue, rlly needs a balancer and to be made asyncio lol, tho rn we're being rate limited
        for process_function in process_functions:
            try:
                process_function()
            except Exception as e:
                print(f"Failure With {process_function} {e}" )
                print("\x1b[44m")
                traceback.print_exc()
                print("\x1b[0m")
        sleep(0.5)
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