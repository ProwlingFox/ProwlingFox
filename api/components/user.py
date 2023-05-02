import re
from fastapi import HTTPException
from pydantic import BaseModel
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

		print(u)

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
			'$lookup': { # Attach user's role preferences to the job
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
							'roles': '$job_preferences.roles.role'
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
			'$match': { # Get jobs where the roles Intersect
				'$expr': {
					'$gt': [
						{'$size': {
							'$ifNull': [
								{'$setIntersection': [
									{'$ifNull': [ "$role_category", [] ]},
									"$user.roles"
								]},
								[]
							]
						}},
						0,
					],
				}
			}
		}, {
			'$lookup': { # Attach applications to the job
				'from': 'applications', 
				'localField': '_id', 
				'foreignField': 'job_id', 
				'as': 'applications'
			}
		}, {
			'$match': { # Remove Jobs Where the user has applied
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
			'$limit': 10
		}
	])

		jobs = [];

		for job in jobs_from_db:
			try:
				jobs.append(JobSchema.JobSimplified.parse_obj(job))
			except Exception as e:
				print("Issue With Job ID:", job["_id"])
		return jobs

	def get_applications(self, getCompleted = False):
		from api import jobaiDB

		matchCriteria = {
			'user_id': self.user_id,
			'application_requested': True
		}

		if not getCompleted:
			matchCriteria['application_sent'] = False

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

	@staticmethod
	def authenticate_by_JWT(JWT: str):
		from components.secrets import secrets
		import jwt, time
		try:
			decoded_token = jwt.decode(JWT, secrets["JWT"]["Secret"], algorithms=secrets["JWT"]["Algorithm"])
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
			"email": user_from_db['email']
		}

		token = jwt.encode(payload, secrets["JWT"]["Secret"], algorithm=secrets["JWT"]["Algorithm"])

		return {'success': True, 'Token': token}

	@staticmethod
	def get_details_from_linkedIn(code: str):
		from components.secrets import secrets
		url = "https://www.linkedin.com/oauth/v2/accessToken"

		payload = {
			"grant_type": "authorization_code",
			"code": code,
			"client_id": secrets["LinkedIn"]["id"],
			"client_secret": secrets["LinkedIn"]["secret"],
			"redirect_uri": secrets["App_URL"] + "/login"
		}
		headers = {"Content-Type": "application/x-www-form-urlencoded"}
		oauth_response = requests.request("POST", url, data=payload, headers=headers)
		oauth = oauth_response.json()

		if "error" in oauth:
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
		token = jwt.encode(payload, secrets["JWT"]["Secret"], algorithm=secrets["JWT"]["Algorithm"])

		return {'success': True, 'Token': token}


	@staticmethod
	def create_user(name, email, password):
		if not User.validateEmail(email):
			return {'success': False, 'error': "INVALID_EMAIL"}

		if not User.validatePassword(password):
			return {'success': False, 'error': "INSUFICCIENT_PASSWORD_STRENGTH"}

		import bcrypt
		hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

		user = {
			"name": name,
			"email": email,
			"password": hashedPassword,
			"permission": "candidate"
		}

		try:
			from api import jobaiDB
			userId = str( jobaiDB.users.insert_one(user).inserted_id )
		except Mongoerrors.DuplicateKeyerror:
			return {'success': False, 'error': "USER_EXISTS"}

		return {'success': True, 'user_id': userId}
	
	@staticmethod
	def create_user_from_linkedin(code, oauth = None, userinfo = None):
		print("CREATING USER")
		if oauth == None and userinfo == None:
			oauth, userinfo = User.get_details_from_linkedIn(code)

		user = {
			"name": userinfo["name"],
			"email": userinfo["email"],
			"picture": userinfo["picture"],
			"password": None,
			"permission": "candidate",
			"linkedInID": userinfo["sub"]
		}

		try:
			from api import jobaiDB
			userId = str( jobaiDB.users.insert_one(user).inserted_id )
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