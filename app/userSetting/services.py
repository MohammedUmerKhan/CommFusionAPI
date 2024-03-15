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

def update_user_settings(db: Session, user_id: int, settings: Dict[str, str]):
    try:
        for setting_name, setting_value in settings.items():
            db.query(UserSetting).filter(UserSetting.UserId == user_id, UserSetting.SettingName == setting_name).update({"SettingValue": setting_value})
        db.commit()
        return {"message": "User settings updated successfully"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
