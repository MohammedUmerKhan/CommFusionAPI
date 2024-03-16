from pydantic import BaseModel

class UserLesson(BaseModel):
    UserId: int
    LessonId: int
