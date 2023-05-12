import io
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Type, List

from components import authentication
from components.user import User
import schemas.user as UserSchema

router = APIRouter(tags=["User"])


# Get current User
@router.get("/user")
@authentication.access_level("Candidate")
def get_current_user_data(req: Request):
	u = User(req.state.user_id)
	return u.get_info()


# Update User Password
class update_password(BaseModel):
    password: str

@router.post("/user/password")
@authentication.access_level("Authenticated")
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
@authentication.access_level("Authenticated")
def update_user_details(req: Request, ud: UserSchema.UpdateUserDetails):
	u = User(req.state.user_id)
	return u.update_details(ud)

@router.get("/user/applications")
@authentication.access_level("Authenticated")
def get_user_applications(req: Request, showSent: bool = False):
	u = User(req.state.user_id)
	return u.get_applications(showSent)

@router.get("/user/applications/{job_id}")
@authentication.access_level("Authenticated")
def get_user_applications(req: Request, job_id: str):
	u = User(req.state.user_id)
	return u.get_application(job_id)

@router.get("/user/metrics")
@authentication.access_level("Authenticated")
def get_user_metrics(req: Request):
	u = User(req.state.user_id)
	return u.get_metrics()

@router.post("/user/file/{filetype}/upload")
@authentication.access_level("Authenticated")
def update_user_details(req: Request):
	u = User(req.state.user_id)
	return 

@router.get("/user/data/applications", response_class=StreamingResponse)
@authentication.access_level("Authenticated")
def export_applications(req: Request):
	u = User(req.state.user_id)
	stream = io.StringIO(u.export_applications_as_csv())
	response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
	response.headers["Content-Disposition"] = "attachment; filename=Applications.csv"

	return response