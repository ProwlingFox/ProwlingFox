from api import jobaiDB
import components.schemas.job as JobSchema

class metrics:
    @staticmethod
    def count_active_jobs() -> int:
        activeJobsCount = jobaiDB.jobs.count_documents({ "status": JobSchema.Status.ACTIVE.value })
        return activeJobsCount
    
    @staticmethod
    def count_users() -> int:
        userCount = jobaiDB.users.count_documents({})
        return userCount
    
    @staticmethod
    def count_applications() -> int:
        userCount = jobaiDB.applications.count_documents({ "applied": True })
        return userCount