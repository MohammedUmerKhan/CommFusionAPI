from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import database
from app.gesture.services import get_gesture_details
from app.gesture.schemas import GestureDetails
from typing import List
router = APIRouter(prefix="/gesture", tags=['Gesture'])

@router.get("/{lesson_id}", response_model=List[GestureDetails])
def get_gestures_for_lesson(lesson_id: int, db: Session = Depends(database.get_db)):
    gestures = get_gesture_details(db, lesson_id)
    if not gestures:
        raise HTTPException(status_code=404, detail="No gestures found for the provided lesson")
    return gestures
