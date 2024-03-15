from typing import Dict, Any
from pydantic import BaseModel


class UserSettings(BaseModel):
    SettingName: str
    SettingValue: str
