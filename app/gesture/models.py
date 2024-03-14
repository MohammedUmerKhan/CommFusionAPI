from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db import database

Base = database.Base


class Gesture(Base):
    __tablename__ = 'Gesture'

    Id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    LessonId = Column(Integer, ForeignKey('Lesson.Id'), nullable=False)
    Description = Column(String, nullable=False)
    Resource = Column(String, nullable=False)

    # Relationships
    gesture_user_favorites = relationship('UserFavouriteGesture', back_populates='favouriteGesture_gesture')
    gesture_lesson = relationship("Lesson", back_populates="lesson_gestures")
