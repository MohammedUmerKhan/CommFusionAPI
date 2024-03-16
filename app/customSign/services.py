# services.py
from sqlalchemy.orm import Session
from app.customSign.models import CustomSign
from app.customSign_Pictures.models import  CustomSign_Pictures
from typing import List
from app.customSign.schemas import CustomSignDetails


def get_custom_signs(db: Session, user_id: int) -> List[CustomSignDetails]:
    custom_signs = (
        db.query(CustomSign)
        .filter(CustomSign.UserId == user_id)
        .join(CustomSign_Pictures, CustomSign.Id == CustomSign_Pictures.CustomSignId)
        .all()
    )
    if not custom_signs:
        return []

    custom_sign_details = []
    for sign in custom_signs:
        pictures = [pic.Picture for pic in sign.customSign_CSpictures]
        sign_details = CustomSignDetails(
            id=sign.Id,
            status=sign.Status,
            definition=sign.Definition,
            pictures=pictures
        )
        custom_sign_details.append(sign_details)

    return custom_sign_details
