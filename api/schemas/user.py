from datetime import date
from pydantic import BaseModel, create_model
from typing import Optional
from enum import Enum

from schemas.mongo import MongoBaseModel
from schemas.configurations import City, Role, B64_File

class UserRoles(str, Enum):
    ADMIN = "admin"
    CANDIDATE = "candidate"
    AUTHENTICATED = "authenticated"
    UNVERIFIED = "unverified"

Data_Field_Conversion = {
    "Text": str,
    "Number": int,
    "Date": date,
    "File": B64_File,
    "Checkbox": bool
}

class BaseDataField(BaseModel):
    pass

# Prevents Duplicate Models (Causes FASTAPI Problems)
modelCache = {}

def DataField(types):
    class_dict = {}
    for var in types:
        if var in Data_Field_Conversion:
            class_dict[var] = (Data_Field_Conversion[var], None)
        else:
            raise Exception(f"Type {var} Not Supported")

    if 'DataField' + "".join(types) in modelCache:
        return modelCache['DataField' + "".join(types)]
    
    model = create_model(
        'DataField' + "".join(types),
        **class_dict,
        __base__=BaseDataField
    )
    modelCache['DataField' + "".join(types)] = model
    return model


class UserDataFields(BaseModel):
    firstname: DataField(["Text"]) = DataField(["Text"])()
    surname: DataField(["Text"]) = DataField(["Text"])()
    website: DataField(["Text"]) = DataField(["Text"])()
    git: DataField(["Text"]) = DataField(["Text"])()
    linkedIn: DataField(["Text"]) = DataField(["Text"])()
    phone_number: DataField(["Text"]) = DataField(["Text"])()
    pronouns: DataField(["Text"]) = DataField(["Text"])()
    notice_period: DataField(["Text", "Number"]) = DataField(["Text", "Number"])()
    expected_salary: DataField(["Text", "Number"]) = DataField(["Text", "Number"])()
    address: DataField(["Text"]) = DataField(["Text"])()
    resume: DataField(["File"]) = DataField(["File"])()
    headline: DataField(["Text"]) = DataField(["Text"])()
    pass

class CountryPreference(BaseModel):
    country_code: str
    has_visa: bool

class LocationCriteria(BaseModel):
    remote_only: bool = False
    country_preferences: list[CountryPreference] = []
    city_preferences: list[City] = []
    strict_preferences: bool = False

# Todo: Add Blacklists
class UserJobPreferences(BaseModel):
    roles: list[Role] = []
    location: LocationCriteria = LocationCriteria()
    min_salary: Optional[int]

class BulkUser(BaseModel):
    name: str
    email: str
    permission: UserRoles
    linkedInID: Optional[str]
    
class User(MongoBaseModel):
    name: str
    email: str
    email_opt_out: bool = False
    permission: UserRoles
    picture: str
    linkedInID: Optional[str]

    # Data
    data: UserDataFields = UserDataFields()
    job_preferences: UserJobPreferences = UserJobPreferences()

class CreateUser(User):
    password: Optional[str]

# WARNING WARNING WARINIG
# The User can update any of these details freely
class UpdateUserDetails(BaseModel):
    name: Optional[str]
    picture: Optional[str]
    email_opt_out: Optional[bool]
    # Data
    data: Optional[UserDataFields]
    job_preferences: Optional[UserJobPreferences]
    
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