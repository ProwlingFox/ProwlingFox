import logging
from bson import ObjectId
from schemas.configurations import B64_File
import schemas.job as JobSchema

from components.db import prowling_fox_db
from pymongo import errors as MongoErrors


# Must return an itterator when called for that returns a new job, defined above.
# Must implement the apply function that takes a job and applys to it
# May Implement SaveProgress, which allows the plugin to save arbitrary dictionaries to the database as JSON, This allows for recording
# If jobsniffer cannot return a job, i.e No Jobs Left/RateLimiting then it should throw an error
# When Finding new jobs, an optional search term arg may be sent, i.e. "Software Engineer", the Jobsniffer MUST query using that search term, If the sniffer is unable to query using that search term it must return the Exception Not Implemented, and it will be passed over for that search query, if it can never be searched, then searchable: false should be added in secrets.json and it will only be looked up generically

class baseJobsniffer:
    country_alias_list = None
    empty_roles_location = []

    def __init__(self):
        return
    
    # Gets updates to a job i.e. status change
    def getUpdates(jobID):
        return
    
    def load_preset_file(self, preset: str):
        header, presetType = preset.split(",", 1)
        x, userId = header.split(":", 1)

        file_from_db = prowling_fox_db.users.find_one({"_id": ObjectId(userId)}, {"data": "$data.resume.File.data", "file_name": "$data.resume.File.file_name"})
        if not file_from_db:
            raise Exception("User doesn't exist.")

        try:
            file = B64_File.parse_obj(file_from_db)
        except ValueError:
            raise Exception("File doesn't exist.")

        return file.data
        
    def get_country_alias_list(self):
        aliases_from_db = list(prowling_fox_db.locations.aggregate(
            [
                {
                    '$project': {
                        'country_code': 1, 
                        'alias': {
                            '$concatArrays': [
                                '$aliases', [
                                    '$name'
                                ], [
                                    '$country_code'
                                ]
                            ]
                        }
                    }
                }, {
                    '$unwind': {
                        'path': '$alias'
                    }
                }
            ]
        ))

        self.country_alias_list = {}
        for alias in aliases_from_db:
            self.country_alias_list[alias["alias"]] = alias["country_code"]
        return
    
    def attempt_get_country(self, country: str):
        if not self.country_alias_list:
            self.get_country_alias_list()

        if country in self.country_alias_list:
            return self.country_alias_list[country]

        return country

    def saveJobSniffer(self, saveData):
        db_response = prowling_fox_db.jobsniffer_save.update_one(
			{"_id": self.__class__.__name__},
			{"$set": saveData},
            upsert=True
        )
        return db_response

    def getJobSnifferSave(self):
        db_response = prowling_fox_db.jobsniffer_save.find_one(
			{"_id": self.__class__.__name__}
        )
        return db_response

    def get_one_job():
        raise NotImplementedError("Child Class Must Implement get_one_job")

    def insert_one_job(self, roles_to_add):
        while True:
            try:
                role_to_add = roles_to_add.next()
                searchQuery = role_to_add["role"]
                locationQuery = role_to_add["country_code"]

                if not searchQuery+":"+locationQuery in self.empty_roles_location:
                    break
            except StopIteration:
                return


        while True:
            try:
                job = JobSchema.Job.parse_obj(self.get_one_job(searchQuery, locationQuery))
                resp = prowling_fox_db.jobs.insert_one(job.dict())
                logging.info(f"Inserted Job From {job.company.name} Into DB | ID:{resp.inserted_id}")
                return True
            except OutOfJobs:
                logging.warning("That Query Is Out Of Jobs")
                self.empty_roles_location.append(searchQuery+":"+locationQuery)
                return False
            except MongoErrors.DuplicateKeyError:
                logging.warning("Job Allready Existed")

    def apply():
        return
    
class OutOfJobs(Exception):
    def __init__(self, message='No More Jobs Left'):
        # Call the base class constructor with the parameters it needs
        super(OutOfJobs, self).__init__(message)
