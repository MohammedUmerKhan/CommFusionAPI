from sqlalchemy.orm import Session
from app.transcriptSegment.models import TranscriptSegment
from app.transcriptSegment.schemas import TranscriptSegment as TS, TranscriptSegmentCreate
from typing import List

def create_transcript_segment(db: Session, segment_data: TS):
    # Check if there are previous segments for the given VideoCallId
    last_segment = db.query(TranscriptSegment).filter(
        TranscriptSegment.VideoCallId == segment_data.VideoCallId
    ).order_by(TranscriptSegment.SegmentNumber.desc()).first()

    if last_segment:
        # Create a new instance of TranscriptSegment with updated SegmentNumber
        updated_segment_data = TranscriptSegment(
            UserId=segment_data.UserId,
            VideoCallId=segment_data.VideoCallId,
            StartTime=segment_data.StartTime,
            EndTime=segment_data.EndTime,
            Content=segment_data.Content,
            SegmentNumber=last_segment.SegmentNumber + 1
        )
    else:
        # If there are no previous segments, set SegmentNumber to 1
        updated_segment_data = TranscriptSegment(
            UserId=segment_data.UserId,
            VideoCallId=segment_data.VideoCallId,
            StartTime=segment_data.StartTime,
            EndTime=segment_data.EndTime,
            Content=segment_data.Content,
            SegmentNumber=1
        )

    # Create the new TranscriptSegment
    db.add(updated_segment_data)
    db.commit()
    db.refresh(updated_segment_data)
    return updated_segment_data

def create_transcript_segments(db: Session, segments_data: List[TranscriptSegmentCreate]) -> List[TS]:
    created_segments = []
    segment_number = 1

    for segment_data in segments_data:
        new_segment = TranscriptSegment(
            UserId=segment_data.UserId,
            VideoCallId=segment_data.VideoCallId,
            StartTime=segment_data.StartTime,
            EndTime=segment_data.EndTime,
            Content=segment_data.Content,
            SegmentNumber=segment_number
        )
        segment_number += 1

        # Add the new TranscriptSegment to the session
        db.add(new_segment)
        db.commit()
        db.refresh(new_segment)
        created_segments.append(new_segment)

    return created_segments

def get_transcript_segments_by_videocall(db: Session, video_call_id: int) -> List[TS]:
    segments = db.query(TranscriptSegment).filter(
        TranscriptSegment.VideoCallId == video_call_id
    ).order_by(TranscriptSegment.SegmentNumber.asc()).all()
    return segments