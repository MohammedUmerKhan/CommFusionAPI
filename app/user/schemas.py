from pydantic import BaseModel
from datetime import date


class UserLogin(BaseModel):
    email: str
    password: str


class UserBase(BaseModel):
    Username: str
    Email: str
    # Add other fields as needed


class UserCreate(UserBase):
    Password: str
    # Add other fields as needed


class User(UserBase):
    Id: int
    DisabilityType: str

    # Add other fields as needed

    class Config:
        from_attributes = True


class UserSignup(BaseModel):
    fname: str
    lname: str
    DateOfBirth: date
    password: str
    email: str
    disability_type: str
    account_status: str = "Active"  # Default value
    bio_status: str = ""
    registration_date: date  # Automatically generated
    online_status: int = 1  # Default value


class UserDetails(BaseModel):
    fname: str
    lname: str
    DateOfBirth: date
    password: str
    profile_picture: str  # Assuming the file path for profile picture
    email: str
    disability_type: str
    account_status: str = "Active"  # Default value
    bio_status: str = ""
    registration_date: date  # Automatically generated
    online_status: int = 1  # Default value


class UserSearchResult(BaseModel):
    user_id: int
    username: str
    fname: str
    lname: str
    account_status: str
    is_friend: bool


class UpdateUserProfile(BaseModel):
    user_id: int
    current_password: str
    new_password: str = None
    new_fname: str = None
    new_lname: str = None
    new_bio_status: str = None
    new_disability_type: str = None
