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

@app.route('/')
def index():
    """ Render HTML page """
    return render_template('face_register.html')

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
