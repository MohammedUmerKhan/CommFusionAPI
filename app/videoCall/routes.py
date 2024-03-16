from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import database
from app.videoCall.services import start_video_call, accept_video_call, add_video_call_participant,end_call
from app.videoCall.schemas import VideoCallStart, VideoCallAccept, VideoCallParticipantAdd,EndCallRequest

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
