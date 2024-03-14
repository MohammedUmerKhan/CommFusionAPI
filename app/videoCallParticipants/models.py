from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME
from sqlalchemy.orm import relationship
from ..db import  database

Base = database.Base


class VideoCallParticipants(Base):
    __tablename__ = 'VideoCallParticipants'
    UserId = Column(Integer, ForeignKey('User.Id'),primary_key=True, nullable=False)
    VideoCallId = Column(Integer, ForeignKey('VideoCall.Id'), primary_key=True, nullable=False)
    CallQuality = Column(Integer, nullable=False)
    isCaller = Column(DATETIME, nullable=False)

    # Relationships
    VCP_user = relationship("User", back_populates="user_VPC")
    VCP_videoCall = relationship('VideoCall', back_populates='videocall_VCP')
