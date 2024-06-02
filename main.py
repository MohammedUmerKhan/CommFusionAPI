from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from pydantic import BaseModel
import pickle
from app.db import Database
from app.user import models as user
from app.contacts import models as contacts
from app.customSign import models as customSign
from app.customSign_Pictures import models as customSign_Pictures
from app.gesture import models as gesture
from app.lesson import models as lesson
from app.transcriptFeedback import models as transcriptFeedback
from app.transcriptFeedback_Images import models as transcriptFeedback_Images
from app.transcriptSegment import models as transcriptSegment
from app.userFavouriteGesture import models as userFavouriteGesture
from app.userSetting import models as userSetting
from app.userTakesLesson import models as userTakesLesson
from app.videoCall import models as videoCall
from app.videoCallParticipants import models as videoCallParticipants
from app.user.routes import router as users_router
from app.contacts.routes import router as contacts_router
from app.videoCallParticipants.routes import router as videoCallParticipants_router
from app.customSign.routes import router as customSign_router
from app.customSign_Pictures.routes import router as customSign_Pictures_router
from app.userFavouriteGesture.routes import router as userFavouriteGesture_router
from app.userSetting.routes import router as userSettings_router
from app.lesson.routes import router as lesson_router
from app.gesture.routes import router as gesture_router
from app.userTakesLesson.routes import router as userTakesLesson_router
from app.videoCall.routes import router as videoCall_router
from app.transcriptFeedback.routes import router as transcriptFeedback_router
from app.transcriptSegment.routes import router as transcriptSegment_router
# from app.model.image_classifier import router as image_router

# from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
# import cv2
# import mediapipe as mp
# import numpy as np
import torch
import torchvision.transforms as transforms
import torch.nn.functional as F
import numpy as np
from PIL import Image
import io
from fastapi import APIRouter, File, UploadFile
import cv2
import mediapipe as mp
from app.model.actions import ActionHandler
import sys
from io import BytesIO
import uvicorn

app = FastAPI()
# Define the directory where profile pictures are stored
PROFILE_PICTURES_DIR = "app/assets/images/profile"

# Mount the directory as a route for serving static files
app.mount("/profile_pictures", StaticFiles(directory=PROFILE_PICTURES_DIR), name="profile_pictures")

# This is for mounting the gestures
# Define another directory to be served
GESTURE_DIR = "app/assets/images/gestures"
# Mount the additional directory
app.mount("/gestures_files", StaticFiles(directory=GESTURE_DIR), name="gestures_files")

# Mount routers
# app.include_router(image_router)
app.include_router(users_router)
app.include_router(contacts_router)
app.include_router(videoCallParticipants_router)
app.include_router(customSign_router)
app.include_router(customSign_Pictures_router)
app.include_router(userFavouriteGesture_router)
app.include_router(userSettings_router)
app.include_router(lesson_router)
app.include_router(gesture_router)
app.include_router(userTakesLesson_router)
app.include_router(videoCall_router)
app.include_router(transcriptFeedback_router)
app.include_router(transcriptSegment_router)


@app.get("/")
def check_db_connection():
    return {'Message': 'Go to Url /docs or /redocs to view the API UI'}


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
# Initialize MediaPipe Hands
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)


# base model
class Item(BaseModel):
    class_name: str
    confidence: float


