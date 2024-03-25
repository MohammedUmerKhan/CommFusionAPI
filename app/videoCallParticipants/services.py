from sqlalchemy.orm import Session
from app.db import database
from app.videoCallParticipants.models import VideoCallParticipants
from app.user.models import User
from app.videoCall.models import VideoCall
from app.videoCallParticipants.schemas import UserCallDetails
from fastapi import HTTPException
from sqlalchemy.orm import aliased
def get_user_calls(db: Session, user_id: int):
    try:
        # Check if the user exists
        user = db.query(User).filter_by(Id=user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Alias for the other participants
        OtherParticipants = aliased(User)

        # Alias for the VideoCallParticipants to join with itself
        OtherParticipantsParticipants = aliased(VideoCallParticipants)

        # Get the user's calls with other participants' details
        user_calls = db.query(
            VideoCall.Id,
            OtherParticipants.Fname.label("OtherParticipantFname"),
            OtherParticipants.Lname.label("OtherParticipantLname"),
            OtherParticipants.ProfilePicture,
            OtherParticipants.OnlineStatus,
            OtherParticipants.AccountStatus,
            VideoCallParticipants.isCaller,
            VideoCall.EndTime,
            VideoCall.StartTime
        ).join(
            VideoCall, VideoCallParticipants.VideoCallId == VideoCall.Id
        ).join(
            User, VideoCallParticipants.UserId == User.Id
        ).join(
            OtherParticipantsParticipants, VideoCall.Id == OtherParticipantsParticipants.VideoCallId
        ).join(
            OtherParticipants, OtherParticipantsParticipants.UserId == OtherParticipants.Id
        ).filter(
            VideoCallParticipants.UserId == user_id,
            OtherParticipants.Id != user_id
        ).order_by(
            VideoCall.StartTime.desc()
        ).all()

        # Convert the result to a list of dictionaries for JSON serialization
        user_calls = [{
            "VideoCallId": row[0],
            "OtherParticipantFname": row[1],
            "OtherParticipantLname": row[2],
            "ProfilePicture": row[3],
            "OnlineStatus": row[4],
            "AccountStatus": row[5],
            "isCaller": row[6],
            "EndTime": row[7],
            "StartTime": row[8]
        } for row in user_calls]

        return user_calls

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_contact_callLogs(db: Session, user_id: int, contact_id: int):
    try:
        # Check if the user exists
        user = db.query(User).filter_by(Id=user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if the contact exists
        contact = db.query(User).filter_by(Id=contact_id).first()
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")

        # Alias for the other participants
        OtherParticipants = aliased(User)

        # Alias for the VideoCallParticipants to join with itself
        OtherParticipantsParticipants = aliased(VideoCallParticipants)

        # Get the user's calls with the specified contact details
        user_calls = db.query(
            VideoCall.Id,
            OtherParticipants.Fname.label("OtherParticipantFname"),
            OtherParticipants.Lname.label("OtherParticipantLname"),
            OtherParticipants.ProfilePicture,
            OtherParticipants.OnlineStatus,
            OtherParticipants.AccountStatus,
            VideoCallParticipants.isCaller,
            VideoCall.EndTime,
            VideoCall.StartTime
        ).join(
            VideoCall, VideoCallParticipants.VideoCallId == VideoCall.Id
        ).join(
            User, VideoCallParticipants.UserId == User.Id
        ).join(
            OtherParticipantsParticipants, VideoCall.Id == OtherParticipantsParticipants.VideoCallId
        ).join(
            OtherParticipants, OtherParticipantsParticipants.UserId == OtherParticipants.Id
        ).filter(
            VideoCallParticipants.UserId == user_id,
            OtherParticipants.Id == contact_id
        ).order_by(
            VideoCall.StartTime.desc()
        ).all()

        # Convert the result to a list of dictionaries for JSON serialization
        user_calls = [{
            "VideoCallId": row[0],
            "OtherParticipantFname": row[1],
            "OtherParticipantLname": row[2],
            "ProfilePicture": row[3],
            "OnlineStatus": row[4],
            "AccountStatus": row[5],
            "isCaller": row[6],
            "EndTime": row[7],
            "StartTime": row[8]
        } for row in user_calls]

        return user_calls

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))