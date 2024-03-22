from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import database
from app.videoCallParticipants.services import get_user_calls

router = APIRouter(prefix="/videocallparticipants", tags=['Videocall Participants'])


@router.get("/{user_id}/calls")
def get_user_calls_route(user_id: int, db: Session = Depends(database.get_db)):
    return get_user_calls(db, user_id)
