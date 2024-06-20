from sqlalchemy.orm import Session
from app.videoCall.models import VideoCall
from app.videoCallParticipants.models import VideoCallParticipants
from app.videoCall.schemas import VideoCallStart
from app.user.models import User
from app.transcriptSegment.models import TranscriptSegment
from fastapi import HTTPException
from datetime import datetime
from typing import List


def start_video_call(db: Session, video_call_data: VideoCallStart):
    try:
        # Create a new video call
        new_video_call = VideoCall(StartTime=datetime.now())
        db.add(new_video_call)
        db.commit()
        db.refresh(new_video_call)

        # Create a record in the VideoCallParticipants table for the caller
        caller_participant = VideoCallParticipants(UserId=video_call_data.caller_id, VideoCallId=new_video_call.Id,
                                                   isCaller=1)
        db.add(caller_participant)

        # Create records in the VideoCallParticipants table for each receiver
        for receiver_id in video_call_data.receiver_ids:
            receiver_participant = VideoCallParticipants(UserId=receiver_id, VideoCallId=new_video_call.Id, isCaller=0)
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
    # if participant.isCaller == 0:  # Not Caller
    #     other_participant = db.query(VideoCallParticipants).filter(
    #         VideoCallParticipants.VideoCallId == video_call_id,
    #         VideoCallParticipants.UserId != user_id,
    #         VideoCallParticipants.AcceptTime == None  # Check for null AcceptTime
    #     ).first()
    #     if other_participant:
    #         other_participant.AcceptTime = datetime.now()

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
        else:
            # Update end time for all participants
            db.query(VideoCallParticipants).filter(
                VideoCallParticipants.VideoCallId == video_call_id,
                VideoCallParticipants.EndTime == None
            ).update({"EndTime": datetime.now()})

            # Update end time in video call table
            video_call.EndTime = datetime.now()
            db.commit()


        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e


def rate_call_quality(db: Session, video_call_id: int, user_id: int, call_quality: int):
    try:
        participant = db.query(VideoCallParticipants).filter(
            VideoCallParticipants.VideoCallId == video_call_id,
            VideoCallParticipants.UserId == user_id
        ).first()

        if not participant:
            return False

        participant.CallQuality = call_quality
        db.commit()
        return True, "Thanks for rating!"
    except Exception as e:
        db.rollback()
        raise e


def get_transcript(db: Session, user_id: int, video_call_id: int) -> List[TranscriptSegment]:
    try:
        # Fetch the accept time and end time of the video call for the user
        participant = db.query(VideoCallParticipants).filter(
            VideoCallParticipants.VideoCallId == video_call_id,
            VideoCallParticipants.UserId == user_id
        ).first()

        if not participant:
            raise HTTPException(status_code=404, detail="User not found in the video call participants")

        accept_time = participant.AcceptTime
        end_time = participant.EndTime

        # Fetch the transcript segments within the accept time and end time
        user_segments = db.query(TranscriptSegment, User.Fname, User.Lname).join(
            User, TranscriptSegment.UserId == User.Id
        ).filter(
            TranscriptSegment.VideoCallId == video_call_id,
            # TranscriptSegment.UserId == user_id,
            TranscriptSegment.StartTime >= accept_time,
            TranscriptSegment.EndTime <= end_time
        ).all()

        transcript_data = []
        for segment, fname, lname in user_segments:
            fullname = f"{fname} {lname}"
            segment_dict = segment.__dict__
            segment_dict["Fullname"] = fullname
            transcript_data.append(segment_dict)

        return transcript_data
    except Exception as e:
        raise e











#
# def end_call(db: Session, video_call_id: int, user_id: int):
#     try:
#         video_call = db.query(VideoCall).filter(VideoCall.Id == video_call_id).first()
#         if not video_call:
#             return False
#
#         # Check if the user is the caller
#         is_caller = db.query(VideoCallParticipants.isCaller).filter(
#             VideoCallParticipants.VideoCallId == video_call_id,
#             VideoCallParticipants.UserId == user_id
#         ).scalar()
#
#         if is_caller:
#             # Update end time for all participants
#             db.query(VideoCallParticipants).filter(
#                 VideoCallParticipants.VideoCallId == video_call_id,
#                 VideoCallParticipants.EndTime == None
#             ).update({"EndTime": datetime.now()})
#
#             # Update end time in video call table
#             video_call.EndTime = datetime.now()
#             db.commit()
#         else:
#             # Update end time for the user only
#             db.query(VideoCallParticipants).filter(
#                 VideoCallParticipants.VideoCallId == video_call_id,
#                 VideoCallParticipants.UserId == user_id
#             ).update({"EndTime": datetime.now()})
#
#         db.commit()
#         return True
#     except Exception as e:
#         db.rollback()
#         raise e