import cv2
import mediapipe as mp
import os
import pickle

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection

# Load or initialize dataset
faces_data = {}
faces_file = "faces_images.pkl"

if os.path.exists(faces_file):
    with open(faces_file, "rb") as f:
        try:
            faces_data = pickle.load(f)
        except EOFError:
            faces_data = {}

video = None  # Video capture object
user_name = ""
frame_count = 0
frame_skip = 3
count = 0

def start_capture(student_name):
    """ Start capturing face images """
    global user_name, count, video
    
    user_name = student_name
    
    if user_name not in faces_data:
        faces_data[user_name] = []  # Create entry for new student
    
    count = 0  # Reset image count
    
    if video is None or not video.isOpened():
        video = cv2.VideoCapture(0)
        video.set(3, 640)  # Width
        video.set(4, 480)  # Height

    return f"Face capture started for {user_name}"  # ✅ Ensure a valid return statement


def generate_frames():
    """ Stream webcam and capture faces every 3rd frame """
    global frame_count, count, video
    
    if video is None or not video.isOpened():
        return
    
    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.6) as face_detection:
        while count < 200:
            success, frame = video.read()
            if not success:
                break
            
            frame_count += 1
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_detection.process(rgb_frame)
            
            if results.detections:
                for detection in results.detections:
                    bboxC = detection.location_data.relative_bounding_box
                    frame_h, frame_w, _ = frame.shape

                    x = int(bboxC.xmin * frame_w)
                    y = int(bboxC.ymin * frame_h)
                    w = int(bboxC.width * frame_w)
                    h = int(bboxC.height * frame_h)

                    x, y = max(0, x), max(0, y)
                    w, h = min(frame_w - x, w), min(frame_h - y, h)

                    if w > 0 and h > 0:
                        face_image = frame[y:y + h, x:x + w]
                        
                        if frame_count % frame_skip == 0:
                            face_resized = cv2.resize(face_image, (100, 100))
                            faces_data[user_name].append(face_resized)
                            count += 1
                            print(f"Captured {count}/200 images for {user_name}")

                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
        video.release()
        print("Captured 200 images. Camera released.")
        save_faces()

def save_faces():
    """ Save collected faces """
    try:
        with open(faces_file, "wb") as f:
            pickle.dump(faces_data, f)
        print("Face images saved successfully.")
        return "Face data saved successfully."
    except Exception as e:
        print(f"Error saving face data: {e}")
        return "Error saving face data."
