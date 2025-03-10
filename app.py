from flask import Flask, render_template, Response, request, jsonify
from face_recognize import generate_frames, save_faces, start_capture

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    """ Render HTML page """
    return render_template('face_register.html')

@app.route('/video_feed')
def video_feed():
    """ Stream video frames """
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_capture', methods=['POST'])
def start_capture_route():
    """ Start capturing faces """
    student_name = request.form.get('student_name')  # Get name from form
    if not student_name:
        return jsonify({'error': 'No student name provided'}), 400  # Return an error if empty

    response = start_capture(student_name)  # Call function from face_recognize.py

    if response is None:
        return jsonify({'error': 'Failed to start capture'}), 500  # Handle unexpected errors

    return jsonify({'message': response})  # Return success response


@app.route('/save_faces')
def save_faces_route():
    """ Save captured face images """
    return save_faces()

if __name__ == '__main__':
    app.run(debug=True)
