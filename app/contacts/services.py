from sqlalchemy.orm import Session
from app.user.models import User
from app.contacts.models import Contacts
from app.contacts.schemas import UserContact, AddContactRequest, SearchedUserContact
from fastapi import HTTPException


def get_contacts(db: Session):
    try:
        return db.query(Contacts).all()
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def get_all_user_contacts(db: Session, user_id: int):
    try:
        contacts = db.query(User.Id, User.Fname, User.Lname, User.Username, User.DisabilityType, User.ProfilePicture,
                            User.AccountStatus, User.BioStatus, User.OnlineStatus) \
            .join(Contacts, User.Id == Contacts.ContactId) \
            .filter(Contacts.UserId == user_id).all()

        contacts_data = [
            UserContact(user_id=user_id, fname=fname, lname=lname, username=username, disability_type=disability_type,
                        profile_picture=profile_picture, account_status=account_status, bio_status=bio_status,
                        online_status=online_status)
            for
            user_id, fname, lname, username, disability_type, profile_picture, account_status, bio_status, online_status
            in contacts]

        return contacts_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def add_contact(db: Session, request: AddContactRequest):
    try:
        # Check if the other user is already a contact
        existing_contact = db.query(Contacts).filter_by(UserId=request.user_id, ContactId=request.contact_id).first()
        if existing_contact:
            raise HTTPException(status_code=400, detail="The other user is already a contact")

        # Check if the user exists
        user = db.query(User).filter_by(Id=request.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if the contacts user exists
        contacts_user = db.query(User).filter_by(Id=request.contact_id).first()
        if not contacts_user:
            raise HTTPException(status_code=404, detail="Contacts user not found")

        # Add the user as a contact for the other user
        contact = Contacts(UserId=request.user_id, ContactId=request.contact_id, IsBlocked=request.is_blocked)
        db.add(contact)
        db.commit()

        return {"message": "User added as a contact successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_online_contacts(db: Session, user_id: int):
    try:
        online_contacts = db.query(User.Id, User.Fname, User.Lname, User.Username, User.DisabilityType,
                                   User.ProfilePicture, User.AccountStatus, User.BioStatus, User.OnlineStatus) \
            .join(Contacts, User.Id == Contacts.ContactId) \
            .filter(Contacts.UserId == user_id, User.OnlineStatus == 1).all()

        contacts_data = [
            UserContact(user_id=user_id, fname=fname, lname=lname, username=username, disability_type=disability_type,
                        profile_picture=profile_picture, account_status=account_status, bio_status=bio_status,
                        online_status=online_status)
            for
            user_id, fname, lname, username, disability_type, profile_picture, account_status, bio_status, online_status
            in online_contacts]

        return contacts_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def search_contacts(db: Session, user_id: int, search_string: str):
    try:
        searched_contacts = db.query(User.Id, User.Username, User.Fname, User.Lname, User.DisabilityType,
                                     User.ProfilePicture, User.AccountStatus, User.BioStatus, User.OnlineStatus) \
            .join(Contacts, Contacts.ContactId == User.Id) \
            .filter(Contacts.UserId == user_id,
                    (User.Fname.ilike(f'%{search_string}%')) | (User.Lname.ilike(f'%{search_string}%'))).all()

        searched_contacts_data = [
            SearchedUserContact(Id=user_id, username=username, fname=fname, lname=lname, DisabilityType=disability_type,
                                ProfilePicture=profile_picture, AccountStatus=account_status, BioStatus=bio_status,
                                OnlineStatus=online_status)
            for
            user_id, username, fname, lname, disability_type, profile_picture, account_status, bio_status, online_status
            in searched_contacts]

        return searched_contacts_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
