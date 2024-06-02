import torch
import torchvision.transforms as transforms
import torch.nn.functional as F
import numpy as np
from PIL import Image
import io
from fastapi import APIRouter, File, UploadFile
import cv2
import mediapipe as mp
from app.model.actions  import ActionHandler
import sys

sys.path.append('../')
from app.model.neuralnet import model as nn_model

# Setting device agnostic code
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Load the PyTorch model
model_path = 'app/model/model/efficientnet_model.pth'
model_info = torch.load(model_path, map_location=torch.device('cpu'))
model = nn_model.EfficientNetB0(num_classes=29).to(device)
model.load_state_dict(model_info)
model.eval()

# # Initialize MediaPipe Hands
# mp_drawing = mp.solutions.drawing_utils
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2,min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Define class labels
class_labels = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E',
    5: 'F',
    6: 'G',
    7: 'H',
    8: 'I',
    9: 'J',
    10: 'K',
    11: 'L',
    12: 'M',
    13: 'N',
    14: 'O',
    15: 'P',
    16: 'Q',
    17: 'R',
    18: 'S',
    19: 'T',
    20: 'U',
    21: 'V',
    22: 'W',
    23: 'X',
    24: 'Y',
    25: 'Z',
    26: 'del',
    27: 'nothing',
    28: 'space'
}

# Define transforms for preprocessing the hand image
transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
])

router = APIRouter(prefix="/classify", tags=['Image Classification'])
@router.post("/")
def classify_image(file: UploadFile = File(...)):
    try:
        # Initialize MediaPipe Hands
        mp_drawing = mp.solutions.drawing_utils
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5,
                               min_tracking_confidence=0.5)
        # Read the image file
        contents = file.file.read()

        # Convert the bytes to a PIL Image
        img = Image.open(io.BytesIO(contents))

        # Convert the PIL Image to a NumPy array
        img_np = np.array(img)

        # Display the original image
        cv2.imshow('Original Image', img_np)
        cv2.waitKey(0)

        # Convert BGR to RGB
        img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

        # Display the image after color conversion
        cv2.imshow('After Color Conversion', img_np)
        cv2.waitKey(0)

        # Process the image with MediaPipe Hands
        results = hands.process(img_np)

        # Check if hands are detected
        if results.multi_hand_landmarks:
            annotated_image = img_np.copy()
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw bounding box around detected hands
                bbox =...  # Calculate bounding box as before
                cv2.rectangle(annotated_image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)

            # Display the image with bounding boxes
            cv2.imshow('Detected Hands', annotated_image)
            cv2.waitKey(0)

            # Further processing and visualization of cropped hand images...
            #...
        # Release MediaPipe Hands object
        hands.close()
        return {"error": "No hands detected in the image."}

    except Exception as e:
        return {"error": str(e)}

# @router.post("/")
# async def classify_image(file: UploadFile = File(...)):
#     try:
#         # Read the image file
#         contents = await file.read()
#
#         # Convert the bytes to a PIL Image
#         img = Image.open(io.BytesIO(contents))
#
#         # Convert the PIL Image to a NumPy array
#         img_np = np.array(img)
#
#         # Log the image shape
#         print(f"Image shape: {img_np.shape}")
#
#         # Convert BGR to RGB
#         img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
#
#         # Process the image with MediaPipe Hands
#         results = hands.process(img_np)
#
#         # Check if hands are detected
#         if results.multi_hand_landmarks:
#             for hand_landmarks in results.multi_hand_landmarks:
#                 # Extract bounding box coordinates
#                 hand_landmarks_array = np.array([[data.x, data.y, data.z] for data in hand_landmarks.landmark])
#                 x_min, y_min, z_min = np.min(hand_landmarks_array, axis=0)
#                 x_max, y_max, z_max = np.max(hand_landmarks_array, axis=0)
#                 padding = 0.05  # Change this value to increase/decrease the padding
#                 x_min -= padding
#                 y_min -= padding
#                 x_max += padding
#                 y_max += padding
#                 x_min, y_min, x_max, y_max = max(0, x_min), max(0, y_min), min(1, x_max), min(1, y_max)
#                 bbox = [int(x_min * img_np.shape[1]), int(y_min * img_np.shape[0]), int(x_max * img_np.shape[1]),
#                         int(y_max * img_np.shape[0])]
#
#                 # Log the bounding box coordinates
#                 print(f"BBox: {bbox}")
#
#                 # Extract the hand image
#                 hand_img = img_np[bbox[1]:bbox[3], bbox[0]:bbox[2]]
#
#                 # Check if the hand image is non-empty
#                 if hand_img.size == 0:
#                     print("Empty hand image detected, skipping.")
#                     continue
#
#                 # Preprocess hand image to tensors
#                 pil_img = Image.fromarray(hand_img)
#                 pil_img = transform(pil_img).unsqueeze(0).to(device)
#
#                 # Inferencing to predict the class
#                 with torch.inference_mode():
#                     outputs = model(pil_img)
#
#                     _, predicted = torch.max(outputs, 1)
#                     confidence_value = F.softmax(outputs, dim=1).max().item()
#                     predicted_class = predicted.item()
#
#                     # Get the class label
#                     action = class_labels[predicted_class]
#
#                     return {"gesture": action, "confidence": confidence_value}
#
#         return {"error": "No hands detected in the image."}
#
#     except Exception as e:
#         return {"error": str(e)}

@router.get("/test")
async def classify_image_s ():
    return "Route works"

