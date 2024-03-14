from pydantic import BaseModel
from typing import List
from datetime import datetime


class UserCallDetails(BaseModel):
    VideoCallId: int
    Fname: str
    Lname: str
    ProfilePicture: str
    OnlineStatus: str
    AccountStatus: str
    isCaller: int
    StartTime: datetime
    EndTime: datetime


class UserCallsResponse(BaseModel):
    user_calls: List[UserCallDetails]
