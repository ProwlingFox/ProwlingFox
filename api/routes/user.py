from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from components.authentication import access_level
from components.user import User
import schemas.user as UserSchema

router = APIRouter(tags=["User"])


# Get current User
@router.get("/user")
@access_level("Candidate")
def get_current_user_data(req: Request):
	u = User(req.state.user_id)
	return u.get_info()


# Update User Password
class update_password(BaseModel):
    password: str

@router.post("/user/password")
@access_level("Authenticated")
def update_password(req: Request, p: update_password):
	u = User(req.state.user_id)
	return u.set_password(p.password)

# Create User
class create_user(BaseModel):
    name: str
    email: str
    password: str

@router.post("/user/create")
def create_user(u: create_user):
	return User.create_user(u.name, u.email, u.password)


# Login User Using Password
class pw_login_user(BaseModel):
	email: str
	password: str

@router.post("/user/login")
def login_user_using_pass(u: pw_login_user):
	return User.autenticate_by_email(u.email, u.password)

# Login User Using LinkedIn
class oauth_code(BaseModel):
	code: str

@router.post("/user/login/linkedin")
def login_user_using_linkedIn(o: oauth_code):
	return User.authenticate_by_linkedIn(o.code)

# Create User Using LinkedIn
@router.post("/user/create/linkedin")
def create_user_using_linkedIn(o: oauth_code):
	return User.create_user_from_linkedin(o.code)



# Update User Details
@router.post("/user/update")
@access_level("Authenticated")
def update_user_details(req: Request, ud: UserSchema.UpdateUserDetails):
	u = User(req.state.user_id)
	return u.update_details(ud)


@router.get("/user/metrics")
@access_level("Authenticated")
def get_user_metrics(req: Request):
	u = User(req.state.user_id)
	return u.get_metrics()

@router.post("/user/file/{filetype}/upload")
@access_level("Authenticated")
def update_user_details(req: Request):
	u = User(req.state.user_id)
	return 
