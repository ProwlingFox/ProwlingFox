from typing import List
from schemas.job import ApplicationStatus
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
        user_count = prowling_fox_db.users.count_documents({})
        return user_count
    
    @staticmethod
    def count_applications() -> int:
        application_count = prowling_fox_db.applications.count_documents({ "application_sent_ts": {"$ne": None} })
        return application_count
    
    @staticmethod
    def get_openAI_usage():
        openAI_usage = prowling_fox_db.openai_request_log.aggregate([
            {
                '$match': {
                    'success': True
                }
            }, {
                '$group': {
                    '_id': {
                        'date': {
                            '$dateToString': {
                                'format': '%Y-%m-%d', 
                                'date': '$sent_ts'
                            }
                        }, 
                        'model': '$model', 
                        'note': '$note'
                    }, 
                    'prompt_tokens': {
                        '$sum': {
                            '$add': '$prompt_tokens'
                        }
                    }, 
                    'completion_tokens': {
                        '$sum': {
                            '$add': '$completion_tokens'
                        }
                    }, 
                    'total_tokens': {
                        '$sum': {
                            '$add': '$total_tokens'
                        }
                    }, 
                    'count': {
                        '$sum': 1
                    }
                }
            }, {
                '$project': {
                    '_id': 0,
                    'date': '$_id.date',
                    'model': '$_id.model',
                    'label': '$_id.note',
                    'prompt_tokens': 1,
                    "completion_tokens": 1,
                    "total_tokens": 1,
                    "count": 1
                }
            }
        ])
        return list(openAI_usage)

    @staticmethod
    def get_average_questions():
        question_count = prowling_fox_db.jobs.aggregate([
            {
                '$match': {
                    'short_description': {
                        '$ne': None
                    }
                }
            }, {
                '$project': {
                    'ai_question_count': {
                        '$filter': {
                            'input': '$questions', 
                            'as': 'q', 
                            'cond': {
                                '$and': [
                                    {
                                        '$in': [
                                            '$$q.type', [
                                                'Text', 'LongText'
                                            ]
                                        ]
                                    }, {
                                        '$eq': [
                                            '$$q.response', None
                                        ]
                                    }
                                ]
                            }
                        }
                    }
                }
            }, {
                '$project': {
                    'ai_question_count': {
                        '$size': '$ai_question_count'
                    }
                }
            }, {
                '$group': {
                    '_id': 'Average AI Questions', 
                    'avg': {
                        '$avg': '$ai_question_count'
                    }
                }
            }
        ])
        return question_count.next()["avg"]

    @staticmethod
    def get_roles() -> List[Role]:
        roles_from_db = prowling_fox_db.roles.find({}, projection={ "embedding": 0, "_id": 0 })
        return list(map(lambda x:Role.parse_obj(x), roles_from_db))
    
    @staticmethod
    def get_locations():
        locations_from_db = prowling_fox_db.locations.find({}, projection={"_id": 0})
        return list(locations_from_db)
        