from typing import Dict
from pydantic import BaseModel


class UserSettings(BaseModel):
    SettingName: str
    SettingValue: str


class UpdateUserSettings(BaseModel):
    user_id: int
    settings: Dict[str, str]

class DefaultUserSettings(BaseModel):
    TranscriptionFontSize: str = '12px'
    TranscriptionOpacity: str = '0.8'
    TranscriptionColor: str = 'black'
    Notifications: str = 'Enabled'
    Ringtone: str = 'default_ringtone.mp3'
