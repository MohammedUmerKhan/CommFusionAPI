from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..db import  database

Base = database.Base

class TranscriptFeedback_Images(Base):
    __tablename__ = 'TranscriptFeedback_Images'
    Image = Column(String(500), primary_key=True, nullable=False)
    TranscriptFeedbackId = Column(Integer, ForeignKey('TranscriptFeedback.Id'), primary_key=True, nullable=False)

    # Relationship to TranscriptFeedbackImages
    TFImages_TF = relationship('TranscriptFeedback', back_populates='TF_TFImages')
