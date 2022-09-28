from pydantic import BaseModel
from typing import Type, List, Any
from enum import Enum, IntEnum

class question_datatypes(str, Enum):
	string
	integer
	boolean
	decimal
	file
	date
	multiple_choice


class job_application_question_choice(BaseModel):
	'id': Any
	'choice': str


class job_application_question(BaseModel):
	'id': Any
	'question': str
	'datatype': question_datatypes
	'questiontype': str
	'choices': List[job_application_question_choice] = None
	'response': Any
	'required': bool
	'raw_data': Any


class job_application_question(BaseModel):
	questions: List(job_application_question) = []


