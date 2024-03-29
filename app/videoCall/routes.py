from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import database
from app.videoCall.services import start_video_call, accept_video_call, add_video_call_participant, end_call, \
    rate_call_quality,get_transcript
from app.videoCall.schemas import VideoCallStart, VideoCallAccept, VideoCallParticipantAdd, EndCallRequest, \
    RatingCallQuality, TranscriptResponse

router = APIRouter(prefix="/video-call", tags=['Video Call'])


@router.post("/start")
def start_video_call_route(video_call_data: VideoCallStart, db: Session = Depends(database.get_db)):
    return start_video_call(db, video_call_data)


@router.post("/accept")
async def accept_video_call_endpoint(data: VideoCallAccept, db: Session = Depends(database.get_db)):
    try:
        result = accept_video_call(db, data.video_call_id, data.user_id)
        if not result:
            raise HTTPException(status_code=404, detail="Video call not found")
        return {"message": "Video call accepted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add-participant")
async def add_video_call_participant_endpoint(data: VideoCallParticipantAdd, db: Session = Depends(database.get_db)):
    try:
        result = add_video_call_participant(db, data.video_call_id, data.user_id)
        if not result:
            raise HTTPException(status_code=404, detail="Video call not found")
        return {"message": "Participant added to video call successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/end-call")
async def end_call_endpoint(data: EndCallRequest, db: Session = Depends(database.get_db)):
    try:
        result = end_call(db, data.video_call_id, data.user_id)
        if not result:
            raise HTTPException(status_code=404, detail="Video call not found")
        return {"message": "Call ended successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/rate-call-quality/{video_call_id}/{user_id}", response_model=str)
def rate_call_quality_endpoint(video_call_id: int, user_id: int, quality: RatingCallQuality, db: Session = Depends(database.get_db)):
    success, message = rate_call_quality(db, video_call_id, user_id, quality.call_quality)
    if not success:
        raise HTTPException(status_code=404, detail="Video call or user not found")
    return message


@router.get("/transcript/{user_id}/{video_call_id}", response_model=TranscriptResponse)
def get_transcript_endpoint(user_id: int, video_call_id: int, db: Session = Depends(database.get_db)):
    transcript_data = get_transcript(db, user_id, video_call_id)
    if not transcript_data:
        raise HTTPException(status_code=404, detail="No transcript data found")
    return {"transcript_segments": transcript_data}
