import cv2
import mediapipe as mp
import pickle
import numpy as np
from skimage.metrics import structural_similarity as ssim

# Load stored face data
faces_file = "faces_images.pkl"
try:
    with open(faces_file, 'rb') as f:
        faces_data = pickle.load(f)
except (FileNotFoundError, EOFError):
    print("Error: No stored face data found.")
    faces_data = {}

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection

# Open webcam
video = cv2.VideoCapture(0)
if not video.isOpened():
    print("Error: Could not access webcam.")
    exit()

def preprocess_face(face_image):
    """ Resize and normalize face image """
    face_resized = cv2.resize(face_image, (100, 100))  # Resize to match stored data
    face_gray = cv2.cvtColor(face_resized, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    return face_gray

def compare_faces(test_face):
    """ Compare test face with stored faces using SSIM similarity """
    best_match = None
    highest_similarity = 0.0  # SSIM ranges from -1 to 1

    for user, stored_faces in faces_data.items():
        for stored_face in stored_faces:
            stored_gray = cv2.cvtColor(stored_face, cv2.COLOR_BGR2GRAY)  # Convert stored image to grayscale
            similarity = ssim(test_face, stored_gray)  # Compute SSIM similarity

            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = user  # Update best match

    return best_match if highest_similarity > 0.6 else "Unknown"  # Threshold (0.6) for recognition
with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.9) as face_detection:

# with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:

    while True:
        ret, frame = video.read()
        if not ret:
            break

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

                # Ensure bounding box is within frame bounds
                x, y = max(0, x), max(0, y)
                w, h = min(frame_w - x, w), min(frame_h - y, h)

                if w > 0 and h > 0:
                    face_image = frame[y:y + h, x:x + w]  # Extract face ROI

                    if face_image.size > 0:
                        test_face = preprocess_face(face_image)  # Preprocess the face
                        detected_name = compare_faces(test_face)  # Compare with stored faces

                        # Draw bounding box
                        color = (0, 255, 0) if detected_name != "Unknown" else (0, 0, 255)  # Green for match, Red for unknown
                        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

                        # Display the detected name
                        cv2.putText(frame, detected_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        # Show the frame
        cv2.imshow("Face Recognition", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release resources
video.release()
cv2.destroyAllWindows()
