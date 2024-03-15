from pydantic import BaseModel

class GestureDetails(BaseModel):
    Id: int
    LessonId: int
    Description: str
    Resource: str
