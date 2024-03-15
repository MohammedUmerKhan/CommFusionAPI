from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import database
from app.userSetting.services import get_user_settings
from app.userSetting.schemas import UserSettings
from typing import List
router = APIRouter(prefix="/usersettings", tags=['User Settings'])


@router.get("/{user_id}", response_model=List[UserSettings])
def read_user_settings(user_id: int, db: Session = Depends(database.get_db)):
    user_settings = get_user_settings(db, user_id)
    if not user_settings:
        raise HTTPException(status_code=404, detail="User settings not found")
    return user_settings
