from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import os
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
SWAP_FOLDER = 'static/swapped'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SWAP_FOLDER'] = SWAP_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(SWAP_FOLDER):
    os.makedirs(SWAP_FOLDER)

def face_swap(img1, img2):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    faces1 = face_cascade.detectMultiScale(cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY), 1.3, 5)
    faces2 = face_cascade.detectMultiScale(cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY), 1.3, 5)

    if len(faces1) != 1 or len(faces2) != 1:
        print("Error: Could not detect exactly one face in each image.")
        return None, None

    x1, y1, w1, h1 = faces1[0]
    face1 = img1[y1:y1+h1, x1:x1+w1]

    x2, y2, w2, h2 = faces2[0]
    face2 = img2[y2:y2+h2, x2:x2+w2]

    roi1_eyes = face1[int(h1/5):int(h1*2/5), int(w1/6):int(w1*5/6)]
    roi2_eyes = face2[int(h2/5):int(h2*2/5), int(w2/6):int(w2*5/6)]

    roi1_nose = face1[int(h1*2/5):int(h1*3/5), int(w1/4):int(w1*3/4)]
    roi2_nose = face2[int(h2*2/5):int(h2*3/5), int(w2/4):int(w2*3/4)]

    roi1_mouth = face1[int(h1*3/5):int(h1*4/5), int(w1/6):int(w1*5/6)]
    roi2_mouth = face2[int(h2*3/5):int(h2*4/5), int(w2/6):int(w2*5/6)]

    roi1_eyes_resized = cv2.resize(roi1_eyes, (roi2_eyes.shape[1], roi2_eyes.shape[0]))
    roi2_eyes_resized = cv2.resize(roi2_eyes, (roi1_eyes.shape[1], roi1_eyes.shape[0]))

    roi1_nose_resized = cv2.resize(roi1_nose, (roi2_nose.shape[1], roi2_nose.shape[0]))
    roi2_nose_resized = cv2.resize(roi2_nose, (roi1_nose.shape[1], roi1_nose.shape[0]))

    roi1_mouth_resized = cv2.resize(roi1_mouth, (roi2_mouth.shape[1], roi2_mouth.shape[0]))
    roi2_mouth_resized = cv2.resize(roi2_mouth, (roi1_mouth.shape[1], roi1_mouth.shape[0]))

    face1_swapped = face1.copy()
    face1_swapped[int(h1/5):int(h1*2/5), int(w1/6):int(w1*5/6)] = roi2_eyes_resized
    face1_swapped[int(h1*2/5):int(h1*3/5), int(w1/4):int(w1*3/4)] = roi2_nose_resized
    face1_swapped[int(h1*3/5):int(h1*4/5), int(w1/6):int(w1*5/6)] = roi2_mouth_resized

    face2_swapped = face2.copy()
    face2_swapped[int(h2/5):int(h2*2/5), int(w2/6):int(w2*5/6)] = roi1_eyes_resized
    face2_swapped[int(h2*2/5):int(h2*3/5), int(w2/4):int(w2*3/4)] = roi1_nose_resized
    face2_swapped[int(h2*3/5):int(h2*4/5), int(w2/6):int(w2*5/6)] = roi1_mouth_resized

    img1_swapped = img1.copy()
    img1_swapped[y1:y1+h1, x1:x1+w1] = face1_swapped
    img2_swapped = img2.copy()
    img2_swapped[y2:y2+h2, x2:x2+w2] = face2_swapped

    return img1_swapped, img2_swapped

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('images')
    if len(files) != 2:
        return jsonify({'error': 'Exactly two images required.'}), 400

    img_paths = []
    for i, file in enumerate(files):
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], f'image{i + 1}.jpg')
        file.save(img_path)
        img_paths.append(img_path)

    img1 = cv2.imread(img_paths[0])
    img2 = cv2.imread(img_paths[1])
    img1_swapped, img2_swapped = face_swap(img1, img2)

    cv2.imwrite(os.path.join(app.config['SWAP_FOLDER'], 'swapped1.jpg'), img1_swapped)
    cv2.imwrite(os.path.join(app.config['SWAP_FOLDER'], 'swapped2.jpg'), img2_swapped)

    return jsonify({
        'swapped1_url': f'swapped/swapped1.jpg',
        'swapped2_url': f'swapped/swapped2.jpg'
    })

@app.route('/swapped/<filename>')
def send_swapped_image(filename):
    return send_from_directory(app.config['SWAP_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
