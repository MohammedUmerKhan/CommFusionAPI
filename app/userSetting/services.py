from sqlalchemy.orm import Session
from app.userSetting.models import UserSetting
from app.userSetting.schemas import DefaultUserSettings
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


from sqlalchemy.orm import Session
from app.userSetting.models import UserSetting

def create_default_user_settings(db: Session, user_id: int):
    default_settings = DefaultUserSettings()
    try:
        user_settings = UserSetting(
            UserId=user_id,
            SettingName='TranscriptionFontSize',
            SettingValue=default_settings.TranscriptionFontSize
        )
        db.add(user_settings)

        user_settings = UserSetting(
            UserId=user_id,
            SettingName='TranscriptionOpacity',
            SettingValue=default_settings.TranscriptionOpacity
        )
        db.add(user_settings)

        user_settings = UserSetting(
            UserId=user_id,
            SettingName='TranscriptionColor',
            SettingValue=default_settings.TranscriptionColor
        )
        db.add(user_settings)

        user_settings = UserSetting(
            UserId=user_id,
            SettingName='Notifications',
            SettingValue=default_settings.Notifications
        )
        db.add(user_settings)

        user_settings = UserSetting(
            UserId=user_id,
            SettingName='Ringtone',
            SettingValue=default_settings.Ringtone
        )
        db.add(user_settings)

        db.commit()
        return {"message": "Default user settings created successfully"}, 201
    except Exception as e:
        return {"error": str(e)}, 500
