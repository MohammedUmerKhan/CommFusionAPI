from pydantic import BaseModel


class UserContact(BaseModel):
    fname: str
    lname: str
    profile_picture: str
    account_status: str
    bio_status: str
    online_status: int
    user_id: int
    user_name: str


class Contacts(BaseModel):
    UserId: int
    ContactId: int
    IsBlocked: int


class AddContactRequest(BaseModel):
    user_id: int
    contact_id: int
    is_blocked: int = 0  # Default value
