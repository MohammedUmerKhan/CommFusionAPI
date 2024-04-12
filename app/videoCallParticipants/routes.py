from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import database
from app.videoCallParticipants.services import get_user_calls, get_contact_callLogs

router = APIRouter(prefix="/videocallparticipants", tags=['Videocall Participants'])


@router.get("/{user_id}/calls")
def get_user_calls_route(user_id: int, db: Session = Depends(database.get_db)):
    return get_user_calls(db, user_id)


@router.get("/{user_id}/calls/{contact_id}")
def get_contact_call_logs_route(user_id: int, contact_id: int, db: Session = Depends(database.get_db)):
    return get_contact_callLogs(db, user_id, contact_id)
