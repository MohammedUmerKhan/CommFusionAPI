from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import database

from app.userTakesLesson.services import add_user_lesson, get_user_lessons
from app.userTakesLesson.schemas import UserLesson

router = APIRouter(prefix="/usertakeslesson", tags=['User Takes Lesson'])


@router.get("/get-lessons")
def get_user_lessons_route(user_id: int, language_type: str, db: Session = Depends(database.get_db)):
    lesson_types = get_user_lessons(db, user_id, language_type)
    if not lesson_types:
        raise HTTPException(status_code=404, detail="User lessons not found")
    return {"lesson_types": lesson_types}


@router.post("/add")
def add_user_takes_lesson(user_lesson: UserLesson, db: Session = Depends(database.get_db)):
    result = add_user_lesson(db, user_lesson.UserId, user_lesson.LessonId)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
