from pydantic import BaseModel
from datetime import datetime


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
