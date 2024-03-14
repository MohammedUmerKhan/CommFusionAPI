import os
from fastapi import UploadFile, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from app.user.models import User
from app.contacts.models import Contacts
from app.user.schemas import UserLogin, UserSearchResult
from app.user.schemas import UserSignup
# from typing import Union
from sqlalchemy.exc import SQLAlchemyError


def get_users(db: Session):
    return db.query(User).all()


def authenticate_user(db: Session, login_data: UserLogin):
    user = db.query(User).filter(User.Email == login_data.email).first()
    if user and user.Password == login_data.password:
        return user
    return None


def signup_user(db: Session, signup_data: UserSignup):
    # Create username based on fname and lname
    username = signup_data.fname.lower() + signup_data.lname.lower()
    # Formulate bio_status
    bio_status = f"Hello, I am {signup_data.fname} {signup_data.lname}"
    # Get current date as registration date
    registration_date = datetime.now().date()

    # Create user instance
    user = User(
        Username=username,
        DateOfBirth=signup_data.DateOfBirth,
        Password=signup_data.password,
        ProfilePicture="",
        Email=signup_data.email,
        DisabilityType=signup_data.disability_type,
        Fname=signup_data.fname,
        Lname=signup_data.lname,
        AccountStatus=signup_data.account_status,
        BioStatus=bio_status,
        RegistrationDate=registration_date,
        OnlineStatus=signup_data.online_status
    )

    # Add user to database
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User successfully created", "Id": user.Id}


def uploadprofilepicture_user(db: Session, id: int, profile_picture: UploadFile):
    try:
        # Fetch the user by id
        user = db.query(User).filter(User.Id == id).first()
        if user is None:
            return {"message": "User not found"}

        # Define the directory where images will be saved
        image_dir = "C:\\Users\\dell\\PycharmProjects\\CommFusionAPI\\app\\images"
        # os.makedirs(image_dir, exist_ok=True)  # Create the directory if it doesn't exist

        # Generate a unique filename for the uploaded file
        filename = profile_picture.filename
        file_path = os.path.join(image_dir, filename)

        # Write the file to disk
        with open(file_path, "wb") as f:
            f.write(profile_picture.file.read())

        # Update the ProfilePicture attribute in the user model
        user.ProfilePicture = file_path

        # Commit the changes to the database
        db.commit()

        return {"message": "Profile picture saved and user updated successfully", "Id": user.Id}
    except Exception as e:
        return {"message": f"An error occurred: {str(e)}"}


def get_user_details(db: Session, user_id: int):
    user = db.query(User).filter(User.Id == user_id).first()
    if not user:
        return None

    user_details = {
        "fname": user.Fname,
        "lname": user.Lname,
        "DateOfBirth": user.DateOfBirth,
        "password": user.Password,
        "profile_picture": user.ProfilePicture,
        "email": user.Email,
        "disability_type": user.DisabilityType,
        "account_status": user.AccountStatus,
        "bio_status": user.BioStatus,
        "registration_date": user.RegistrationDate,
        "online_status": user.OnlineStatus
    }
    return user_details


def search_user(db: Session, user_id: int, search_username: str):
    try:
        user = db.query(User).filter(User.Username == search_username).first()
        if not user:
            return {"message": "User not found"}, 404

        friend = db.query(Contacts).filter(Contacts.UserId == user_id, Contacts.ContactId == user.Id).first()

        is_friend = friend is not None  # Check if friend exists

        result = {
            'user_id': user.Id,
            'username': user.Username,
            'fname': user.Fname,
            'lname': user.Lname,
            'account_status': user.AccountStatus,
            'is_friend': is_friend
        }

        return result
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
