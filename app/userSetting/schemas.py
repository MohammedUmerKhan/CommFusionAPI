from typing import Dict
from pydantic import BaseModel


class UserSettings(BaseModel):
    SettingName: str
    SettingValue: str


class UpdateUserSettings(BaseModel):
    user_id: int
    settings: Dict[str, str]

class DefaultUserSettings(BaseModel):
    TranscriptionFontSize: str = '20'
    TranscriptionOpacity: str = '5'
    TranscriptionColor: str = 'black'
    Notifications: str = 'Enabled'
    Ringtone: str = 'Xylophone'
