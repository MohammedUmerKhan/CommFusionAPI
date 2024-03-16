from pydantic import BaseModel

class UserLesson(BaseModel):
    UserId: int
    LessonId: int

class UserLessonRequest(BaseModel):
    user_id: int
    language_type: str
