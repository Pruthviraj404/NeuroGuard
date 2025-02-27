import cv2
import mediapipe as mp
import os


mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
import numpy as np
video = cv2.VideoCapture(0)

def sharpen_image(image, strength=1.0):
    kernel = np.array([[0, -1, 0],
                       [-1,  5 + strength, -1],
                       [0, -1, 0]]) / (1 + strength)  # Normalize to prevent excessive sharpening
    sharp_image = cv2.filter2D(image, -1, kernel)
    return sharp_image

with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
    while True:
        ret, frame = video.read()
        if not ret:
            break

        frame = sharpen_image(frame,strength=0.5)
        frame=cv2.resize(frame,(1080,720))

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(rgb_frame)

        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                h, w, _ = frame.shape
                x, y, w, h = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

        cv2.imshow("Face Detection", frame)
     

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

video.release()
cv2.destroyAllWindows()
 