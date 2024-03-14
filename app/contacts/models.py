from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..db import  database

Base = database.Base

class Contacts(Base):
    __tablename__ = 'Contacts'
    UserId = Column(Integer, ForeignKey('User.Id'), primary_key=True, nullable=False)
    ContactId = Column(Integer, ForeignKey('User.Id'), primary_key=True, nullable=False)
    IsBlocked = Column(Integer, nullable=False)


    # Relationships
    contact_user = relationship("User", back_populates="user_contact", foreign_keys=[UserId])
    contact_users = relationship("User", back_populates="user_contacts", foreign_keys=[ContactId])



