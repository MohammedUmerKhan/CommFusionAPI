import os
import uuid
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, UploadFile

from app.customSign_Pictures.models import CustomSign_Pictures
from app.customSign.models import CustomSign
from app.customSign_Pictures.schemas import CustomSignPictureCreate


def upload_custom_sign_picture(db: Session, custom_sign_id: int, files: List[UploadFile]):
    try:
        # Ensure CustomSignId exists
        custom_sign_exists = db.query(CustomSign).filter_by(Id=custom_sign_id).first()
        if not custom_sign_exists:
            raise HTTPException(status_code=404, detail="CustomSign not found")

        # Define the directory where images will be saved
        image_dir = "C:\\Users\\dell\\PycharmProjects\\CommFusionAPI\\app\\assets\\images\\customSign"
        os.makedirs(image_dir, exist_ok=True)

        # Iterate over each uploaded file
        for file in files:
            # Generate a unique filename for the uploaded file
            unique_filename = f"{uuid.uuid4().hex}.png"
            file_path = os.path.join(image_dir, unique_filename)

            # Write the file to disk
            with open(file_path, "wb") as f:
                f.write(file.file.read())

            # Save the file path to the database
            custom_sign_picture = CustomSignPictureCreate(Picture=file_path, CustomSignId=custom_sign_id)
            db_custom_sign_picture = CustomSign_Pictures(**custom_sign_picture.dict())
            db.add(db_custom_sign_picture)

        # Commit changes to the database
        db.commit()

        return {"message": "Custom sign pictures uploaded successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
