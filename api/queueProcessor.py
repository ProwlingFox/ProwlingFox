from pprint import pprint
import components.secrets as secrets
secrets.init()

#initialise DB
import components.db as db
db.init()
jobaiDB = db.jobaiDB

# update all records, mark them as not currently being processed
jobaiDB.applications.update_many({
    "application_processing": True
},{
    '$set': {'application_processing': False}
})

while True:
    # Work Out What Tasks to do
    application_to_process = jobaiDB.applications.find_one_and_update({
        "application_requested": True,
        "application_processing": False,
        "application_processed": False
    },
    {
        '$set': {'application_processing': True}
    })

    job_from_db = jobaiDB.jobs.find_one({"_id": application_to_process["job_id"]})
    user_from_db = jobaiDB.users.find_one({"_id": application_to_process["user_id"]})


    pprint(application_to_process)
    pprint(job_from_db)
    pprint(user_from_db)
    # Preform Task



    break