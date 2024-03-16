from pydantic import BaseModel

class VideoCallStart(BaseModel):
    caller_id: int
    receiver_id: int

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
