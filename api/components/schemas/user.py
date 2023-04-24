from pydantic import BaseModel, Extra, validator
from typing import Type, List, Any, Optional
from enum import Enum

from components.schemas.mongo import MongoBaseModel

class UserRoles(str, Enum):
    ADMIN = "admin"
    CANDIDATE = "candidate"
    AUTHENTICATED = "authenticated"

class UserDataFields(BaseModel, extra=Extra.forbid):
    firstname: Optional[str]
    surname: Optional[str]
    website: Optional[str]
    git: Optional[str]
    linkedIn: Optional[str]
    phone_number: Optional[str]
    pronouns: Optional[str]
    notice: Optional[str]
    expected_sallary: Optional[int]
    location: Optional[str]
    
class UserJobPreferences(BaseModel, extra=Extra.forbid):
    roles: list[str]
    sector: str
    locations: list[str]
    remote: bool
    salary: int

class User(MongoBaseModel):
    name: str
    email: str
    permission: UserRoles

    # Data
    data: Optional[UserDataFields]
    job_preferences: Optional[UserJobPreferences]

class UpdateUserDetails(BaseModel, extra=Extra.forbid):
    name: Optional[str]
    # Data
    data: Optional[UserDataFields]
    job_preferences: Optional[UserJobPreferences]
    
    def flatten_dict(self, d=None, parent_key='', sep='.'):
        """
        Recursive helper function to flatten a dictionary with dot-separated keys.
        """
        flattened_dict = {}
        if not d:
            d = self.dict(exclude_unset = True, exclude_none = True)
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                flattened_dict.update(self.flatten_dict(v, new_key, sep))
            else:
                flattened_dict[new_key] = v
        return flattened_dict