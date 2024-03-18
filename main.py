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
from app.customSign_Pictures.routes import router as customSign_Pictures_router
from app.userFavouriteGesture.routes import router as userFavouriteGesture_router
from app.userSetting.routes import router as userSettings_router
from app.lesson.routes import router as lesson_router
from app.gesture.routes import router as gesture_router
from app.userTakesLesson.routes import router as userTakesLesson_router
from app.videoCall.routes import router as videoCall_router
from app.transcriptFeedback.routes import router as transcriptFeedback_router


import uvicorn
app = FastAPI()

# Mount routers
app.include_router(users_router)
app.include_router(contacts_router)
app.include_router(videoCallParticipants_router)
app.include_router(customSign_router)
app.include_router(customSign_Pictures_router)
app.include_router(userFavouriteGesture_router)
app.include_router(userSettings_router)
app.include_router(lesson_router)
app.include_router(gesture_router)
app.include_router(userTakesLesson_router)
app.include_router(videoCall_router)
app.include_router(transcriptFeedback_router)

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
if __name__ == "__main__":
    import socket
    ip = socket.gethostbyname(socket.gethostname())  # Get the IP address of the server
    uvicorn.run(app, host=ip, port=8000)
