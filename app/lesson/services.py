from sqlalchemy.orm import Session
from typing import List
from app.lesson.models import Lesson

def get_lesson_info(db: Session, language_type: str, lesson_level: str) -> List[dict]:
    try:
        lesson_info = db.query(Lesson).filter(
            Lesson.LanguageType == language_type,
            Lesson.LessonLevel == lesson_level
        ).all()
        if lesson_info:
            result = []
            for lesson in lesson_info:
                result.append({
                    "LessonId": lesson.Id,
                    "LessonType": lesson.LessonType
                })
            return result
        else:
            return []
    except Exception as e:
        return {"error": str(e)}
