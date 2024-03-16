from sqlalchemy.orm import Session
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
