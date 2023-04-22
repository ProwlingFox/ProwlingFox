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

# update all records, mark them as not currently being processed
jobaiDB.applications.update_many({
    "application_processing": True
},{
    '$set': {'application_processing': False}
})

def solve_application(application: JobSchema.Application):
    job = Job(application.job_id).get_details()
    user = User(application.user_id).get_info()

    answered_questions = {}

    for question in job.questions:
        print("answering question:", question.id)
        if question.type == JobSchema.FieldType.TEXT:
            answer = AnsweringEngine.answer_question(job, user, question.content)
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

while True:
    # Work Out What Tasks to do
    # Tasks Include:
    # - Loading More Jobs into the system
    # - Pre-Resolving said jobs
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

    if not application_from_db:
        sleep(0.5)
        print("No More Applications")
        continue

    application = JobSchema.Application.parse_obj(application_from_db)
    # Preform Task

    

    

    
