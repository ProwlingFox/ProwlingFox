from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from typing import Type, List

from components import authentication
from components.user import User

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

@router.put("/user/password")
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


# Login User
class pw_login_user(BaseModel):
	email: str
	password: str

@router.post("/user/login")
def login_user_using_pass(u: pw_login_user):
	return User.autenticate_by_email(u.email, u.password)


# Update User Details
class user_job_preferences(BaseModel):
	roles: List[str] = None
	locations: List[str] = None
	remote: bool = None
	salary: int = None

class user_details(BaseModel):
	name: str
	tel: str = None
	pronouns: str = None
	job_preferences: user_job_preferences = None

@router.put("/user/update")
@authentication.access_level("Authenticated")
def update_user_details(req: Request, ud: user_details):
	u = User(req.state.user_id)
	return u.update_details(ud)