<<<<<<< HEAD
import os
import base64
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Create 'img' folder if it doesn't exist
IMG_FOLDER = "img"
os.makedirs(IMG_FOLDER, exist_ok=True)
=======
from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
import os

app = Flask(__name__)

# Directory to save captured faces
SAVE_DIR = "captured_faces"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)
>>>>>>> restore-branch

@app.route('/')
def index():
    return render_template('index.html')

<<<<<<< HEAD
@app.route('/save_image', methods=['POST'])
def save_image():
    data = request.json
    images = data.get('images', [])

    if len(images) != 3:
        return jsonify({"error": "Please capture 3 images"}), 400

    saved_images = []
    for i, img_data in enumerate(images):
        img_bytes = base64.b64decode(img_data.split(",")[1])  # Convert base64 to bytes
        filename = f"{IMG_FOLDER}/image_{i+1}.jpg"
        
        with open(filename, "wb") as f:
            f.write(img_bytes)
        
        saved_images.append(filename)

    return jsonify({"message": "Images saved successfully", "files": saved_images})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
=======
@app.route('/capture_face', methods=['POST'])
def capture_face():
    """ Capture face from user webcam feed """
    data = request.json
    student_name = data.get('student_name')
    frame_data = data.get('frame')

    if not student_name or not frame_data:
        return jsonify({'error': 'Missing data'}), 400

    try:
        # Decode base64 frame
        frame_bytes = base64.b64decode(frame_data.split(',')[1])
        np_img = np.frombuffer(frame_bytes, dtype=np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        # Save the image
        filename = os.path.join(SAVE_DIR, f"{student_name}.jpg")
        cv2.imwrite(filename, img)

        return jsonify({'message': 'Face captured successfully!', 'filename': filename})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
>>>>>>> restore-branch
