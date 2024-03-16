from sqlalchemy.orm import Session
from app.lesson.models import Lesson
from app.userTakesLesson.models import UserTakesLesson


def add_user_lesson(db: Session, user_id: int, lesson_id: int) -> dict:
    try:
        # Check if the user already takes the lesson
        existing_entry = db.query(UserTakesLesson).filter_by(UserId=user_id, LessonId=lesson_id).first()
        if existing_entry:
            return {"message": "User already takes this lesson"}

        # Add the user's lesson
        new_entry = UserTakesLesson(UserId=user_id, LessonId=lesson_id)
        db.add(new_entry)
        db.commit()

        return {"message": "User lesson added successfully"}

    except Exception as e:
        return {"error": str(e)}


def get_user_lessons(db: Session, user_id: int, language_type: str) -> list:
    try:
        # Query user's taken lessons based on the user ID and language type
        user_lessons = db.query(Lesson.LessonType).join(UserTakesLesson, Lesson.Id == UserTakesLesson.LessonId).filter(UserTakesLesson.UserId == user_id, Lesson.LanguageType == language_type).all()

        # Extract lesson types from the result
        lesson_types = [lesson.LessonType for lesson in user_lessons]

        return lesson_types

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
