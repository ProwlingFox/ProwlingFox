from fastapi import HTTPException, Request

# TODO: Enforce w/ pydantic
# Access Levels: 
 # Unauthenticated - Anyone can access
 # Authenticated - Only Signed in users can access
 # Candidate - Only Validated Users can access
 # Admin - Only Admins can access
def access_level(accessLevel):
	def wrapper(f):
		def wrapped_f(authCheck_request: Request, *args, **kwargs):

			#Check to see if Request in kwargs and add if not
			for param in inspect.signature(f).parameters:
				if inspect.signature(f).parameters[param].annotation == Request:
					kwargs[param] = authCheck_request

			if accessLevel == "Unauthenticated":
				return f(*args, **kwargs)

			authHeader = authCheck_request.headers.get("Authorization")
			if not authHeader:
				raise HTTPException(status_code=403, detail="AUTHORIZATION_HEADER_REQUIRED")

			if not authHeader.startswith("Bearer"):
				raise HTTPException(status_code=403, detail="MALFORMED_AUTHORIZATION_HEADER")

			JWT = authHeader[7:]
			from components.user import User
			user = User.authenticate_by_JWT(JWT)

			if not user['success']:
				raise HTTPException(status_code=403, detail="INVALID_AUTHORIZATION_HEADER")

			authCheck_request.state.user_id = user['user_id']
			authCheck_request.state.permission = user['permission']

			if accessLevel == "Authenticated":
				return f(*args, **kwargs)

			if accessLevel == "Candidate":
				if user['permission'] in ["Candidate", "Admin"]:
					return f(*args, **kwargs)

			if accessLevel == "Admin":
				if user['permission'] == "Admin":
					return f(*args, **kwargs)

			raise HTTPException(status_code=403, detail="USER_UNAUTHORIZED")

		# Weird Jiggery Pokery to get the function returned by this decorator to display
		# like the origional function to the framework. :#
		wrapped_f.__name__ = f.__name__

		import inspect
		wrapped_f.__signature__ = inspect.Signature(
			parameters = [
				# Use all parameters from handler
				*inspect.signature(f).parameters.values(),

				# Skip *args and **kwargs from wrapper parameters:
				*filter(
					lambda p: p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD),
					inspect.signature(wrapped_f).parameters.values()
				)
			],
			return_annotation = inspect.signature(f).return_annotation,
		)

		return wrapped_f
	return wrapper