@app.post('/detect_hand')
async def detect_hand(image: UploadFile = File(...)):
    try:
        # Read the image from the request
        image_bytes = await image.read()

        # Convert image bytes to OpenCV format
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Convert BGR to RGB since MediaPipe expects RGB images
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image to detect hands
        results = hands.process(rgb_image)

        # Check if any hands were detected
        if results.multi_hand_landmarks:
            # Iterate over each detected hand
            for hand_landmarks in results.multi_hand_landmarks:
                # Convert landmarks to a NumPy array
                hand_landmarks_array = np.array([[data.x, data.y, data.z] for data in hand_landmarks.landmark])

                # Calculate bounding box coordinates
                x_min, y_min, _ = np.min(hand_landmarks_array, axis=0)
                x_max, y_max, _ = np.max(hand_landmarks_array, axis=0)
                padding = 0.05  # Padding factor to expand the bounding box slightly
                x_min -= padding
                y_min -= padding
                x_max += padding
                y_max += padding

                # Convert normalized coordinates to pixel coordinates
                x_min, y_min, x_max, y_max = max(0, x_min), max(0, y_min), min(1, x_max), min(1, y_max)
                bbox = [int(x_min * image.shape[1]), int(y_min * image.shape[0]), int(x_max * image.shape[1]),
                        int(y_max * image.shape[0])]

                # Log the bounding box coordinates for debugging
                print(f"BBox: {bbox}")

                # Extract the hand image using the bounding box
                hand_img = image[bbox[1]:bbox[3], bbox[0]:bbox[2]]

                # Check if the extracted hand image is empty
                if hand_img.size == 0:
                    print("Empty hand image detected, skipping.")
                    continue
                # Preprocess hand image to tensors
                pil_img = Image.fromarray(hand_img)
                pil_img = transform(pil_img).unsqueeze(0).to(device)  # Move tensor to the correct device

                # Inferencing to predict the class
                with torch.no_grad():  # Use torch.no_grad() for efficiency
                    outputs = model(pil_img)

                    _, predicted = torch.max(outputs, 1)
                    confidence_value = F.softmax(outputs, dim=1).max().item()
                    predicted_class = predicted.item()

                    # Get the class label
                    action = class_labels[predicted_class]

                    # Create an instance of ActionHandler with the confidence value and action
                    handler = ActionHandler(confidence_value, action)
                    handler.execute_action()
                    # Return the classification result
                    return Item(class_name=action, confidence=confidence_value)

        # # Construct a dynamic output path for the cropped image
        # output_dir = os.path.join(os.getcwd(), 'output_images')
        # os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
        # output_path = os.path.join(output_dir, 'cropped_hand_image.jpg')
        #
        # # Save the cropped hand image
        # cv2.imwrite(output_path, hand_img)
        # print(f"Cropped image saved to {output_path}")  # Debugging output
        #
        # # Return a success message indicating the cropped image was processed and saved
        # return {'message': 'Cropped hand image saved as "cropped_hand_image.jpg".'}

    except Exception as e:
        # Handle exceptions by returning an error response
        return JSONResponse(status_code=500, content={'error': str(e)})


