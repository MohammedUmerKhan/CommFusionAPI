from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import database
from app.transcriptSegment.services import create_transcript_segment,create_transcript_segments,get_transcript_segments_by_videocall
from app.transcriptSegment.schemas import TranscriptSegmentCreate,TranscriptSegment, TranscriptSegmentList
from typing import List


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


@router.post("/bulk", response_model=List[TranscriptSegment])
def add_transcript_segments(
        segments_data: TranscriptSegmentList,
        db: Session = Depends(database.get_db)
):
    try:
        segments = create_transcript_segments(db, segments_data.segments)
        return segments
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/video/{video_call_id}", response_model=List[TranscriptSegment])
def get_transcript_segments(
        video_call_id: int,
        db: Session = Depends(database.get_db)
):
    try:
        segments = get_transcript_segments_by_videocall(db, video_call_id)
        if not segments:
            raise HTTPException(status_code=404, detail="Transcript segments not found")
        return segments
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")