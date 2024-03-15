from pydantic import BaseModel

class LessonQuery(BaseModel):
    LanguageType: str
    LessonLevel: str
