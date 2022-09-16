from fastapi import HTTPException, Request

# TODO: Enforce w/ pydantic
# Access Levels: 
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

			user = decodeJWT( authCheck_request.headers.get("Authorization") )

			authCheck_request.state.user_id = user['user_id']
			authCheck_request.state.permission = user['permission']

			if hasAccess(user['permission'], accessLevel):
				return f(*args, **kwargs)
			else:
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


def hasAccess(userAccessLevel, requiredAccessLevel):
	userAccessLevel = userAccessLevel.lower()
	requiredAccessLevel = requiredAccessLevel.lower()

	if requiredAccessLevel == "authenticated":
		if userAccessLevel in ["unverified","candidate", "admin"]:
			return True

	if requiredAccessLevel == "candidate":
		if userAccessLevel in ["candidate", "admin"]:
			return True

	if requiredAccessLevel == "admin":
		if userAccessLevel == "admin":
			return True

	return False


def decodeJWT(auth_token: str):
	if not auth_token:
		raise HTTPException(status_code=403, detail="AUTHORIZATION_HEADER_REQUIRED")

	if not auth_token.startswith("Bearer"):
		raise HTTPException(status_code=403, detail="MALFORMED_AUTHORIZATION_HEADER")

	JWT = auth_token[7:]
	from components.user import User
	user = User.authenticate_by_JWT(JWT)

	if not user['success']:
		raise HTTPException(status_code=403, detail="INVALID_AUTHORIZATION_HEADER")

	return user