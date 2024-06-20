from pydantic import BaseModel
from datetime import datetime
from typing import List


class VideoCallStart(BaseModel):
    caller_id: int
    receiver_ids: List[int]  # Change to a list to accept multiple receiver IDs


class VideoCallAccept(BaseModel):
    video_call_id: int
    user_id: int


class VideoCallParticipantAdd(BaseModel):
    video_call_id: int
    user_id: int


class EndCallRequest(BaseModel):
    video_call_id: int
    user_id: int


class RatingCallQuality(BaseModel):
    call_quality: int


class TranscriptSegment(BaseModel):
    Id: int
    UserId: int
    VideoCallId: int
    SegmentNumber: int
    StartTime: datetime
    EndTime: datetime
    Content: str
    Fullname: str


class TranscriptResponse(BaseModel):
    transcript_segments: List[TranscriptSegment]
