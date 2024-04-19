from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import database
from app.contacts.services import get_all_user_contacts, get_online_contacts, get_contacts, add_contact,search_contacts
from app.contacts.schemas import UserContact, Contacts, AddContactRequest, SearchedUserContact
from typing import List

router = APIRouter(prefix="/contacts", tags=['Contacts'])


@router.get("/all", response_model=List[Contacts])
def get_all_contacts(db: Session = Depends(database.get_db)):
    return get_contacts(db)


@router.get("/{user_id}/contacts", response_model=List[UserContact])
def get_user_contacts(user_id: int, db: Session = Depends(database.get_db)):
    return get_all_user_contacts(db, user_id)


@router.get("/{user_id}/online-contacts", response_model=List[UserContact])
def get_online_user_contacts(user_id: int, db: Session = Depends(database.get_db)):
    return get_online_contacts(db, user_id)


@router.post("/add", response_model=None)
def add_new_contact(request: AddContactRequest, db: Session = Depends(database.get_db)):
    return add_contact(db, request)


@router.get("/search", response_model=List[SearchedUserContact])
def search_user_contacts(user_id: int, search_string: str, db: Session = Depends(database.get_db)):
    return search_contacts(db, user_id, search_string)
