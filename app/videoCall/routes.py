from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import database
from app.videoCall.services import start_video_call, accept_video_call
from app.videoCall.schemas import VideoCallStart,VideoCallAccept

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
