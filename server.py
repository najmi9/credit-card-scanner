import os
import uuid
from flask import Flask, request, send_from_directory
from flask_cors import CORS
import easyocr
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)

static_files_dir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'static'
)

@app.route('/', methods=['GET'])
def index():
    return send_from_directory(
        static_files_dir,
        'index.html'
    )

@app.route('/api/upload', methods=['POST'])
def upload():
    file = request.files['file']
    random_file_name = str(uuid.uuid4())
    file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'uploads',
        f"{random_file_name}-{file.filename}.png",
    )
    file.save(file_path)

    output_file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'static',
        'results',
        f"{random_file_name}-{file.filename}_result.png",
    )

    credit_card_data = extract_credit_card_data(
        file_path,
        output_file_path
    )

    validate_credit_card_data(credit_card_data)

    root_dir = os.path.dirname(os.path.realpath(__file__))
    output_file_path = output_file_path.replace(root_dir, '')
    current_url = request.url_root
    output_file_path = current_url + output_file_path

    return {
        'output_file': output_file_path,
        'credit_card': credit_card_data,
    }, 200

def extract_credit_card_data(input_path: str, output_path: str):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(input_path)
    image = cv2.imread(input_path)

    response = {}
    for i in range(len(result)):
        points = np.array(result[i][0], dtype=np.int32)
        points = points.reshape((-1, 1, 2))
        cv2.polylines(image, [points], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.putText(image, result[i][1], (points[0][0][0], points[0][0][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        if i == 6:
            response['number'] = result[i][1]

        if i == 8:
            response['holder_name'] = result[i][1].upper()

        if i == 10:
            expiry_date = result[i][1].replace('FIN', '').replace(',', '')
            expiry_date = expiry_date.replace(':', '')
            response['expiry_date'] = expiry_date

        if i == 12:
            response['cvv'] = result[i][1]

    cv2.imwrite(output_path, image)

    return response

def validate_credit_card_data(data: dict):
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
