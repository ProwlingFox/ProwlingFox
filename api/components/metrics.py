from typing import List
from components.db import prowling_fox_db
import schemas.job as JobSchema
from schemas.configurations import Role

class metrics:
    @staticmethod
    def count_active_jobs() -> int:
        activeJobsCount = prowling_fox_db.jobs.count_documents({ "status": JobSchema.Status.ACTIVE.value })
        return activeJobsCount
    
    @staticmethod
    def count_processed_jobs() -> int:
        processed_jobs_count = prowling_fox_db.jobs.count_documents({ "short_description": {"$ne": None}, "status": JobSchema.Status.ACTIVE.value })
        return processed_jobs_count

    @staticmethod
    def count_users() -> int:
        userCount = prowling_fox_db.users.count_documents({})
        return userCount
    
    @staticmethod
    def count_applications() -> int:
        userCount = prowling_fox_db.applications.count_documents({ "applied": True })
        return userCount

    @staticmethod
    def get_roles() -> List[Role]:
        roles_from_db = prowling_fox_db.roles.find({}, projection={ "embedding": 0, "_id": 0 })
        return list(map(lambda x:Role.parse_obj(x), roles_from_db))
    
    @staticmethod
    def get_locations():
        locations_from_db = prowling_fox_db.locations.find({}, projection={"_id": 0})
        return list(locations_from_db)
        