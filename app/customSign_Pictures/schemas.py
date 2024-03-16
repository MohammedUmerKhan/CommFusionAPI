from pydantic import BaseModel
from typing import List

class CustomSignPictureBase(BaseModel):
    Picture: str
    CustomSignId: int

class CustomSignPictureCreate(CustomSignPictureBase):
    pass
