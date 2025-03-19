from flask import Flask, render_template
from flask_socketio import SocketIO
import cv2
import base64
import numpy as np
import eventlet  # Required for async support

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@socketio.on('video_frame')
def handle_frame(data):
    """Receive, process, and send frame back."""
    try:
        if not data:
            print("[ERROR] Received empty frame data")
            return

        # Decode Base64 frame
        frame_data = base64.b64decode(data)
        npimg = np.frombuffer(frame_data, dtype=np.uint8)
        frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        if frame is None:
            print("[ERROR] Decoded frame is None")
            return

        # Resize to reduce processing time
        frame = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_AREA)

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        # Encode frame back to JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        encoded_frame = base64.b64encode(buffer).decode('utf-8')

        print("[INFO] Sending processed frame")  # Debugging message
        socketio.emit('processed_frame', encoded_frame)  # ❌ Removed `broadcast=True`

    except Exception as e:
        print(f"[ERROR] Exception occurred: {e}")

if __name__ == '__main__':
    print("Starting Flask-SocketIO server on http://localhost:8080")
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
