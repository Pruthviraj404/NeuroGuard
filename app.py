import os
import cv2
import numpy as np
import pickle
import base64
from flask import Flask, request, jsonify, render_template
from keras_facenet import FaceNet  # Pre-trained FaceNet model

app = Flask(__name__)

# Directory for storing face data
STORAGE_DIR = "face_data"
os.makedirs(STORAGE_DIR, exist_ok=True)

# Initialize FaceNet model
embedder = FaceNet()

# Load stored face embeddings
def load_embeddings():
    embeddings = {}
    for file in os.listdir(STORAGE_DIR):
        if file.endswith("_embeddings.pkl"):
            try:
                with open(os.path.join(STORAGE_DIR, file), "rb") as f:
                    data = pickle.load(f)
                    embeddings[data["username"]] = np.array(data["embeddings"])
            except Exception as e:
                print(f"Error loading {file}: {e}")
    return embeddings

face_embeddings = load_embeddings()

def recognize_face(image):
    """Recognizes a face in the given image."""
    try:
        img_resized = cv2.resize(image, (160, 160))
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)

        # Normalize embeddings
        embedding = embedder.embeddings(np.expand_dims(img_rgb, axis=0))[0]
        embedding = embedding / np.linalg.norm(embedding)  # Normalize

        best_match = None
        min_dist = float("inf")
        threshold = 0.7  # Lowered threshold for better accuracy

        for username, stored_embeddings in face_embeddings.items():
            for stored_embedding in stored_embeddings:
                dist = np.linalg.norm(stored_embedding - embedding)
                if dist < min_dist:
                    min_dist = dist
                    best_match = username

        return best_match if min_dist < threshold else "Unknown"
    except Exception as e:
        print(f"Face recognition error: {str(e)}")
        return "Error"

@app.route('/')
def login():
    return render_template("face_recognize.html")

@app.route('/faceregistration')
def face_register():
    return render_template("face_register.html")

@app.route('/dashboard')
def home():
    return render_template('dashboard.html')

@app.route('/save_images', methods=['POST'])
def save_images():
    """Saves face embeddings from uploaded images."""
    try:
        data = request.get_json()
        if not data or "username" not in data or "images" not in data:
            return jsonify({"message": "Invalid data format"}), 400

        username = data["username"].strip()
        images = data["images"]

        if not username or not isinstance(images, list) or len(images) == 0:
            return jsonify({"message": "Username and images are required"}), 400

        user_file = os.path.join(STORAGE_DIR, f"{username}_embeddings.pkl")
        embeddings_data = {"username": username, "embeddings": []}

        valid_images = 0
        for img_data in images:
            try:
                img_bytes = base64.b64decode(img_data.split(',')[1])
                nparr = np.frombuffer(img_bytes, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                if img is None:
                    print("Warning: Skipping invalid image")
                    continue  # Skip invalid images

                img_resized = cv2.resize(img, (160, 160))
                img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)

                embedding = embedder.embeddings(np.expand_dims(img_rgb, axis=0))[0]
                embedding = embedding / np.linalg.norm(embedding)  # Normalize

                embeddings_data["embeddings"].append(embedding.tolist())
                valid_images += 1
            except Exception as e:
                print(f"Error processing image: {str(e)}")

        if valid_images == 0:
            return jsonify({"message": "No valid images processed"}), 400

        with open(user_file, "wb") as f:
            pickle.dump(embeddings_data, f)

        global face_embeddings
        face_embeddings = load_embeddings()

        return jsonify({"message": "Embeddings saved successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/detect_face", methods=["POST"])
def detect_face():
    """Detects and recognizes a face from an uploaded image."""
    try:
        data = request.get_json()
        if "image" not in data or not data["image"]:
            return jsonify({"error": "No image provided"}), 400

        # Decode base64 image
        image_data = data["image"].split(",")[1]  # Remove "data:image/jpeg;base64,"
        image_bytes = base64.b64decode(image_data)
        image_np = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        if image is None:
            return jsonify({"error": "Invalid image"}), 400

        # Perform face recognition
        face_name = recognize_face(image)

        return jsonify({"name": face_name})
    except Exception as e:
        print("Error processing image:", e)
        return jsonify({"error": "Face recognition failed"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
