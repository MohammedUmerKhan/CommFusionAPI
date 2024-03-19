from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import database
from app.transcriptSegment.services import create_transcript_segment
from app.transcriptSegment.schemas import TranscriptSegmentCreate,TranscriptSegment


router = APIRouter(prefix="/transcriptsegments", tags=["Transcript Segments"])


@router.post("/", response_model=TranscriptSegment)
def add_transcript_segment(
        segment_data: TranscriptSegmentCreate,
        db: Session = Depends(database.get_db)
):
    try:
        segment = create_transcript_segment(db, segment_data)
        return segment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
