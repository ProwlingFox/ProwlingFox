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
    notice_period: Optional[str]
    expected_sallary: Optional[int]
    location: Optional[str]
    address: Optional[str]
    
class city(BaseModel):
    city: str
    region: Optional[str]
    country: str

class LocationCriteria(BaseModel):
    can_relocate: bool
    distance_km: int

    remote_only: bool
    allowed_countries: list[str]
    city_preferences: Optional[list[city]]
    strict_preferences: bool

class Role(BaseModel):
    role: str
    sector: str

# Todo: Add Blacklists
class UserJobPreferences(BaseModel, extra=Extra.forbid):
    roles: list[Role]
    location: Optional[LocationCriteria]
    min_salary: int


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