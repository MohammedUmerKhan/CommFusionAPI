from pydantic import BaseModel
from typing import Optional

class GestureDetails(BaseModel):
    Id: int
    LessonId: int
    Description: str
    Resource: str

class GestureMatchRequest(BaseModel):
    Description: str

class GestureMatchResponse(BaseModel):
    Resource: Optional[str] = None