from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import database
from app.lesson.services import get_lesson_info
from app.lesson.schemas import LessonQuery

router = APIRouter(prefix="/lesson", tags=['Lesson'])

@router.post("/query")
def query_lesson(lesson_query: LessonQuery, db: Session = Depends(database.get_db)):
    return get_lesson_info(db, lesson_query.LanguageType, lesson_query.LessonLevel)
