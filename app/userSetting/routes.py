from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import database
from app.userSetting.services import get_user_settings,update_user_settings, create_default_user_settings
from app.userSetting.schemas import UserSettings, UpdateUserSettings
from typing import List
router = APIRouter(prefix="/usersettings", tags=['User Settings'])


@router.get("/{user_id}", response_model=List[UserSettings])
def read_user_settings(user_id: int, db: Session = Depends(database.get_db)):
    user_settings = get_user_settings(db, user_id)
    if not user_settings:
        raise HTTPException(status_code=404, detail="User settings not found")
    return user_settings


@router.put("/settings")
def update_user_setting(settings: UpdateUserSettings, db: Session = Depends(database.get_db)):
    response = update_user_settings(db, settings.user_id, settings.settings)
    if "error" in response:
        raise HTTPException(status_code=500, detail="Failed to update user settings")
    return response


@router.post("/{user_id}/default")
def create_default_settings(user_id: int, db: Session = Depends(database.get_db)):
    return create_default_user_settings(db, user_id)
