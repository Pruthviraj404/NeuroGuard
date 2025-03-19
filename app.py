from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable WebSocket communication

@app.route('/')
def index():
    return render_template('index.html')  # Load HTML page

@socketio.on('offer')
def handle_offer(data):
    emit('offer', data, broadcast=True)  # Send offer to the other peer

@socketio.on('answer')
def handle_answer(data):
    emit('answer', data, broadcast=True)  # Send answer to the other peer

@socketio.on('candidate')
def handle_candidate(data):
    emit('candidate', data, broadcast=True)  # Send ICE candidate

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
