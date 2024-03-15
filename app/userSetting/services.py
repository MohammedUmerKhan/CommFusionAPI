from sqlalchemy.orm import Session
from app.userSetting.models import UserSetting
from fastapi import HTTPException
from typing import Dict


def get_user_settings(db: Session, user_id: int):
    try:
        user_settings = db.query(UserSetting.SettingName, UserSetting.SettingValue).filter(UserSetting.UserId == user_id).all()
        if user_settings:
            return user_settings
        else:
            return {}
    except Exception as e:
        # Log the error or handle it in another way (e.g., returning an error message)
        return {"error": str(e)}
