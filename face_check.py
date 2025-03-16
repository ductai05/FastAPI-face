from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware 
import face_recognition
import pprint
import uvicorn
from pydantic import BaseModel
import numpy as np
from io import BytesIO
import json

def face_distance_to_conf(face_distance, face_match_threshold=0.6):
    if face_distance > face_match_threshold:
        range_val = (1.0 - face_match_threshold)
        linear_val = (1.0 - face_distance) / (range_val * 2.0)
        return linear_val
    else:
        range_val = face_match_threshold
        linear_val = 1.0 - (face_distance / (range_val * 2.0))
        return linear_val + ((1.0 - linear_val) * ((linear_val - 0.5) * 2))
    
def load_user_data():
    try:
        with open("user_data.json", "r") as f:
            user_data = json.load(f)
    except FileNotFoundError:
        user_data = {}
    return user_data

def save_user_data(user_data):
    with open("user_data.json", "w") as f:
        json.dump(user_data, f, indent=2, separators=(",", ":"))
    
class User(BaseModel):
    username: str
    password: str

app = FastAPI()

# Thêm CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Địa chỉ của frontend
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các methods (GET, POST, etc.)
    allow_headers=["*"],  # Cho phép tất cả các headers
)

@app.get("/")
def read_root():
    return {"Hello": "Thís is DucTai"}

@app.get("/get_names")
def get_names():
    user_data = load_user_data()
    return list(user_data.keys())

@app.post("/register")
async def register(user: User):
    user_data = load_user_data()

    if user.username in user_data:
        return {"register": "failed - username already exists"}
    
    user_data[user.username] = {"username": user.username, "password": user.password}
    
    save_user_data(user_data)
    
    return {"register": "success"}

@app.post("/login")
async def login(user: User):
    user_data = load_user_data()
    
    if user.username not in user_data:
        return {"login": "username not found"}
    if user_data[user.username]["password"] == user.password:
        return {"login": "success"}
    else:
        return {"login": "failed"}

@app.put("/change_password")
async def change_password(user: User, new_password: str):
    user_data = load_user_data()
    
    if user.username not in user_data:
        return {"change_password": "username not found"}
    if user_data[user.username]["password"] == user.password:
        user_data[user.username]["password"] = new_password
        save_user_data(user_data)
        return {"change_password": "success"}
    else:
        return {"change_password": "failed"}

@app.post("/save_encoding")
async def save_face_encoding(username: str, password: str, file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        image = face_recognition.load_image_file(BytesIO(file_bytes))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {e}")

    encodings = face_recognition.face_encodings(image)

    if not encodings:
        raise HTTPException(status_code=400, detail="No faces found in the image.")

    # Load existing data from the JSON file
    user_data = load_user_data()

    # Check if the username exists and the password is correct
    if username not in user_data:
        raise HTTPException(status_code=400, detail=f"There is no user with the username {username}.")
    if user_data[username]["password"] != password:
        raise HTTPException(status_code=400, detail="Incorrect password.")

    # Update the dictionary with the new encoding
    user_data[username]["face_encoding"] = encodings[0].tolist()

    # Save the updated data to the JSON file
    save_user_data(user_data)

    return {"message": f"Encoding for {username} saved successfully."}

@app.post("/verify_existing_face")
async def verify_existing_face(username: str, file: UploadFile = File(...)):
    user_data = load_user_data()

    if username not in user_data:
        raise HTTPException(status_code=400, detail=f"There is no user with the username {username}.")

    try:
        file_bytes = await file.read()

        image = face_recognition.load_image_file(BytesIO(file_bytes))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing images: {e}")

    encodings1 = face_recognition.face_encodings(image)
    encodings2 = [np.array(user_data[username]["face_encoding"])]

    if not encodings1:
        raise HTTPException(status_code=400, detail="No faces found in the image.")

    # Compare the first face detected from each image
    match_result = face_recognition.compare_faces([encodings1[0]], encodings2[0], 0.4)

    distance = face_recognition.face_distance([encodings1[0]], encodings2[0])[0]
    confidence = face_distance_to_conf(distance)

    return {"match": bool(match_result[0]), "confidence": confidence}

@app.post("/verify_two_faces")
async def verify_two_faces(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    try:
        file1_bytes = await file1.read()
        file2_bytes = await file2.read()

        image1 = face_recognition.load_image_file(BytesIO(file1_bytes))
        image2 = face_recognition.load_image_file(BytesIO(file2_bytes))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing images: {e}")

    encodings1 = face_recognition.face_encodings(image1)
    encodings2 = face_recognition.face_encodings(image2)

    if not encodings1:
        raise HTTPException(status_code=400, detail="No faces found in the first image.")
    if not encodings2:
        raise HTTPException(status_code=400, detail="No faces found in the second image.")

    # Compare the first face detected from each image
    match_result = face_recognition.compare_faces([encodings1[0]], encodings2[0], 0.6)

    distance = face_recognition.face_distance([encodings1[0]], encodings2[0])[0]
    confidence = face_distance_to_conf(distance)

    return {"match": bool(match_result[0]), "confidence": confidence}