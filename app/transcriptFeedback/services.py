from sqlalchemy.orm import Session
from app.transcriptFeedback.models import TranscriptFeedback
from app.transcriptFeedback.schemas import TranscriptFeedbackCreate
from sqlalchemy.exc import SQLAlchemyError

def create_transcriptfeedback(db: Session, feedback: TranscriptFeedbackCreate):
    try:
        db_feedback = TranscriptFeedback(**feedback.dict())
        db.add(db_feedback)
        db.commit()
        db.refresh(db_feedback)
        return db_feedback
    except SQLAlchemyError as e:
        db.rollback()  # Rollback changes if an error occurs
        raise e  # Re-raise the exception to propagate it to the caller
