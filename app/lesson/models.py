from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..db import database

Base = database.Base


class Lesson(Base):
    __tablename__ = 'Lesson'
    Id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    LanguageType = Column(String(255), nullable=False)
    LessonLevel = Column(String(255), nullable=False)
    LessonType = Column(String(255), nullable=False)

    # Relationships
    lesson_gestures = relationship('Gesture', back_populates='gesture_lesson')
    lesson_UTL = relationship('UserTakesLesson', back_populates='UTL_lesson')
