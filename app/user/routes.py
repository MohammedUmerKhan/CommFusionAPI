from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app.db import database
from app.user.schemas import UserLogin, User, UserSignup, UserDetails, UpdateUserProfile, UserProfile
from app.user.services import authenticate_user, get_users, signup_user, uploadprofilepicture_user, get_user_details, \
    search_user, update_user_profile, update_user_online_status, update_user_account_status_to_deleted, \
    get_user_profile, search_user_by_email
from typing import List

router = APIRouter(prefix="/user", tags=['User'])


@router.get("/check_connection")
def check_db_connection():
    return database.connection_status


@router.get("/all", response_model=List[User])
def get_all_users(db: Session = Depends(database.get_db)):
    return get_users(db)


@router.get("/search-by-username")
def search_user_by_username_route(user_id: int, search_username: str, db: Session = Depends(database.get_db)):
    return search_user(db, user_id, search_username)


@router.get("/search-by-email")
def search_user_by_email_route(user_id: int, search_email: str, db: Session = Depends(database.get_db)):
    try:
        return search_user_by_email(db, user_id, search_email)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
    return {"message": "Login successful", "user": user}


@router.post("/signup")
def signup_user_route(signup_data: UserSignup, db: Session = Depends(database.get_db)):
    return signup_user(db, signup_data)


@router.post("/uploadprofilepicture/{id}")
def signup_user_route(id: int, profile_picture: UploadFile = File(...), db: Session = Depends(database.get_db)):
    return uploadprofilepicture_user(db, id, profile_picture)


@router.put("/update-profile")
def update_user_profile_route(data: UpdateUserProfile, db: Session = Depends(database.get_db)):
    return update_user_profile(db, data)


@router.put("/{user_id}/online-status")
def update_user_online_status_route(user_id: int, online_status: int, db: Session = Depends(database.get_db)):
    return update_user_online_status(db, user_id, online_status)


@router.put("/{user_id}/delete")
def update_user_account_status_to_deleted_route(user_id: int, db: Session = Depends(database.get_db)):
    return update_user_account_status_to_deleted(db, user_id)


@router.get("/profile/{user_id}", response_model=UserProfile)
def get_user_profile_route(user_id: int, db: Session = Depends(database.get_db)):
    user_profile = get_user_profile(db, user_id)
    if not user_profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return user_profile
