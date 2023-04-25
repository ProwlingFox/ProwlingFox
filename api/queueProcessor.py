from multiprocessing import process
import components.secrets as secrets
secrets.init()

from time import sleep

from components.answeringEngine import AnsweringEngine
from components.job import Job
from components.user import User

#initialise DB
import components.db as db
db.init()
jobaiDB = db.jobaiDB

import components.schemas.job as JobSchema

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
            answer = AnsweringEngine.answer_question(job, user, question.ai_prompt or question.content)
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
    j = Job(job.id)
    print("preprocessing job: ", job.id)
    j.preprocess_job()
    return

process_queue = {
    "job_preprocessor": [],
    "application_processor": []
}

process_functions = {
    "job_preprocessor": preprocess_job,
    "application_processor": solve_application
}


reset_processing()
while True:
    # Work Out What Tasks to do
    # Tasks Include:
    # - Loading More Jobs into the system
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

    # For now, just round robin things in the queue, rlly needs a balancer 
    for process_type in process_queue:
        typed_process_queue = process_queue[process_type]
        if (len(typed_process_queue) > 0):
            process_functions[process_type](typed_process_queue.pop(0))
            
    sleep(0.5)
    print("Done One Round")
    continue

    

    

    
