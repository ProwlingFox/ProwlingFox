from ast import alias
from bson import ObjectId
from schemas.configurations import B64_File
import schemas.job as JobSchema
from components.db import prowling_fox_db


# Must return an itterator when called for that returns a new job, defined above.
# Must implement the apply function that takes a job and applys to it
# May Implement SaveProgress, which allows the plugin to save arbitrary dictionaries to the database as JSON, This allows for recording
# If jobsniffer cannot return a job, i.e No Jobs Left/RateLimiting then it should throw an error
# When Finding new jobs, an optional search term arg may be sent, i.e. "Software Engineer", the Jobsniffer MUST query using that search term, If the sniffer is unable to query using that search term it must return the Exception Not Implemented, and it will be passed over for that search query, if it can never be searched, then searchable: false should be added in secrets.json and it will only be looked up generically

class baseJobsniffer:
    country_alias_list = None

    def __init__(self, config, override = False):
        self.config = config

        # Error Out if the config is disabled
        if (not config["enabled"] and not override):
            raise Exception(self.__class__.__name__ + " Module Is Disabled In Secrets.Json")
    
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

    def apply():
        return
    
class OutOfJobs(Exception):
    def __init__(self, message='No More Jobs Left'):
        # Call the base class constructor with the parameters it needs
        super(OutOfJobs, self).__init__(message)
