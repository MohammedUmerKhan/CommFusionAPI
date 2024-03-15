from sqlalchemy.orm import Session
from app.db import database
from app.user.models import User
from app.gesture.models import Gesture
from app.userFavouriteGesture.models import UserFavouriteGesture
from app.userFavouriteGesture.schemas import AddUserFavoriteGestureRequest
from fastapi import HTTPException


def get_user_favorite_gestures(db: Session, user_id: int):
    try:
        # Check if the user exists
        user = db.query(User).filter_by(Id=user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Get the user's favorite gestures
        user_favorite_gestures = db.query(
            UserFavouriteGesture.UserId,
            UserFavouriteGesture.GestureId
        ).filter(
            UserFavouriteGesture.UserId == user_id
        ).all()

        # Convert the result to a list of dictionaries for JSON serialization
        user_favorite_gestures = [{"UserId": row[0], "GestureId": row[1]} for row in user_favorite_gestures]

        return  user_favorite_gestures

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def add_user_favorite_gesture(db: Session, request: AddUserFavoriteGestureRequest):
    try:
        # Check if the user exists
        user = db.query(User).filter_by(Id=request.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if the gesture exists
        gesture = db.query(Gesture).filter_by(Id=request.gesture_id).first()
        if not gesture:
            raise HTTPException(status_code=404, detail="Gesture not found")

        # Check if the gesture is already a favorite
        existing_favorite = db.query(UserFavouriteGesture).filter_by(UserId=request.user_id,
                                                                     GestureId=request.gesture_id).first()
        if existing_favorite:
            raise HTTPException(status_code=400, detail="The gesture is already a favorite")

        # Add the gesture as a favorite for the user
        favorite = UserFavouriteGesture(UserId=request.user_id, GestureId=request.gesture_id)
        db.add(favorite)
        db.commit()

        return {"message": "Gesture added as a favorite successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def delete_user_favorite_gesture(db: Session, user_id: int, gesture_id: int):
    try:
        # Check if the user exists
        user = db.query(User).filter_by(Id=user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if the gesture exists
        gesture = db.query(Gesture).filter_by(Id=gesture_id).first()
        if not gesture:
            raise HTTPException(status_code=404, detail="Gesture not found")

        # Check if the user has the gesture as a favorite
        favorite_gesture = db.query(UserFavouriteGesture).filter_by(UserId=user_id, GestureId=gesture_id).first()
        if not favorite_gesture:
            raise HTTPException(status_code=404, detail="User does not have the gesture as a favorite")

        # Delete the favorite gesture
        db.delete(favorite_gesture)
        db.commit()

        return {"message": "User's favorite gesture deleted successfully"}, 200

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
