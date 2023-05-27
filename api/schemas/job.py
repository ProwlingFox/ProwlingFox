from datetime import datetime
from pydantic import BaseModel
from typing import List, Any, Optional
from enum import Enum, IntEnum

from schemas.mongo import MongoBaseModel, ObjectId
from schemas.configurations import City, FieldType

class Status(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"

class ApplicationStatus(IntEnum):
    REJECTED = -3
    CANDIDATEREJECTED = -2
    READ = -1
    UNREAD = 0 # Should Never Occur, Unread applications don't exist as applications
    REQUESTED = 1
    PROCESSING = 2
    PROCESSED = 3
    REVIEWED = 4
    SENDING = 5
    SENT = 6
    CONTACT = 7
    INTERVIEWING = 8
    OFFERED = 9
    ACCEPTED = 10

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

class CompanySummary(BaseModel):
    name: str
    logo: Optional[str]

class Company(CompanySummary):
    website: Optional[str]
    tagline: Optional[str]
    employee_count: Optional[str]
    sectors: Optional[List[str]] # Company Sectors i.e. B2B,E-Commerce from a preset selection (TBD), likely to be automated

class JobSummary(MongoBaseModel):
    role: str
    company: CompanySummary
    role_category: Optional[List[str]]

class JobSimplified(JobSummary):
    # Technical Details
    source: str  # Should be class Name i.e. sampleJobsniffer
    ext_ID: str # Should be a unique ID for the job, can be used to store id's equal to the origional src
    added_ts: datetime
    last_updated_ts: datetime
    created_ts: datetime
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
    skills: Optional[List[str]] # Skills i.e. Python, Swimming from a preset selection (TBD), likely to be automated
    status: Status

class Job(JobSimplified):
    long_description: Optional[str] # Should contain a full summary of the job listing. This is what the AI will use to analyse the Job
    raw_data: Optional[Any] # Contains Any Data Required for Applying to a job, that doesn't fit anywhere else i.e. real types. Please don't dump here.
    questions: List[Question]

class ApplicationSummary(MongoBaseModel):
    user_id: ObjectId
    job_id: ObjectId
    job: Optional[JobSummary]
    status: ApplicationStatus

    application_read_ts: datetime = None
    application_requested_ts: datetime = None
    application_processing_ts: datetime = None
    application_processed_ts: datetime = None
    application_reviewed_ts: datetime = None
    application_sending_ts: datetime = None
    application_sent_ts: datetime = None
    application_contact_ts: datetime = None
    application_interview_ts: datetime = None
    application_offer_ts: datetime = None
    application_accepted_ts: datetime = None
    application_rejected_ts: datetime = None
    application_rejected_by_candidate_ts: datetime = None

    application_failed: bool = False

class Application(ApplicationSummary):
    job: Optional[JobSimplified]
    responses: Optional[object]
