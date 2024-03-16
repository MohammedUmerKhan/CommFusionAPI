from fastapi import FastAPI
from app.db import Database
from app.user import models as user
from app.contacts import models as contacts
from app.customSign import models as customSign
from app.customSign_Pictures import models as customSign_Pictures
from app.gesture import models as gesture
from app.lesson import models as lesson
from app.transcriptFeedback import models as transcriptFeedback
from app.transcriptFeedback_Images import models as transcriptFeedback_Images
from app.transcriptSegment import models as transcriptSegment
from app.userFavouriteGesture import models as userFavouriteGesture
from app.userSetting import models as userSetting
from app.userTakesLesson import models as userTakesLesson
from app.videoCall import models as videoCall
from app.videoCallParticipants import models as videoCallParticipants
from app.user.routes import router as users_router
from app.contacts.routes import router as contacts_router
from app.videoCallParticipants.routes import router as videoCallParticipants_router
from app.customSign.routes import router as customSign_router
from app.userFavouriteGesture.routes import router as userFavouriteGesture_router
from app.userSetting.routes import router as userSettings_router
from app.lesson.routes import router as lesson_router
from app.gesture.routes import router as gesture_router
from app.userTakesLesson.routes import router as userTakesLesson_router


import uvicorn
app = FastAPI()

# Mount routers
app.include_router(users_router)
app.include_router(contacts_router)
app.include_router(videoCallParticipants_router)
app.include_router(customSign_router)
app.include_router(userFavouriteGesture_router)
app.include_router(userSettings_router)
app.include_router(lesson_router)
app.include_router(gesture_router)
app.include_router(userTakesLesson_router)
#
# @app.get('/checkDatabase')
# def index():
#     test = databaseHandler.check_database_connection()
#     return {'data': f'{test}'}
#
#
# @app.get('/contacts')
# def FetchContacts():
#     try:
#         session = databaseHandler.return_session()
#         contact = session.query(contacts.Contacts).all()
#         return contact
#     except Exception as e:
#         return {"error": str(e)}, 500
#
#
# @app.get('/customSign')
# def FetchCustomSign():
#     try:
#         session = databaseHandler.return_session()
#         cs = session.query(customSign.CustomSign).all()
#         return cs
#     except Exception as e:
#         return {"error": str(e)}, 500
#
#
# @app.get('/customSignPictures')
# def FetchCustomSignPictures():
#     try:
#         session = databaseHandler.return_session()
#         cs = session.query(customSign_Pictures.CustomSign_Pictures).all()
#         return cs
#     except Exception as e:
#         return {"error": str(e)}, 500
#
#
# @app.get('/gesture')
# def FetchGesture():
#     try:
#         session = databaseHandler.return_session()
#         cs = session.query(gesture.Gesture).all()
#         return cs
#     except Exception as e:
#         return {"error": str(e)}, 500
#
#
# @app.get('/lesson')
# def FetchLesson():
#     try:
#         session = databaseHandler.return_session()
#         cs = session.query(lesson.Lesson).all()
#         return cs
#     except Exception as e:
#         return {"error": str(e)}, 500
#
#
# @app.get('/transcriptFeedback')
# def FetchTranscriptFeedback():
#     try:
#         session = databaseHandler.return_session()
#         cs = session.query(transcriptFeedback.TranscriptFeedback).all()
#         return cs
#     except Exception as e:
#         return {"error": str(e)}, 500
#
#
# @app.get('/transcriptFeedback_Images')
# def FetchtranscriptFeedback_Images():
#     try:
#         session = databaseHandler.return_session()
#         cs = session.query(transcriptFeedback_Images.TranscriptFeedback_Images).all()
#         return cs
#     except Exception as e:
#         return {"error": str(e)}, 500
#
#
# @app.get('/transcriptSegment')
# def FetchtranscriptSegment():
#     try:
#         session = databaseHandler.return_session()
#         cs = session.query(transcriptSegment.TranscriptSegment).all()
#         return cs
#     except Exception as e:
#         return {"error": str(e)}, 500
#
#
# @app.get('/user')
# def FetchUsers():
#     try:
#         session = databaseHandler.return_session()
#         users = session.query(user.User).all()
#         return users
#     except Exception as e:
#         return {"error": str(e)}, 500
#
#
# @app.get('/userFavouriteGesture')
# def FetchuserFavouriteGesture():
#     try:
#         session = databaseHandler.return_session()
#         cs = session.query(userFavouriteGesture.UserFavouriteGesture).all()
#         return cs
#     except Exception as e:
#         return {"error": str(e)}, 500
#
#
# @app.get('/userSetting')
# def FetchuserSetting():
#     try:
#         session = databaseHandler.return_session()
#         cs = session.query(userSetting.UserSetting).all()
#         return cs
#     except Exception as e:
#         return {"error": str(e)}, 500
#
#
# @app.get('/userTakesLesson')
# def FetchuserTakesLesson():
#     try:
#         session = databaseHandler.return_session()
#         cs = session.query(userTakesLesson.UserTakesLesson).all()
#         return cs
#     except Exception as e:
#         return {"error": str(e)}, 500
#
#
# @app.get('/videoCall')
# def FetchvideoCall():
#     try:
#         session = databaseHandler.return_session()
#         cs = session.query(videoCall.VideoCall).all()
#         return cs
#     except Exception as e:
#         return {"error": str(e)}, 500
#
#
# @app.get('/videoCallParticipants')
# def FetchvideoCallParticipants():
#     try:
#         session = databaseHandler.return_session()
#         cs = session.query(videoCallParticipants.VideoCallParticipants).all()
#         return cs
#     except Exception as e:
#         return {"error": str(e)}, 500
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
