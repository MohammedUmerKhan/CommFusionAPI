from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db import  database

Base = database.Base

class TranscriptFeedback(Base):
    __tablename__ = 'TranscriptFeedback'
    Id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    TranscriptSegmentId = Column(Integer, ForeignKey('TranscriptSegment.Id'), nullable=False)
    Description = Column(String, nullable=False)
    isCorrect = Column(Integer, nullable=False)

    # Relationships
    TF_TFImages = relationship("TranscriptFeedback_Images", back_populates="TFImages_TF")
    TF_has_TS = relationship("TranscriptSegment", back_populates="TS_has_TF")
