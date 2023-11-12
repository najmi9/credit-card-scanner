import os
import uuid
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from PIL import Image
import pytesseract
import matplotlib.pyplot as plt
import keras_ocr
import easyocr

def easyocr_read(file_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(file_path)
    text = ''
    for i in range(len(result)):
        text += result[i][1]
    return text

def keras_read(file_path):
    image = keras_ocr.tools.read(file_path)
    pipeline = keras_ocr.pipeline.Pipeline()
    images = [image]
    prediction_groups = pipeline.recognize(images)


    recognized_text = [text for _, text in prediction_groups[0]]

    """ fig, axs = plt.subplots(nrows=len(images), figsize=(20, 20))
    for ax, image, predictions in zip(axs, images, prediction_groups):
        keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)

    plt.show() """

    return recognized_text

def tesseract_read(file_path):
    image = Image.open(file_path)
    text = pytesseract.image_to_string(
        image,
        lang='eng'
    )

    return text

app = Flask(__name__)
CORS(app)

# Define the path to the static files directory
static_files_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')

@app.route('/', methods=['GET'])
def index():
    return send_from_directory(static_files_dir, 'index.html')

@app.route('/api/upload', methods=['POST'])
def upload():
    file = request.files['file']
    random_file_name = str(uuid.uuid4())
    file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'uploads',
        random_file_name + file.filename + '.png'
    )
    file.save(file_path)

    tesseract_txt = tesseract_read(file_path)
    keras_txt = keras_read(file_path)
    easyocr_txt = easyocr_read(file_path)

    return {
        'tesseract_txt': tesseract_txt,
        'keras_txt': keras_txt,
        'easyocr_txt': easyocr_txt
    }, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
