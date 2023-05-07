from datetime import date
from pydantic import BaseModel
from typing import List, Any, Optional
from enum import Enum

from schemas.mongo import MongoBaseModel, ObjectId
from schemas.configurations import City

class Status(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"

class FieldType(str, Enum):
    TEXT = "Text"
    LONG_TEXT = "LongText"
    NUMBER = "Number"
    MULTIPLE_CHOICE = "MultipleChoice"
    DATE = "Date"
    FILE = "File"
    CHECKBOX = "CheckBox"
    RADIO = "Radio"

class Choice(BaseModel):
    id: str
    content: str
    raw_data: Optional[Any]

class Question(BaseModel):
    id: str
    content: str
    ai_prompt: Optional[str]
    type: FieldType
    required: bool
    choices: Optional[List[Choice]]
    response: Optional[Any]
    raw_data: Optional[Any] # Contains Any Data Required for Applying to a job, For individual questions. Please don't dump here.

class Company(BaseModel):
    name: str
    logo: Optional[str]
    website: Optional[str]
    tagline: Optional[str]
    employee_count: Optional[str]
    sectors: Optional[List[str]] # Company Sectors i.e. B2B,E-Commerce from a preset selection (TBD), likely to be automated

class JobSimplified(MongoBaseModel):
    # Technical Details
    source: str  # Should be class Name i.e. sampleJobsniffer
    ext_ID: str # Should be a unique ID for the job, can be used to store id's equal to the origional src
    added_ts: int
    last_updated_ts: int
    created_ts: int
    short_description: Optional[str] # A Short Description Generated automatically if it doesn't exist <200 words
    # Display Details
    src_url: Optional[str]
    role: str #Role i.e Production Engineer
    company: Company
    role_description: Optional[str]
    requirements: Optional[List[str]]
    key_points: Optional[List[str]]
    location: City # Location
    salary: Optional[str] # A Salary If Possible, Either one number or a range ( min - max ) i.e "10000 - 14000"
    salary_currency: Optional[str]
    remote: Optional[bool]
    role_category: Optional[List[str]] # Role from a preset selection
    sector_category: Optional[str] # Sector from a preset selection
    skills: List[str] # Skills i.e. Python, Swimming from a preset selection (TBD), likely to be automated
    status: Status

class Job(JobSimplified):
    long_description: Optional[str] # Should contain a full summary of the job listing. This is what the AI will use to analyse the Job
    raw_data: Optional[Any] # Contains Any Data Required for Applying to a job, that doesn't fit anywhere else i.e. real types. Please don't dump here.
    questions: List[Question]

class Application(MongoBaseModel):
    user_id: ObjectId
    job_id: ObjectId
    job: Optional[JobSimplified]
    responses: Optional[object]
    application_read: bool = False
    application_read_ts: date = None
    application_requested: bool = False
    application_requested_ts: date = None
    application_processing: bool = False
    application_processing_ts: date = None
    application_processed: bool = False
    application_processed_ts: date = None
    application_reviewed: bool = False
    application_reviewed_ts: date = None
    application_sending: bool = False
    application_sending_ts: date = None
    application_sent: bool = False
    application_sent_ts: date = None