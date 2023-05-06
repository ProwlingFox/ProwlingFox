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

    def __init__(self, config):
        self.config = config

        # Error Out if the config is disabled
        if (not config["enabled"]):
            raise Exception(self.__class__.__name__ + " Module Is Disabled In Secrets.Json")
    
        return
    
    # Gets updates to a job i.e. status change
    def getUpdates(jobID):
        return
    
    def load_preset_file(self, preset: str):
        print(preset)
        header, presetType = preset.split(",", 1)
        x, userId = header.split(":", 1)

        file_from_db = prowling_fox_db.users.find_one({"_id": ObjectId(userId)}, {"data": "$data.resume.data", "file_name": "$data.resume.file_name"})
        if not file_from_db:
            raise Exception("User doesn't exist.")

        try:
            file = B64_File.parse_obj(file_from_db)
        except ValueError:
            raise Exception("File doesn't exist.")

        return file.data.split(",", 1)
        
    def apply():
        return
    
class OutOfJobs(Exception):
    def __init__(self, message='No More Jobs Left'):
        # Call the base class constructor with the parameters it needs
        super(OutOfJobs, self).__init__(message)
