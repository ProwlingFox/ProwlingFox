from pymongo import errors as Mongoerrors
from bson.objectid import ObjectId

MIN_PASSWORD_LENGTH = 8

class User:
	def __init__(self, user_id):
		self.user_id = user_id
		return

	def get_info(self):
		from api import jobaiDB
		user_from_db = jobaiDB.users.find_one({"_id": ObjectId(self.user_id)})

		if not user_from_db:
			raise Exception("User Could Not Be Found In DB")

		user_data = {
			"user_id": str(user_from_db['_id']),
			"name": user_from_db['name'],
			"permission": user_from_db['permission'],
		}

		return {'success': True, 'data': user_data}

	def set_password(self, newpassword):
		if not User.validatePassword(newpassword):
			return {'success': False, 'error': "INSUFICCIENT_PASSWORD_STRENGTH"}

		import bcrypt
		hashedPassword = bcrypt.hashpw(newpassword.encode('utf-8'), bcrypt.gensalt())

		from api import jobaiDB
		userId = str( jobaiDB.users.update_one({"_id":ObjectId("6320f4498dd6e6071251de30")}, {"$set":{"password": hashedPassword}}) )

		return {'success': True}

	def get_job_reccomendations(self):
		# Right Now Just Gets 10 Jobs at random essentially
		from api import jobaiDB
		jobs_from_db = jobaiDB.jobs.find({}, limit=10)

		jobs = [];

		for job in jobs_from_db:
			jobs.append({
				"job_id": str(job['_id']),
				"jobTitle": job['jobTitle'],
				"company": job['company'],
				"longListing": job['longListing']
			})

		return {'success': True, 'data': jobs}

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
		from api import jobaiDB

		user_from_db = jobaiDB.users.find_one({"email": email})

		# Corfirm User Exists
		if not user_from_db:
			return {'success': False, 'error': 'AUTHENTICATION_FAILED'}

		# Check Password
		import bcrypt
		if not bcrypt.checkpw(password.encode('utf-8'), user_from_db['password']):
			return {'success': False, 'error': 'AUTHENTICATION_FAILED'}

		# Create JWT Token
		from components.secrets import secrets
		import jwt, time
		payload = {
			"expiry": int(time.time()) + 86400,
			"user_id": str(user_from_db['_id']),
			"permission": user_from_db['permission']
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
			"type": "user",
			"permission": "unverified"
		}

		try:
			from api import jobaiDB
			userId = str( jobaiDB.users.insert_one(user).inserted_id )
		except Mongoerrors.DuplicateKeyerror:
			return {'success': False, 'error': "USER_EXISTS"}

		return {'success': True, 'user_id': userId}

	@staticmethod
	def validateEmail(email: str) -> bool:
		return True

	@staticmethod
	def validatePassword(password: str) -> bool:
		if len(password) < MIN_PASSWORD_LENGTH:
			return False
		return True