from pydantic import BaseModel
from typing import List, Any, Optional

class Role(BaseModel):
    role: str
    sector: str
    embedding: Optional[List[float]]

class City(BaseModel):
    city: str
    region: Optional[str]
    country: str