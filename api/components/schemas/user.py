from pydantic import BaseModel
from typing import Type, List, Any, Optional
from enum import Enum

from components.schemas.mongo import MongoBaseModel

class UserRoles(str, Enum):
    ADMIN = "Admin"
    CANDIDATE = "Candidate"
    AUTHENTICATED = "Authenticated"

class UserDataFields(BaseModel):
    firstname: Optional[str]
    surname: Optional[str]
    website: Optional[str]
    git: Optional[str]
    linkedIn: Optional[str]
    phone_number: Optional[str]
    pronouns: Optional[str]
    notice: Optional[str]
    expected_sallary: Optional[str]
    location: Optional[str]
    

class User(MongoBaseModel):
    name: str
    email: str
    permission: UserRoles

    # Data
    data: Optional[UserDataFields]