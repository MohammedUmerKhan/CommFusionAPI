# schemas.py
from pydantic import BaseModel
from typing import List

class CustomSignDetails(BaseModel):
    id: int
    status: str
    definition: str
    pictures: List[str]
