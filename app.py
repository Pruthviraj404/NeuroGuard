from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import cv2
import base64
import numpy as np

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@socketio.on('video_frame')
def handle_frame(data):
    """Receive frame from client and process it."""
    frame_data = base64.b64decode(data)
    npimg = np.frombuffer(frame_data, dtype=np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Optimize by resizing the frame to reduce data size
    frame = cv2.resize(frame, (320, 240))

    # Convert to grayscale (example processing)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    # Convert back to JPEG and send to client
    _, buffer = cv2.imencode('.jpg', frame)
    encoded_frame = base64.b64encode(buffer).decode('utf-8')
    socketio.emit('processed_frame', encoded_frame)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
