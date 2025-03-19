import os
import base64
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Create 'img' folder if it doesn't exist
IMG_FOLDER = "img"
os.makedirs(IMG_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

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
