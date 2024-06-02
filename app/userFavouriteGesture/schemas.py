from pydantic import BaseModel


class AddUserFavoriteGestureRequest(BaseModel):
    user_id: int
    gesture_id: int


class UserFavoriteGesture(BaseModel):
    UserId: int
    GestureId: int


class DeleteUserFavoriteGesture(BaseModel):
    user_id: int
    gesture_id: int


class UserFavoriteGestureSchema(BaseModel):
    UserId: int
    GestureId: int
    LessonType: str  # Adjust according to your actual model
    Description: str
    Resource: str  # Adjust according to your actual model
