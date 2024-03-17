from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import database
from app.transcriptFeedback.schemas import TranscriptFeedbackCreate, TranscriptFeedback
from app.transcriptFeedback.services import create_transcriptfeedback

router = APIRouter(prefix="/transcript-feedback", tags=["Transcript Feedback"])


@router.post("/", response_model=TranscriptFeedback)
def create_transcript_feedback(
        feedback: TranscriptFeedbackCreate,
        db: Session = Depends(database.get_db)
):
    try:
        return create_transcriptfeedback(db, feedback)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
