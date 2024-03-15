from typing import Dict
from pydantic import BaseModel


class UserSettings(BaseModel):
    SettingName: str
    SettingValue: str


class UpdateUserSettings(BaseModel):
    user_id: int
    settings: Dict[str, str]
