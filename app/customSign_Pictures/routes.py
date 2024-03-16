from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import database
from app.customSign_Pictures.schemas import CustomSignPictureCreate
from app.customSign_Pictures.services import upload_custom_sign_picture

router = APIRouter(prefix="/customsignpictures", tags=['Custom Sign Pictures'])


@router.post("/{custom_sign_id}")
def upload_custom_sign_pictures(custom_sign_id: int, files: List[UploadFile] = File(...), db: Session = Depends(database.get_db)):
    return upload_custom_sign_picture(db, custom_sign_id, files)
