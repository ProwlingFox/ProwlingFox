from datetime import timedelta, datetime
from typing import List
from fastapi import HTTPException
from pymongo import errors as Mongoerrors
from bson.objectid import ObjectId
import schemas.job as JobSchema
import schemas.user as UserSchema
import requests

MIN_PASSWORD_LENGTH = 8

class User:
    def __init__(self, user_id):
        self.user_id = ObjectId(user_id)
        return

    def get_info(self):
        from api import jobaiDB
        user_from_db = jobaiDB.users.find_one({"_id": self.user_id})

        if not user_from_db:
            raise Exception("User Could Not Be Found In DB")

        return UserSchema.User.parse_obj(user_from_db)

    def set_password(self, newpassword):
        if not User.validatePassword(newpassword):
            return {'success': False, 'error': "INSUFICCIENT_PASSWORD_STRENGTH"}

        import bcrypt
        hashedPassword = bcrypt.hashpw(newpassword.encode('utf-8'), bcrypt.gensalt())

        from api import jobaiDB
        update_response = jobaiDB.users.update_one({"_id":self.user_id}, {"$set":{"password": hashedPassword}})

        return {'success': True}

    def update_details(self, details):
        u = UserSchema.UpdateUserDetails.parse_obj(details)

        from components.db import prowling_fox_db as jobaiDB
        try:
            update_response = jobaiDB.users.update_one({"_id":self.user_id}, {"$set": u.flatten_dict()})
            return {'success': True}
        except Exception as e:
            raise

    def get_job_reccomendations(self):
        # Right Now Just Gets 10 Jobs at random essentially, filtering out those marked as read
        from api import jobaiDB
        # jobs_from_db = jobaiDB.jobs.find({}, limit=10)
        jobs_from_db = jobaiDB.jobs.aggregate([
            {
                '$lookup': {
                    'from': 'users', 
                    'let': {
                        'user_id': self.user_id
                    }, 
                    'pipeline': [
                        {
                            '$match': {
                                '$expr': {
                                    '$eq': [
                                        '$_id', '$$user_id'
                                    ]
                                }
                            }
                        }, {
                            '$project': {
                                'roles': '$job_preferences.roles.role', 
                                'countries': '$job_preferences.location.country_preferences.country_code', 
                                'city': '$job_preferences.location.city_preferences'
                            }
                        }
                    ], 
                    'as': 'user'
                }
            }, {
                '$unwind': {
                    'path': '$user'
                }
            }, {
                '$match': {
                    '$expr': {
                        '$and': [
                            {
                                '$gt': [
                                    {
                                        '$size': {
                                            '$ifNull': [
                                                {
                                                    '$setIntersection': [
                                                        {
                                                            '$ifNull': [
                                                                '$role_category', []
                                                            ]
                                                        }, '$user.roles'
                                                    ]
                                                }, []
                                            ]
                                        }
                                    }, 0
                                ]
                            }, {
                                '$in': [
                                    '$location.country', '$user.countries'
                                ]
                            }
                        ]
                    }
                }
            }, {
                '$lookup': {
                    'from': 'applications', 
                    'localField': '_id', 
                    'foreignField': 'job_id', 
                    'as': 'applications'
                }
            }, {
                '$match': {
                    'applications': {
                        '$not': {
                            '$elemMatch': {
                                'user_id': self.user_id
                            }
                        }
                    }, 
                    'short_description': {
                        '$ne': None
                    }
                }
            }, {
                '$sort': {
                    '_id': -1
                }
            }, {
                '$facet': {
                    'count': [
                        {
                            '$count': 'total'
                        }
                    ], 
                    'results': [
                        {
                            '$limit': 10
                        }
                    ]
                }
            }, {
                '$project': {
                    'count': {
                        '$arrayElemAt': [
                            '$count.total', 0
                        ]
                    }, 
                    'results': 1
                }
            }
        ])

        jobs = [];
        count = 0

        try:
            document = jobs_from_db.next()
            count = 0
            if "count" in document:
                count = document["count"]
            for job in document["results"]:
                try:
                    jobs.append(JobSchema.JobSimplified.parse_obj(job))
                except Exception as e:
                    print("Issue With Job ID:", job["_id"])
        except StopIteration:
            pass

        return {
            "totalJobs": count,
            "jobs": jobs
        }

    def get_applications(self, getSent = False) -> List[JobSchema.Application]:
        from api import jobaiDB

        matchCriteria = {
            'user_id': self.user_id,
            'application_requested': True
        }

        if not getSent:
            matchCriteria['application_sent'] = {"$ne": True}

        applications_from_db = jobaiDB.applications.aggregate([
            {
                '$match': matchCriteria
            },
            {
                '$lookup': {
                    'from': 'jobs',
                    'localField': 'job_id',
                    'foreignField': '_id',
                    'as': 'job'
                }
            },
            {"$unwind": {
                    "path": "$job",
                    "preserveNullAndEmptyArrays": False
                }
            },
            { "$sort": { "_id": -1 }}
        ])

        applications = [];

        for application in applications_from_db:
            # pprint(application)
            application["id"] = str(application["_id"])
            application["user_id"] = str(application["user_id"])
            application["job_id"] = str(application["job_id"])


            try:
                applications.append(JobSchema.Application.parse_obj(application))
            except Exception as e:
                print("Issue with jobID " + application["job_id"])

        return applications

    def get_application(self, job_id):
        from components.db import prowling_fox_db
        applications_from_db = prowling_fox_db.applications.aggregate([
            {
                '$match': {
                    'user_id': self.user_id,
                    'job_id': ObjectId(job_id)
                }
            },
            {
                '$lookup': {
                    'from': 'jobs',
                    'localField': 'job_id',
                    'foreignField': '_id',
                    'as': 'job'
                }
            },
            {"$unwind": {
                    "path": "$job",
                    "preserveNullAndEmptyArrays": False
                }
            }
        ])
        
        try:
            return JobSchema.Application.parse_obj(applications_from_db.next())
        except StopIteration:
            return {}

    def get_metrics(self):
        from components.db import prowling_fox_db
        # Number of job applications sent today, 
        now = datetime.now()
        past_day = now - timedelta(days=1)

        applicationsToday = prowling_fox_db.applications.count_documents({
            "user_id": self.user_id,
            "application_sent": True,
            "application_sent_ts": {"$gte": past_day}
        })
        return {"applicationsToday": applicationsToday}

    def export_applications_as_csv(self):
        import csv, io
        applications = self.get_applications(True)

        f = io.StringIO()
        w = csv.DictWriter(f, ["ID", "Role", "Company", "Status", "TimeStamp", "URL"])

        for app in applications:
            w.writerow({
                "ID": app.id,
                "Role": app.job.role,
                "Company": app.job.company.name,
                "URL": app.job.src_url,
                "Status":  "SENT" if app.application_sent else ("AWAITING REVIEW" if app.application_processed else "PROCESSING"),
                "TimeStamp": app.application_sent_ts if app.application_sent else (app.application_processed_ts if app.application_processed else app.application_requested_ts),
            })
        return f.getvalue()

    @staticmethod
    def authenticate_by_JWT(JWT: str):
        from components.secrets import secrets
        import jwt, time
        try:
            decoded_token = jwt.decode(JWT, secrets["JWT_SECRET"], algorithms=secrets["JWT_ALG"])
        except Exception as e:
            return {'success': False, 'error': 'INVALID_TOKEN'}
        if decoded_token['expiry'] < time.time():
            return {'success': False, 'error': 'EXPIRED_TOKEN'}
        return {'success': True, 'user_id': decoded_token['user_id'], 'permission': decoded_token['permission']}

    @staticmethod
    def autenticate_by_email(email: str, password: str):
        from components.db import prowling_fox_db
        user_from_db = prowling_fox_db.users.find_one({"email": email})

        # Corfirm User Exists
        if not user_from_db:
            return {'success': False, 'error': 'AUTHENTICATION_FAILED'}

        # Check Password
        import bcrypt
        if not user_from_db['password'] or (not bcrypt.checkpw(password.encode('utf-8'), user_from_db['password'])):
            return {'success': False, 'error': 'AUTHENTICATION_FAILED'}

        # Create JWT Token
        from components.secrets import secrets
        import jwt, time
        payload = {
            "expiry": int(time.time()) + 86400,
            "user_id": str(user_from_db['_id']),
            "permission": user_from_db['permission'],
            "name": user_from_db['name'],
            "profileImage": user_from_db["picture"],
            "email": user_from_db['email']
        }

        token = jwt.encode(payload, secrets["JWT_SECRET"], algorithm=secrets["JWT_ALG"])

        return {'success': True, 'Token': token}

    @staticmethod
    def get_details_from_linkedIn(code: str):
        from components.secrets import secrets
        url = "https://www.linkedin.com/oauth/v2/accessToken"

        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": secrets["PUBLIC_LINKEDIN_CLIENT_ID"],
            "client_secret": secrets["LINKEDIN_CLIENT_SECRET"],
            "redirect_uri": secrets["PUBLIC_APP_URL"] + "/login"
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        oauth_response = requests.request("POST", url, data=payload, headers=headers)
        oauth = oauth_response.json()

        if "error" in oauth:
            print(oauth, payload)
            raise HTTPException(400, "OAUTH_CODE_INVALID")

        url = "https://api.linkedin.com/v2/userinfo"
        headers = {"Authorization": "Bearer " + oauth["access_token"]}
        userinfo_response = requests.request("GET", url, headers=headers)
        userinfo = userinfo_response.json() 
        return oauth, userinfo

    @staticmethod
    def authenticate_by_linkedIn(code: str):
        oauth, userinfo = User.get_details_from_linkedIn(code)

        from components.db import prowling_fox_db
        user_from_db = prowling_fox_db.users.find_one({"linkedInID": userinfo["sub"]})

        if not user_from_db:
            u = User.create_user_from_linkedin(code, oauth, userinfo)
            if u["success"]:
                user_from_db = prowling_fox_db.users.find_one({"_id": ObjectId(u["user_id"])})
            else:
                raise HTTPException(500, "COULD_NOT_CREATE_USER")

        # Create JWT Token
        from components.secrets import secrets
        import jwt, time
        payload = {
            "expiry": int(time.time()) + oauth["expires_in"],
            "user_id": str(user_from_db['_id']),
            "permission": user_from_db['permission'],
            "name": user_from_db['name'],
            "email": user_from_db['email'],
            "profileImage": user_from_db["picture"],
            "linkedInAccessKey": oauth["access_token"],
        }
        token = jwt.encode(payload, secrets["JWT_SECRET"], algorithm=secrets["JWT_ALG"])

        return {'success': True, 'Token': token}

    @staticmethod
    def create_user(name, email, password):
        if not User.validateEmail(email):
            return {'success': False, 'error': "INVALID_EMAIL"}

        if not User.validatePassword(password):
            return {'success': False, 'error': "INSUFICCIENT_PASSWORD_STRENGTH"}

        import bcrypt
        hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user = UserSchema.CreateUser(
            name = name,
            email = email,
            picture = None,
            password = hashedPassword,
            permission = "unverified",
        )

        try:
            from api import jobaiDB
            userId = str( jobaiDB.users.insert_one(user.dict()).inserted_id )
        except Mongoerrors.DuplicateKeyerror:
            return {'success': False, 'error': "USER_EXISTS"}

        return {'success': True, 'user_id': userId}
    
    @staticmethod
    def create_user_from_linkedin(code, oauth = None, userinfo = None):
        print("CREATING USER")
        if oauth == None and userinfo == None:
            oauth, userinfo = User.get_details_from_linkedIn(code)

        user = UserSchema.CreateUser(
            name = userinfo["name"],
            email = userinfo["email"],
            picture = userinfo["picture"],
            password = None,
            permission = "unverified",
            linkedInID = userinfo["sub"],
        )

        try:
            from api import jobaiDB
            userId = str( jobaiDB.users.insert_one(user.dict()).inserted_id )
        except Mongoerrors.DuplicateKeyerror:
            return {'success': False, 'error': "USER_EXISTS"}
        except Mongoerrors:
            return {'success': False, 'error': "OTHER_DB_ERROR"}

        return {'success': True, 'user_id': userId}

    @staticmethod
    def validateEmail(email: str) -> bool:
        return True

    @staticmethod
    def validatePassword(password: str) -> bool:
        if len(password) < MIN_PASSWORD_LENGTH:
            return False
        return True