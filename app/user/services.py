import os
import uuid
from datetime import date
from fastapi import UploadFile, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.user.models import User
from app.contacts.models import Contacts
from app.user.schemas import UserLogin, UpdateUserProfile, UpdateBioStatus,UserDetails
from app.user.schemas import UserSignup


def get_users(db: Session):
    return db.query(User).all()


def authenticate_user(db: Session, login_data: UserLogin):
    user = db.query(User).filter(User.Email == login_data.email).first()
    if user and user.Password == login_data.password:
        return user
    return None


def signup_user(db: Session, signup_data: UserSignup):
    # Check if the email address is already registered
    email_exists = db.query(User).filter(User.Email == signup_data.email).first()
    if email_exists:
        raise HTTPException(status_code=400, detail="Email is already registered")

    # Create username based on fname and lname
    base_username = signup_data.fname.lower() + signup_data.lname.lower()
    username = base_username
    username_exists = db.query(User).filter(User.Username == username).first()

    # If the username already exists, append a number until it becomes unique
    counter = 1
    while username_exists:
        username = f"{base_username}{counter}"
        username_exists = db.query(User).filter(User.Username == username).first()
        counter += 1

    # # Formulate bio_status
    # bio_status = f"Hello, I am {signup_data.fname} {signup_data.lname}"
    # Get current date as registration date
    registration_date = datetime.now().date()
    # Set default values for account_status, registration_date, and online_status
    account_status = "Active"

    online_status = 1  # Default value
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
        AccountStatus=account_status,
        BioStatus=signup_data.bio_status,
        RegistrationDate=registration_date,
        OnlineStatus=online_status
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
        image_dir = "app/assets/images/profile/"
        # Create the directory if it doesn't exist
        os.makedirs(image_dir, exist_ok=True)

        # Generate a unique filename for the uploaded file
        unique_filename = f"{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        file_path = os.path.join(image_dir, unique_filename)

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

    return UserDetails(
        Id=user.Id,
        username=user.Username,
        fname=user.Fname,
        lname=user.Lname,
        DateOfBirth=user.DateOfBirth,
        password=user.Password,
        profile_picture=user.ProfilePicture,
        email=user.Email,
        disability_type=user.DisabilityType,
        account_status=user.AccountStatus,
        bio_status=user.BioStatus,
        registration_date=user.RegistrationDate,
        online_status=user.OnlineStatus
    )

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
            'is_friend': is_friend,
            'profile_picture': user.ProfilePicture
        }

        return result
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


def search_user_by_email(db: Session, user_id: int, email: str):
    try:
        user = db.query(User).filter(User.Email == email).first()
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
            'is_friend': is_friend,
            'profile_picture': user.ProfilePicture
        }

        return result
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_user_profile(db: Session, data: UpdateUserProfile):
    try:
        # Retrieve the user
        user = db.query(User).filter_by(Id=data.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Validate current password
        if user.Password != data.current_password:
            raise HTTPException(status_code=401, detail="Incorrect current password")

        # Update profile information
        if data.new_fname:
            user.Fname = data.new_fname

        if data.new_lname:
            user.Lname = data.new_lname

        if data.new_bio_status:
            user.BioStatus = data.new_bio_status

        if data.new_disability_type:
            user.DisabilityType = data.new_disability_type

        if data.new_password:
            user.Password = data.new_password

        db.commit()

        return {"message": "Profile updated successfully"}, 200

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_user_online_status(db: Session, user_id: int, online_status: int):
    try:
        # Fetch the user by id
        user = db.query(User).filter(User.Id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Update the OnlineStatus attribute in the user model
        user.OnlineStatus = online_status

        # Commit the changes to the database
        db.commit()

        return {"message": "User online status updated successfully", "Id": user.Id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


def update_user_account_status_to_deleted(db: Session, user_id: int):
    try:
        # Fetch the user by id
        user = db.query(User).filter(User.Id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Update the AccountStatus attribute to "Deleted" in the user model
        user.AccountStatus = "Deleted"

        # Commit the changes to the database
        db.commit()

        return {"message": "User account status updated to 'Deleted' successfully", "Id": user.Id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


def get_user_profile(db: Session, user_id: int):
    user = db.query(User).filter(User.Id == user_id).first()
    if not user:
        return None

    user_profile = {
        "user_id": user.Id,
        "profile_picture": user.ProfilePicture,
    }
    return user_profile


def update_user_bio_status(db: Session, data: UpdateBioStatus):
    # Get the user by user_id
    user = db.query(User).filter(User.Id == data.user_id).first()
    if not user:
        return {"message": "User not found"}

    # If bio_status is empty, set it to the default value
    if not data.bio_status:
        default_bio_status = "Hi, I am using CommFusion"
        user.BioStatus = default_bio_status
        db.commit()
        return {"message": "Default bio status set successfully", "default_bio_status": default_bio_status}
    else:
        # Update the bio status with the provided value
        user.BioStatus = data.bio_status
        db.commit()
        return {"message": "Bio status added successfully"}
