from enum import Enum
from pydantic import BaseModel
from typing import List, Optional

class Role(BaseModel):
    role: str
    sector: str
    embedding: Optional[List[float]]

class City(BaseModel):
    city: str | None
    region: str | None
    country: str | None

class B64_File(BaseModel):
    file_name: str
    data: str

class FieldType(str, Enum):
    TEXT = "Text"
    LONG_TEXT = "LongText"
    NUMBER = "Number"
    MULTIPLE_CHOICE = "MultipleChoice"
    DATE = "Date"
    FILE = "File"
    CHECKBOX = "CheckBox"
    RADIO = "Radio"