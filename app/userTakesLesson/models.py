from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..db import  database

Base = database.Base

class UserTakesLesson(Base):
    __tablename__ = 'UserTakesLesson'
    UserId = Column(Integer, ForeignKey('User.Id'), primary_key=True, nullable=False)
    LessonId = Column(Integer, ForeignKey('Lesson.Id'), primary_key=True, nullable=False)

    # Relationship to User and lesson
    UTL_user = relationship('User', back_populates='user_UTL')
    UTL_lesson = relationship('Lesson', back_populates='lesson_UTL')
