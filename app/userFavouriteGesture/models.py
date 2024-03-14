from sqlalchemy import Column, Integer, String, ForeignKey,DATETIME
from sqlalchemy.orm import relationship
from ..db import  database

Base = database.Base


class UserFavouriteGesture(Base):
    __tablename__ = 'UserFavouriteGesture'
    UserId = Column(Integer, ForeignKey('User.Id'), primary_key=True, nullable=False)
    GestureId = Column(Integer, ForeignKey('Gesture.Id'), primary_key=True, nullable=False)


    # Relationships
    favouriteGesture_user = relationship("User", back_populates="user_favoritesGesture")
    favouriteGesture_gesture = relationship("Gesture", back_populates="gesture_user_favorites")


