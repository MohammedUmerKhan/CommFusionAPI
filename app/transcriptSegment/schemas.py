from pydantic import BaseModel
from datetime import datetime
from typing import List

class TranscriptSegmentBase(BaseModel):
    UserId: int
    VideoCallId: int

    StartTime: datetime
    EndTime: datetime
    Content: str


class TranscriptSegmentCreate(TranscriptSegmentBase):
     pass


class TranscriptSegment(TranscriptSegmentBase):
    Id: int
    SegmentNumber: int
    class Config:
        from_attributes = True

class TranscriptSegmentList(BaseModel):
    segments: List[TranscriptSegmentCreate]
