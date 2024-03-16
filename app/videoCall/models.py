from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship
from ..db import  database

Base = database.Base


class VideoCall(Base):
    __tablename__ = 'VideoCall'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    StartTime = Column(DateTime, nullable=True)
    EndTime = Column(DateTime, nullable=True)

    #  Relationships
    videocall_TSs = relationship('TranscriptSegment', back_populates='TSs_videocall')
    videocall_VCP = relationship('VideoCallParticipants', back_populates='VCP_videoCall')
