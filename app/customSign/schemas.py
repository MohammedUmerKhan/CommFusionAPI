# schemas.py
from pydantic import BaseModel
from typing import List
from fastapi import UploadFile


class CustomSignDetails(BaseModel):
    id: int
    status: str
    definition: str
    pictures: List[str]


class CustomSignCreate(BaseModel):
    definition: str
    status: str = "Pending"


class CustomSignWithImages(BaseModel):
    user_id: int
    definition: str
    images: List[UploadFile]
