import os

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Path
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.db import database
from app.user.schemas import UserLogin, User, UserSignup, UserDetails, UpdateUserProfile
from app.user.services import authenticate_user, get_users, signup_user, uploadprofilepicture_user, get_user_details, \
    search_user, update_user_profile,update_user_online_status, update_user_account_status_to_deleted
from typing import List

router = APIRouter(prefix="/user", tags=['User'])


@router.get("/check_connection")
def check_db_connection():
    return database.connection_status


@router.get("/all", response_model=List[User])
def get_all_users(db: Session = Depends(database.get_db)):
    return get_users(db)


@router.get("/search")
def search_user_route(user_id: int, search_username: str, db: Session = Depends(database.get_db)):
    return search_user(db, user_id, search_username)


@router.get("/userdetails/{user_id}", response_model=UserDetails)
def get_user_by_id(user_id: int, db: Session = Depends(database.get_db)):
    user_details = get_user_details(db, user_id)
    if not user_details:
        raise HTTPException(status_code=404, detail="User not found")
    return user_details


@router.post("/login")
def login_user(login_data: UserLogin, db: Session = Depends(database.get_db)):
    user = authenticate_user(db, login_data)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    # You can return a token here for authentication purposes
    return {"message": "Login successful", "user_id": user.Id,"username": user.Username}


@router.post("/signup")
def signup_user_route(signup_data: UserSignup, db: Session = Depends(database.get_db)):
    return signup_user(db, signup_data)


@router.post("/uploadprofilepicture/{id}")
def signup_user_route(id: int, profile_picture: UploadFile = File(...), db: Session = Depends(database.get_db)):
    return uploadprofilepicture_user(db, id, profile_picture)
@router.put("/update-profile")
def update_user_profile_route(data: UpdateUserProfile, db: Session = Depends(database.get_db)):
    return update_user_profile(db, data)

#for img accessing
@router.get("/images/profile/{image_name}")
async def get_profile_picture(image_name: str):

    image_path = os.path.join(os.path.dirname(__file__),"images/profile/", image_name)
    print("path: ",image_path)
    # Return the image file using FileResponse
    return FileResponse(image_path)

@router.put("/{user_id}/online-status")
def update_user_online_status_route(user_id: int, online_status: int, db: Session = Depends(database.get_db)):
    return update_user_online_status(db, user_id, online_status)


@router.put("/{user_id}/delete")
def update_user_account_status_to_deleted_route(user_id: int, db: Session = Depends(database.get_db)):
    return update_user_account_status_to_deleted(db, user_id)