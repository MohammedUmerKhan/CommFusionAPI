# services.py
from sqlalchemy.orm import Session
from app.customSign.models import CustomSign
from app.customSign_Pictures.models import CustomSign_Pictures
from app.customSign.schemas import CustomSignDetails, CustomSignCreate
from typing import List
from sqlalchemy import func
from fastapi import UploadFile, HTTPException
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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


def create_custom_sign(db: Session, user_id: int, sign_data: CustomSignCreate) -> int:
    new_sign = CustomSign(UserId=user_id, Definition=sign_data.definition, Status=sign_data.status)
    db.add(new_sign)
    db.commit()
    db.refresh(new_sign)
    return new_sign.Id


def check_custom_sign_existence(db: Session, user_id: int, definition: str) -> bool:
    exists = (
        db.query(CustomSign)
        .filter(CustomSign.UserId == user_id, func.lower(CustomSign.Definition) == func.lower(definition))
        .first()
    )
    return exists is not None


# def save_images_and_create_custom_sign(db: Session, user_id: int, definition: str, images: List[UploadFile]) -> int:
#     # Create the new custom sign
#     new_sign = CustomSign(UserId=user_id, Definition=definition, Status="Pending")
#     db.add(new_sign)
#     db.commit()
#     db.refresh(new_sign)
#
#     # Define the directory structure
#     base_dir = os.path.join("assets", "ai")
#     user_dir = os.path.join(base_dir, str(user_id))
#     model_dir = os.path.join(user_dir, "model")
#     dataset_dir = os.path.join(user_dir, "dataset")
#     definition_dir = os.path.join(dataset_dir, definition.replace(" ", "_"))
#
#     # Create directories if they don't exist
#     os.makedirs(model_dir, exist_ok=True)
#     os.makedirs(definition_dir, exist_ok=True)
#
#     # Save images
#     for idx, image in enumerate(images):
#         image_filename = f"{definition.replace(' ', '_')}_{idx}.jpg"
#         image_path = os.path.join(definition_dir, image_filename)
#         with open(image_path, "wb") as img_file:
#             img_file.write(image.file.read())
#
#     return new_sign.Id

def save_images_and_create_custom_sign(db: Session, user_id: int, definition: str, images: List[UploadFile]) -> int:
    try:
        # Create the new custom sign
        new_sign = CustomSign(UserId=user_id, Definition=definition, Status="Pending")
        db.add(new_sign)
        db.commit()
        db.refresh(new_sign)
        logger.info(f"Created new CustomSign with ID: {new_sign.Id}")

        # Define the directory structure
        base_dir = os.path.join(BASE_DIR, "assets", "ai")
        user_dir = os.path.join(base_dir, str(user_id))
        model_dir = os.path.join(user_dir, "model")
        dataset_dir = os.path.join(user_dir, "dataset")
        definition_dir = os.path.join(dataset_dir, definition.replace(" ", "_"))

        # Create directories if they don't exist
        for directory in [model_dir, definition_dir]:
            try:
                os.makedirs(directory, exist_ok=True)
                logger.info(f"Created directory: {directory}")
            except Exception as e:
                logger.error(f"Error creating directory {directory}: {e}")
                raise HTTPException(status_code=500, detail=f"Failed to create directory: {e}")

        # Save images
        for idx, image in enumerate(images):
            try:
                image_filename = f"{definition.replace(' ', '_')}_{idx}.jpg"
                image_path = os.path.join(definition_dir, image_filename)
                logger.info(f"Saving image to: {image_path}")

                with open(image_path, "wb") as img_file:
                    img_file.write(image.file.read())

                if os.path.exists(image_path):
                    logger.info(f"Successfully saved image: {image_path}")
                else:
                    logger.warning(f"Image file not found after saving: {image_path}")
            except Exception as e:
                logger.error(f"Error saving image {idx}: {e}")
                raise HTTPException(status_code=500, detail=f"Failed to save image {idx}: {e}")

        return new_sign.Id

    except Exception as e:
        logger.error(f"Unexpected error in save_images_and_create_custom_sign: {e}")
        db.rollback()  # Rollback the database transaction if an error occurs
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
