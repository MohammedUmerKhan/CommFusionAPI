from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from ..db import  database

Base = database.Base
class User(Base):
    __tablename__ = 'User'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Username = Column(String(505), nullable=False)
    DateOfBirth = Column(Date, nullable=False)
    Password = Column(String(255), nullable=False)
    ProfilePicture = Column(String(255), nullable=False)
    Email = Column(String(355), nullable=False)
    DisabilityType = Column(String(100), nullable=False)
    Fname = Column(String(255), nullable=False)
    Lname = Column(String(255), nullable=False)
    AccountStatus = Column(String(255), nullable=False)
    BioStatus = Column(String(355), nullable=False)
    RegistrationDate = Column(Date, nullable=False)
    OnlineStatus = Column(Integer, nullable=False)

    #  Relationships
    user_contact = relationship("Contacts", back_populates="contact_user", foreign_keys="Contacts.UserId")
    user_contacts = relationship("Contacts", back_populates="contact_users", foreign_keys="Contacts.ContactId")
    user_customSigns = relationship("CustomSign", back_populates="customSign_user")
    user_favoritesGesture = relationship("UserFavouriteGesture", back_populates="favouriteGesture_user")
    user_TS = relationship("TranscriptSegment", back_populates="TS_user")
    user_UTL = relationship("UserTakesLesson", back_populates="UTL_user")
    user_usersetting = relationship('UserSetting', back_populates='usersetting_user')
    user_VPC = relationship("VideoCallParticipants", back_populates="VCP_user")




