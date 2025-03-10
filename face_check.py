from fastapi import FastAPI, File, UploadFile, HTTPException
import face_recognition
import uvicorn
from io import BytesIO

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Thís is DucTai"}

@app.post("/verify")
async def verify_face(file1: UploadFile = File(...), file2: UploadFile = File(...)):
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
    match_result = face_recognition.compare_faces([encodings1[0]], encodings2[0])
    
    def face_distance_to_conf(face_distance, face_match_threshold=0.6):
        if face_distance > face_match_threshold:
            range_val = (1.0 - face_match_threshold)
            linear_val = (1.0 - face_distance) / (range_val * 2.0)
            return linear_val
        else:
            range_val = face_match_threshold
            linear_val = 1.0 - (face_distance / (range_val * 2.0))
            return linear_val + ((1.0 - linear_val) * ((linear_val - 0.5) * 2))

    distance = face_recognition.face_distance([encodings1[0]], encodings2[0])[0]
    confidence = face_distance_to_conf(distance)

    return {"match": bool(match_result[0]), "confidence": confidence}