import logging
from schemas.job import ApplicationStatus

def setup_logger():
    # Create a custom filter class
    class ExcludeModuleFilter(logging.Filter):
        def __init__(self, module_name):
            super().__init__()
            self.module_name = module_name

        def filter(self, record):
            # Exclude log records from the specified module
            return not record.name.startswith(self.module_name)


    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create a formatter
    formatter = logging.Formatter('[%(name)s]%(asctime)s|%(levelname)s: %(message)s')

    exclude_filter = ExcludeModuleFilter("openai")
    logger.addFilter(exclude_filter)


    # Create a console handler and set the formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Create a file handler and set the formatter
    file_handler = logging.FileHandler('queue_processor.log', encoding='utf-8')
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return
setup_logger()

# 3rd Party Imports
import asyncio
import datetime
import openai
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

# EMPTY_ROLES = []

def reset_processing():
    # update all records, mark them as not currently being processed
    jobaiDB.applications.update_many({
        "status": ApplicationStatus.PROCESSING
    },{
        '$set': {'status': ApplicationStatus.REQUESTED}
    })
    jobaiDB.applications.update_many({
        "status": ApplicationStatus.SENDING
    },{
        '$set': {'status': ApplicationStatus.REVIEWED}
    })
    jobaiDB.jobs.update_many({
        "job_processing": True
    },{
        '$set': {'job_processing': False}
    })
    return

def solve_application():
    application_from_db = jobaiDB.applications.find_one_and_update({
        "status": ApplicationStatus.REQUESTED,
    },
    {
        '$set': {
            'status': ApplicationStatus.PROCESSING,
            'application_processing_ts': datetime.datetime.now()
        }
    })

    if not application_from_db:
         return False

    application = JobSchema.Application.parse_obj(application_from_db)

    job = Job(application.job_id).get_details()
    user = User(application.user_id).get_info()

    if not application.responses:
        application.responses = {}

    for question in job.questions:
        # If this question has a prefilled response allready, don't re-generate it
        if question.id in application.responses and application.responses[question.id]:
            if len(application.responses[question.id]):
                continue
        
        logging.info("answering question: " + question.id)
        try:
            answer = AnsweringEngine.answer_question(job, user, question)
            logging.debug(answer)
        except:
            logging.error("Question Failed To Answer")
        

        application.responses[question.id] = answer

    jobaiDB.applications.update_one({
        "_id": application.id,
    },
    {
        '$set': {
            'responses': application.responses,
            "status": ApplicationStatus.PROCESSED,
            'application_processed_ts': datetime.datetime.now()
        }
    })
    return True

def preprocess_job():
    job_to_preprocess_from_db = jobaiDB.jobs.find_one_and_update({
        "job_processing": {"$ne": True},
        "job_processing_failure": {"$ne": True},
        "$or": [
            {"short_description": None},
            {"role_description": None}
        ]
    },{
        '$set': {'job_processing': True}
    })

    if not job_to_preprocess_from_db:
        return False

    job = JobSchema.Job.parse_obj(job_to_preprocess_from_db)

    global role_embeddings
    j = Job(job.id)
    logging.info("preprocessing job: " + str(job.id))
    j.preprocess_job()
    return True

def load_jobSniffer(jobSnifferName):
	try:
		jsPlugin = __import__("JobsiteSniffers.%s" % jobSnifferName, globals(), locals(), [jobSnifferName], 0)
		js = getattr(jsPlugin, jobSnifferName)
		return js()
	except Exception as e:
		logging.error("Error with %s Plugin" % (jobSnifferName))
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
            logging.info("inserted: " + line)
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
        logging.info("inserted " + predefined_variable)
    return

def getRoleEmbeddings() -> List[Role]:
    return list(map(lambda x: Role.parse_obj(x),  jobaiDB.roles.find({}) ))

def get_jobs():
    global SECTORS_WHITELIST, MIN_JOB_PER_ROLE
    # Get The Roles that don't have enough jobs
    # TODO: This is a rlly expensive query, find a way to optimise it, prolly just by calling it less frequently lol
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
                    }
                ]
            }
        }
    ])

    for jobSniiffer in jobSniiffers:
        jobSniiffer.insert_one_job(roles_to_add)
    return

def apply_to_job():
    application_from_db = jobaiDB.applications.find_one_and_update({
        "status": ApplicationStatus.REVIEWED,
        "application_failed": {"$ne": True}
    },
    {
        '$set': {
            'status': ApplicationStatus.SENDING,
            'application_sending_ts': datetime.datetime.now()
        }
    })

    if not application_from_db:
        return False

    application = JobSchema.Application.parse_obj(application_from_db)
    job = Job(application.job_id).get_details()

    jobSniffer = load_jobSniffer(job.source)
    resp = jobSniffer.apply(job, application)

    if not (resp.status_code == 200 or resp.status_code == 201):
        mark_job_inactive(job.id)
        logging.warning("Application Failed")
        logging.warning(resp.text)
        jobaiDB.applications.update_one({
            "_id": application.id
        },{
            "$set": {
                'status': ApplicationStatus.REVIEWED,
                "application_failed": True
            }
        })
        return True

    jobaiDB.applications.update_one({
        "_id": application.id
    },{
         "$set": {
             'status': ApplicationStatus.SENT,
             'application_sent_ts': datetime.datetime.now(),
        }
    })
    return True

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
        return False

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
    return True

jobSniiffers = [
    load_jobSniffer("workableJobsniffer")
]

logging.info("Downloading Embeddings...")
# Load into memory to prevent expensive db calls, (Eventually lets implement a vector DB)
role_embeddings=getRoleEmbeddings()
logging.info("Embeddings Downloaded!")

async def main():
    process_functions = [
        get_jobs,
        preprocess_job_embeddings, #Embeds are so much faster, meaning we can actually use them in our search
        preprocess_job,
        solve_application,
        apply_to_job,
    ]

    while True:
        # For now, just round robin things in the queue, rlly needs a balancer and to be made asyncio lol, tho rn we're being rate limited
        function_had_something_to_do = False
        for process_function in process_functions:
            try:
                function_had_something_to_do = process_function() or function_had_something_to_do
            except Exception as e:
                logging.exception(f"Failure With {process_function} {e}" )
        
        # If Processor is sitting idling, don't waste too many packets calling DB
        if (not function_had_something_to_do):
            sleep(15)
        continue

if __name__ == "__main__":
    try:
        reset_processing()
        # fillRoleEmbeddings()
        # fillQuestionEmbeddings()
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Exiting Gracefully (Kbd Interrupt)...")
    except Exception as e:
        raise e