def process_image(image: np.ndarray):
    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError("Input image must be a 3-channel RGB image.")
    # print(f"Processing image with shape: {image.shape}")

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the frame using MediaPipe Hands
    results = hands.process(frame_rgb)
    label = "No gesture detected"

    # Analyze hand landmarks and detect gestures
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Landmarks for thumb, index, middle, ring, and pinky fingers
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            middle_tip = hand_landmarks.landmark[12]
            ring_tip = hand_landmarks.landmark[16]
            pinky_tip = hand_landmarks.landmark[20]

            thumb_ip = hand_landmarks.landmark[2]
            index_ip = hand_landmarks.landmark[6]
            middle_ip = hand_landmarks.landmark[10]
            ring_ip = hand_landmarks.landmark[14]
            pinky_ip = hand_landmarks.landmark[18]

            # Check for "I love you" gesture
            if (thumb_tip.y < thumb_ip.y and
                    index_tip.y < index_ip.y and
                    pinky_tip.y < pinky_ip.y and
                    middle_tip.y > middle_ip.y and
                    ring_tip.y > ring_ip.y):
                label = "I love you"

            # Check for "OK" gesture
            distance_index_thumb = ((index_tip.x - thumb_tip.x) ** 2 + (index_tip.y - thumb_tip.y) ** 2) ** 0.5
            threshold_distance = 0.05  # Adjust the threshold as needed

            if (distance_index_thumb < threshold_distance and
                    middle_tip.y < middle_ip.y and
                    ring_tip.y < ring_ip.y and
                    pinky_tip.y < pinky_ip.y):
                label = "OK"

            # Check for thumbs-down gesture ("I'm not doing great")
            thumb_landmarks = [hand_landmarks.landmark[i] for i in [4, 3, 2]]
            if thumb_landmarks[0].y > thumb_landmarks[1].y > thumb_landmarks[2].y:
                label = "I'm not doing great"

            # Check for thumbs-up gesture ("I am fine")
            thumb_up_landmarks = [hand_landmarks.landmark[i] for i in [2, 3, 4]]  # Thumb landmarks
            other_landmarks = [lm for i, lm in enumerate(hand_landmarks.landmark) if i not in [2, 3, 4]]

            if all(tu.y < ol.y for tu in thumb_up_landmarks for ol in other_landmarks):
                label = "I am fine"

            # Check if all fingers are open ("hello")
            fingers_open = True
            landmark_ids = [
                [4, 3, 2, 1],  # Thumb
                [8, 7, 6, 5],  # Index finger
                [12, 11, 10, 9],  # Middle finger
                [16, 15, 14, 13],  # Ring finger
                [20, 19, 18, 17]  # Pinky
            ]

            for ids in landmark_ids:
                if not all(hand_landmarks.landmark[ids[i]].y < hand_landmarks.landmark[ids[i + 1]].y for i in
                           range(len(ids) - 1)):
                    fingers_open = False
                    break

            if fingers_open:
                label = "hello"

            # Check for "Call me" gesture
            if (thumb_tip.y < thumb_ip.y and pinky_tip.y < pinky_ip.y and
                    index_tip.y > index_ip.y and middle_tip.y > middle_ip.y and ring_tip.y > ring_ip.y):
                label = "Call me"

            # Check for "Victory Fist" gesture
            if (thumb_tip.y < thumb_ip.y and index_tip.y < index_ip.y and
                    middle_tip.y < middle_ip.y and ring_tip.y > ring_ip.y and pinky_tip.y > pinky_ip.y):
                label = "Victory"

    return label


@app.post("/predictWP")
async def predict(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()

        # Convert image bytes to OpenCV format
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        label = process_image(image)
        if label == "No gesture detected":
            return
        return JSONResponse(content={"label": label})
    except Exception as e:
        # Handle exceptions by returning an error response
        return JSONResponse(status_code=500, content={'error': str(e)})


# Load the models once when the app starts
with open('one_hand_model.pkl', 'rb') as f:
    one_hand_model = pickle.load(f)

with open('two_hand_model.pkl', 'rb') as f:
    two_hand_model = pickle.load(f)


def image_processed(hand_img):
    img_rgb = cv2.cvtColor(hand_img, cv2.COLOR_BGR2RGB)
    output = hands.process(img_rgb)

    landmarks_list = []
    if output.multi_hand_landmarks:
        for hand_landmarks in output.multi_hand_landmarks:
            landmarks = [np.array([landmark.x, landmark.y, landmark.z]) for landmark in hand_landmarks.landmark]
            landmarks = np.array(landmarks).flatten()
            landmarks_list.append(landmarks)

    return landmarks_list


@app.post("/predictBSL")
async def predict_bsl(file: UploadFile = File(...)):
    contents = await file.read()

    # Convert image bytes to OpenCV format
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    landmarks_list = image_processed(image)

    if len(landmarks_list) == 0:
        return
        output = "No hands detected"
    else:
        if len(landmarks_list) == 1:
            model = one_hand_model
            data = np.array(landmarks_list[0]).reshape(1, -1)
        elif len(landmarks_list) == 2:
            model = two_hand_model
            data = np.concatenate(landmarks_list[:2]).reshape(1, -1)
        y_pred = model.predict(data)
        raw_output = y_pred[0]
        # Extract the label part from the prediction
        label = raw_output.split(' - ')[0] if ' - ' in raw_output else raw_output
        output = label


    return JSONResponse(content={"prediction": output})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
