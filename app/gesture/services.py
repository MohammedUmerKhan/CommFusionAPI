from sqlalchemy.orm import Session
from app.gesture.models import Gesture
from typing import List
from app.gesture.schemas import GestureDetails,GestureMatchRequest, GestureMatchResponse
def get_gesture_details(db: Session, lesson_id: int) -> List[GestureDetails]:
    try:
        gesture_details = db.query(Gesture).filter(Gesture.LessonId == lesson_id).all()
        if gesture_details:
            return [GestureDetails(
                Id=gesture.Id,
                LessonId=gesture.LessonId,
                Description=gesture.Description,
                Resource=gesture.Resource
            ) for gesture in gesture_details]
        else:
            return []
    except Exception as e:
        return [{"error": str(e)}]



def match_gesture_description(db: Session, description: str) -> GestureMatchResponse:
    gesture = db.query(Gesture).filter(Gesture.Description == description).first()
    if gesture:
        return GestureMatchResponse(Resource=gesture.Resource)
    return GestureMatchResponse(Resource=None)
