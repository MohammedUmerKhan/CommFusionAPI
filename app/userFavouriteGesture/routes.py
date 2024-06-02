from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import database
from app.userFavouriteGesture.services import add_user_favorite_gesture, get_user_favorite_gestures, \
    delete_user_favorite_gesture, get_user_favorite_gestures_with_details
from app.userFavouriteGesture.schemas import (AddUserFavoriteGestureRequest, UserFavoriteGesture,
                                              DeleteUserFavoriteGesture,
                                              UserFavoriteGestureSchema)
from typing import List

router = APIRouter(prefix="/userfavoritegesture", tags=['User Favorite Gesture'])


@router.get("/{user_id}", response_model=List[UserFavoriteGesture])
def get_user_favorite_gestures_route(user_id: int, db: Session = Depends(database.get_db)):
    return get_user_favorite_gestures(db, user_id)


@router.post("/add")
def add_user_favorite_gesture_route(request: AddUserFavoriteGestureRequest, db: Session = Depends(database.get_db)):
    return add_user_favorite_gesture(db, request)


@router.delete("/")
def delete_user_favorite_gesture_route(data: DeleteUserFavoriteGesture, db: Session = Depends(database.get_db)):
    return delete_user_favorite_gesture(db, data.user_id, data.gesture_id)


@router.get("/favouriteDetailed/{user_id}", response_model=List[UserFavoriteGestureSchema])
def get_user_favorite_gestures_with_details_route(user_id: int, db: Session = Depends(database.get_db)):
    return get_user_favorite_gestures_with_details(db, user_id)
