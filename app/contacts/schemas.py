from pydantic import BaseModel


class UserContact(BaseModel):
    user_id: int
    fname: str
    lname: str
    username: str
    disability_type: str
    profile_picture: str
    account_status: str
    bio_status: str
    online_status: int


class Contacts(BaseModel):
    UserId: int
    ContactId: int
    IsBlocked: int


class AddContactRequest(BaseModel):
    user_id: int
    contact_id: int
    is_blocked: int = 0  # Default value
