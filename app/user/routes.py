from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Path
from sqlalchemy.orm import Session
from app.db import database
from app.user.schemas import UserLogin, User, UserSignup, UserDetails
from app.user.services import authenticate_user, get_users, signup_user, uploadprofilepicture_user, get_user_details, \
    search_user
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
    return {"message": "Login successful", "user_id": user.Id}


@router.post("/signup")
def signup_user_route(signup_data: UserSignup, db: Session = Depends(database.get_db)):
    return signup_user(db, signup_data)


@router.post("/uploadprofilepicture/{id}")
def signup_user_route(id: int, profile_picture: UploadFile = File(...), db: Session = Depends(database.get_db)):
    return uploadprofilepicture_user(db, id, profile_picture)
