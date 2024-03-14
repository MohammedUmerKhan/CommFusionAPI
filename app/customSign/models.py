from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db import  database

Base = database.Base

class CustomSign(Base):
    __tablename__ = 'CustomSign'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    UserId = Column(Integer, ForeignKey('User.Id'), nullable=False)
    Status = Column(String(45), nullable=False)
    Definition = Column(String(255), nullable=False)

    # Relationships
    customSign_user = relationship("User", back_populates="user_customSigns")
    customSign_CSpictures = relationship('CustomSign_Pictures', back_populates='CSpictures_custom_Sign')
