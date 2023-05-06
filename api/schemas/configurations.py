from pydantic import BaseModel
from typing import List, Any, Optional

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