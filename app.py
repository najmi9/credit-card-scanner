import os
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
        text += result[i][1] + ' '
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

    #ax = plt.subplots(nrows=1, figsize=(20, 20))
    #keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)

    #plt.show()

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
