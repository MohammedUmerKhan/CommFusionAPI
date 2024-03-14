from sqlalchemy import Column, Integer, String, ForeignKey,DATETIME
from sqlalchemy.orm import relationship
from ..db import  database

Base = database.Base


class TranscriptSegment(Base):
    __tablename__ = 'TranscriptSegment'
    Id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    UserId = Column(Integer, ForeignKey('User.Id'), nullable=False)
    VideoCallId = Column(Integer, ForeignKey('VideoCall.Id'), nullable=False)
    SegmentNumber = Column(Integer, nullable=False)
    StartTime = Column(DATETIME, nullable=False)
    EndTime = Column(DATETIME, nullable=False)
    Content = Column(String, nullable=False)

    # Relationships
    TS_user = relationship("User", back_populates="user_TS")
    TSs_videocall = relationship('VideoCall', back_populates='videocall_TSs')
    TS_has_TF = relationship('TranscriptFeedback', back_populates='TF_has_TS')


