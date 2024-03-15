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
