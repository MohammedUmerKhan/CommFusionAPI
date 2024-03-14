from sqlalchemy import Column, Integer, String, ForeignKey,DATETIME
from sqlalchemy.orm import relationship
from ..db import  database

Base = database.Base


class UserSetting(Base):
    __tablename__ = 'UserSetting'
    Id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    UserId = Column(Integer, ForeignKey('User.Id'), nullable=False)
    SettingName = Column(String(255), nullable=False)
    SettingValue = Column(String(255), nullable=False)

    # Relationships
    usersetting_user = relationship("User", back_populates="user_usersetting")
