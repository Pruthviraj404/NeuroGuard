from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import face_recognize

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('face_register.html')

@app.route('/video_feed')
def video_feed():
    return Response(face_recognize.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('start_capture')
def handle_start_capture(data):
    student_name = data.get('name', 'Unknown')
    response = face_recognize.start_capture(student_name)
    socketio.emit('capture_status', response)

@socketio.on('save_faces')
def handle_save_faces():
    response = face_recognize.save_faces()
    socketio.emit('save_status', response)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)

