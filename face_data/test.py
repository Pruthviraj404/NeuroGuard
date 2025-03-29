import os
import cv2
import numpy as np
import pickle
from keras_facenet import FaceNet

# Load the pre-trained FaceNet model
embedder = FaceNet()

# Directory for stored face data
storage_dir = "face_data"

def load_all_embeddings():
    """
    Load all embeddings and their corresponding usernames from the directory.
    Returns a dictionary with usernames as keys and embeddings as values.
    """
    user_embeddings = {}

    for file in os.listdir(storage_dir):
        if file.endswith("_embeddings.pkl"):
            user_file = os.path.join(storage_dir, file)
            with open(user_file, "rb") as f:
                data = pickle.load(f)
                user_embeddings[data["username"]] = data["embeddings"]

    return user_embeddings

def calculate_similarity(vec1, vec2):
    """
    Calculate cosine similarity between two vectors.
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def predict_name(live_embedding, user_embeddings):
    """
    Predict the username by comparing the live embedding to all stored embeddings.
    """
    best_match = None
    best_similarity = 0
    match_threshold = 0.9  # Adjust the threshold as needed

    for username, embeddings in user_embeddings.items():
        for stored_embedding in embeddings:
            similarity = calculate_similarity(live_embedding, stored_embedding)
            if similarity > best_similarity and similarity > match_threshold:
                best_similarity = similarity
                best_match = username

    return best_match

def main():
    """
    Real-time face prediction using webcam feed.
    """
    print("Loading all stored embeddings...")
    user_embeddings = load_all_embeddings()

    if not user_embeddings:
        print("No stored embeddings found. Please register users first.")
        return

    print("Accessing webcam...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to access webcam.")
        return

    print("Press 'q' to exit the live feed.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Pre-process frame for embedding extraction
        face_resized = cv2.resize(frame, (160, 160))
        face_rgb = cv2.cvtColor(face_resized, cv2.COLOR_BGR2RGB)

        # Extract live embedding
        live_embedding = embedder.embeddings(np.expand_dims(face_rgb, axis=0))[0]

        # Predict name
        predicted_name = predict_name(live_embedding, user_embeddings)
        status = predicted_name if predicted_name else "UNKNOWN"

        # Display prediction on the live feed
        cv2.putText(frame, f"Name: {status}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if predicted_name else (0, 0, 255), 2)
        cv2.imshow("Live Face Prediction", frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
