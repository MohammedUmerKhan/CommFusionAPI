# routes.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.db import database
from app.customSign.services import get_custom_signs, create_custom_sign, check_custom_sign_existence, \
    save_images_and_create_custom_sign
from app.customSign.schemas import CustomSignDetails, CustomSignCreate
from typing import List

router = APIRouter(prefix="/customsign", tags=['Custom Signs'])


@router.get("/{user_id}", response_model=List[CustomSignDetails])
def get_user_custom_signs(user_id: int, db: Session = Depends(database.get_db)):
    custom_signs = get_custom_signs(db, user_id)
    if not custom_signs:
        raise HTTPException(status_code=404, detail="Custom signs not found for the user")
    return custom_signs


@router.post("/", response_model=int)
def create_customsign(user_id: int, sign_data: CustomSignCreate, db: Session = Depends(database.get_db)):
    sign_id = create_custom_sign(db, user_id, sign_data)
    return sign_id


@router.get("/check/{user_id}/{definition}")
def check_custom_sign(user_id: int, definition: str, db: Session = Depends(database.get_db)):
    exists = check_custom_sign_existence(db, user_id, definition)
    if exists:
        return {"message": "Custom sign already requested"}
    else:
        return {"message": "New custom sign detected"}


@router.post("/with_images/", response_model=int)
def create_customsign_with_images(
        user_id: int,
        definition: str,
        images: List[UploadFile] = File(...),
        db: Session = Depends(database.get_db)
):
    if len(images) != 10:
        raise HTTPException(status_code=400, detail="Exactly 10 images are required.")
    sign_id = save_images_and_create_custom_sign(db, user_id, definition, images)
    return sign_id
