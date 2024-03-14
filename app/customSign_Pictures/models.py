from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..db import  database

Base = database.Base

class CustomSign_Pictures(Base):
    __tablename__ = 'CustomSign_Pictures'
    Picture = Column(String(500), primary_key=True, nullable=False)
    CustomSignId = Column(Integer, ForeignKey('CustomSign.Id'), primary_key=True, nullable=False)

    # Relationship to CustomSign
    CSpictures_custom_Sign = relationship('CustomSign', back_populates='customSign_CSpictures')
