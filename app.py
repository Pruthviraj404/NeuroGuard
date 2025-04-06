import os
import cv2
import numpy as np
import pickle
import base64
from flask import Flask, request, jsonify, render_template, redirect, session, url_for, flash
from keras_facenet import FaceNet
from attendance import mark_attendance  # Ensure this file and function exists

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production

# Admin credentials (demo purpose only)
admin_credentials = {
    'xyz1': {'username': 'admin1', 'password': 'pass123'},
    'abc2': {'username': 'admin2', 'password': 'pass456'}
}

# Initialize FaceNet
embedder = FaceNet()

# ------------------ UTILITY FUNCTIONS ------------------ #

def load_embeddings(college_id=None):
    embeddings = {}
    base_dir = "data"

    if not os.path.exists(base_dir):
        return embeddings

    college_dirs = [college_id] if college_id else os.listdir(base_dir)

    for college_folder in college_dirs:
        college_path = os.path.join(base_dir, college_folder)
        if not os.path.isdir(college_path):
            continue

        for file in os.listdir(college_path):
            if file.endswith("_embeddings.pkl"):
                try:
                    with open(os.path.join(college_path, file), "rb") as f:
                        data = pickle.load(f)
                        username = data.get("username")
                        if username:
                            embeddings[username] = np.array(data["embeddings"])
                except Exception as e:
                    print(f"[ERROR] Loading {file}: {e}")
    return embeddings


def recognize_face(image, college_id):
    try:
        img_resized = cv2.resize(image, (160, 160))
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        embedding = embedder.embeddings(np.expand_dims(img_rgb, axis=0))[0]
        embedding = embedding / np.linalg.norm(embedding)

        best_match = None
        min_dist = float("inf")
        threshold = 0.7

        face_embeddings = load_embeddings(college_id)

        for username, stored_embeddings in face_embeddings.items():
            for stored_embedding in stored_embeddings:
                dist = np.linalg.norm(stored_embedding - embedding)
                if dist < min_dist:
                    min_dist = dist
                    best_match = username

        return best_match if min_dist < threshold else "Unknown"
    except Exception as e:
        print(f"[ERROR] Face recognition: {e}")
        return "Error"

# ------------------ ROUTES ------------------ #

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        college_id = request.form['college_id'].strip()
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        if college_id in admin_credentials:
            creds = admin_credentials[college_id]
            if creds['username'] == username and creds['password'] == password:
                session['college_id'] = college_id
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                flash("Incorrect username or password", "danger")
        else:
            flash("College ID not recognized", "danger")

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session['username'], college=session['college_id'])

@app.route('/faceregistration')
def face_register():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("face_register.html")

@app.route('/recognize')
def recognize():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("face_recognize.html")

@app.route('/save_face', methods=['POST'])
def save_face():
    try:
        data = request.get_json()
        college_id = data.get("college_id")
        username = data.get("username")
        image_data = data.get("image")

        if not college_id or not username or not image_data:
            return jsonify({"message": "College ID, username, and image are required"}), 400

        img_bytes = base64.b64decode(image_data.split(",")[1])
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({"message": "Invalid image data"}), 400

        img_resized = cv2.resize(img, (160, 160))
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)

        embedding = embedder.embeddings(np.expand_dims(img_rgb, axis=0))[0]
        embedding = embedding / np.linalg.norm(embedding)

        college_dir = os.path.join("data", college_id)
        os.makedirs(college_dir, exist_ok=True)
        pkl_file = os.path.join(college_dir, f"{username}_embeddings.pkl")

        if os.path.exists(pkl_file):
            with open(pkl_file, "rb") as f:
                existing_data = pickle.load(f)
        else:
            existing_data = {"college_id": college_id, "username": username, "embeddings": []}

        existing_data["embeddings"].append(embedding.tolist())

        with open(pkl_file, "wb") as f:
            pickle.dump(existing_data, f)

        return jsonify({"message": "Embedding saved"}), 200

    except Exception as e:
        print("[ERROR] Saving face:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/detect_face", methods=["POST"])
def detect_face():
    try:
        data = request.get_json()
        if "image" not in data or not data["image"]:
            return jsonify({"error": "No image provided"}), 400

        image_data = data["image"].split(",")[1]
        image_bytes = base64.b64decode(image_data)
        image_np = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        if image is None:
            return jsonify({"error": "Invalid image"}), 400

        college_id = session.get("college_id")
        if not college_id:
            return jsonify({"error": "Unauthorized"}), 403

        face_name = recognize_face(image, college_id)
        mark_attendance(face_name)  # You should define this in attendance.py

        return jsonify({"name": face_name})
    except Exception as e:
        print("[ERROR] Face detection:", e)
        return jsonify({"error": "Face recognition failed"}), 500

# ------------------ MAIN ------------------ #

if __name__ == '__main__':
    os.makedirs("data", exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=8080)
