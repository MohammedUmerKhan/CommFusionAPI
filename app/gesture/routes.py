from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import database
from app.gesture.services import get_gesture_details,match_gesture_description
from app.gesture.schemas import GestureDetails, GestureMatchRequest,GestureMatchResponse
from typing import List
router = APIRouter(prefix="/gesture", tags=['Gesture'])

@router.get("/{lesson_id}", response_model=List[GestureDetails])
def get_gestures_for_lesson(lesson_id: int, db: Session = Depends(database.get_db)):
    gestures = get_gesture_details(db, lesson_id)
    if not gestures:
        raise HTTPException(status_code=404, detail="No gestures found for the provided lesson")
    return gestures

@router.post("/match")
def match_gesture(request: GestureMatchRequest, db: Session = Depends(database.get_db)):
    response = match_gesture_description(db, request.Description)
    if not response.Resource:
        return None
    return response
