from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import database
from app.userTakesLesson.services import add_user_lesson
from app.userTakesLesson.schemas import UserLesson

router = APIRouter(prefix="/usertakeslesson", tags=['User Takes Lesson'])

@router.post("/add")
def add_user_takes_lesson(user_lesson: UserLesson, db: Session = Depends(database.get_db)):
    result = add_user_lesson(db, user_lesson.UserId, user_lesson.LessonId)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
