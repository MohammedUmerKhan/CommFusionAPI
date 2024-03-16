from sqlalchemy.orm import Session
from app.videoCall.models import VideoCall
from app.videoCallParticipants.models import  VideoCallParticipants
from app.videoCall.schemas import VideoCallStart
from app.user.models import User
from fastapi import HTTPException
from datetime import datetime

def start_video_call(db: Session, video_call_data: VideoCallStart):
    try:
        # Create a new video call
        new_video_call = VideoCall(StartTime=datetime.now())
        db.add(new_video_call)
        db.commit()
        db.refresh(new_video_call)

        # Create records in the VideoCallParticipants table for the caller and receiver
        caller_participant = VideoCallParticipants(UserId=video_call_data.caller_id, VideoCallId=new_video_call.Id, isCaller=1)
        receiver_participant = VideoCallParticipants(UserId=video_call_data.receiver_id, VideoCallId=new_video_call.Id, isCaller=0)
        db.add(caller_participant)
        db.add(receiver_participant)
        db.commit()

        return {"message": "Video call started successfully", "video_call_id": new_video_call.Id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


def accept_video_call(db: Session, video_call_id: int, user_id: int):
    # Find the video call participant
    participant = db.query(VideoCallParticipants).filter(
        VideoCallParticipants.VideoCallId == video_call_id,
        VideoCallParticipants.UserId == user_id
    ).first()
    if not participant:
        return False  # Video call participant not found

    # Update the start time for the user
    participant.AcceptTime = datetime.now()

    # Check if the other participant (caller) also needs to update their AcceptTime
    if participant.isCaller == 0:  # Caller
        other_participant = db.query(VideoCallParticipants).filter(
            VideoCallParticipants.VideoCallId == video_call_id,
            VideoCallParticipants.UserId != user_id,
            VideoCallParticipants.AcceptTime == None  # Check for null AcceptTime
        ).first()
        if other_participant:
            other_participant.AcceptTime = datetime.now()

    db.commit()
    return True

def add_video_call_participant(db: Session, video_call_id: int, user_id: int):
    # Create a new participant record
    participant = VideoCallParticipants(
        UserId=user_id,
        VideoCallId=video_call_id,
        isCaller=0  # Participant, not the caller
    )
    db.add(participant)
    db.commit()
    return True

def end_call(db: Session, video_call_id: int, user_id: int):
    try:
        video_call = db.query(VideoCall).filter(VideoCall.Id == video_call_id).first()
        if not video_call:
            return False

        # Check if the user is the caller
        is_caller = db.query(VideoCallParticipants.isCaller).filter(
            VideoCallParticipants.VideoCallId == video_call_id,
            VideoCallParticipants.UserId == user_id
        ).scalar()

        if is_caller:
            # Update end time for all participants
            db.query(VideoCallParticipants).filter(
                VideoCallParticipants.VideoCallId == video_call_id,
                VideoCallParticipants.EndTime == None
            ).update({"EndTime": datetime.now()})

            # Update end time in video call table
            video_call.EndTime = datetime.now()
            db.commit()
        else:
            # Update end time for the user only
            db.query(VideoCallParticipants).filter(
                VideoCallParticipants.VideoCallId == video_call_id,
                VideoCallParticipants.UserId == user_id
            ).update({"EndTime": datetime.now()})

        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e
