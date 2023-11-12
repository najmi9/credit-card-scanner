import os
from PIL import Image
import pytesseract
import matplotlib.pyplot as plt
import keras_ocr
import easyocr
import cv2
import numpy as np

def easyocr_read(file_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(file_path)
    text = ''

    image = cv2.imread(file_path)

    for i in range(len(result)):
        points = np.array(result[i][0], dtype=np.int32)
        points = points.reshape((-1, 1, 2))
        cv2.polylines(image, [points], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.putText(image, result[i][1], (points[0][0][0], points[0][0][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        text += result[i][1] + ' '

    output_file_path = 'easyocr_result.png'
    cv2.imwrite(output_file_path, image)

    return text

def keras_read(file_path):
    image = keras_ocr.tools.read(file_path)
    pipeline = keras_ocr.pipeline.Pipeline()
    images = [image]
    prediction_groups = pipeline.recognize(images)
    predictions = prediction_groups[0]

    text = ''
    for i in range(len(predictions)):
        word, bbox = predictions[i]
        text += word + ' '

    fig, ax = plt.subplots(nrows=1, figsize=(20, 20))
    keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)

    output_file_path = 'keras_ocr_result.png'
    plt.savefig(output_file_path)

    plt.close()

    return text

def tesseract_read(file_path):
    image = Image.open(file_path)
    text = pytesseract.image_to_string(
        image,
        lang='eng'
    )

    return text

def main():

    file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'uploads',
        '40ca3478-2a5c-413a-af41-e8c5d221b080blob.png'
    )

    result = {
        'tesseract_txt': tesseract_read(file_path),
        'keras_txt': keras_read(file_path),
        'easyocr_txt': easyocr_read(file_path)
    }

    print(result)

    return result

if __name__ == '__main__':
    main()
