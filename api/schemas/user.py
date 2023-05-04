from traceback import print_tb
from matplotlib.pyplot import flag
from pydantic import BaseModel, Extra, validator
from typing import Type, List, Any, Optional
from enum import Enum

from schemas.mongo import MongoBaseModel
from schemas.configurations import City, Role

class UserRoles(str, Enum):
    ADMIN = "admin"
    CANDIDATE = "candidate"
    AUTHENTICATED = "authenticated"
    UNVERIFIED = "unverified"

class UserDataFields(BaseModel):
    firstname: Optional[str]
    surname: Optional[str]
    website: Optional[str]
    git: Optional[str]
    linkedIn: Optional[str]
    phone_number: Optional[str]
    pronouns: Optional[str]
    notice_period: Optional[str]
    expected_sallary: Optional[int]
    address: Optional[str]

class LocationCriteria(BaseModel):
    can_relocate: bool = False
    distance_km: int = 10

    remote_only: bool = False
    allowed_countries: list[str] = []
    city_preferences: list[City] = []
    strict_preferences: bool = False

# Todo: Add Blacklists
class UserJobPreferences(BaseModel):
    roles: list[Role] = []
    location: LocationCriteria = LocationCriteria()
    min_salary: Optional[int]


class User(MongoBaseModel):
    name: str
    email: str
    permission: UserRoles
    picture: str
    linkedInID: Optional[str]

    # Data
    data: UserDataFields = UserDataFields()
    job_preferences: UserJobPreferences = UserJobPreferences()

class CreateUser(User):
    password: Optional[str]

class UpdateUserDetails(BaseModel):
    name: Optional[str]
    # Data
    data: UserDataFields
    job_preferences: UserJobPreferences
    
    def flatten_dict(self, d=None, parent_key='', sep='.'):
        """
        Recursive helper function to flatten a dictionary with dot-separated keys.
        """
        flattened_dict = {}
        if d == {}:
            return d
        if not d:
            d = self.dict(exclude_unset = True, exclude_none = True)
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                flattened_dict.update(self.flatten_dict(v, new_key, sep))
            else:
                flattened_dict[new_key] = v
        return flattened_dict