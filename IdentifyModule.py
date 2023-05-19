import json
import os
from google.cloud import vision


# 設定 Google API 憑證環境變數
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'source/seating-chart-checker-2389976159cf.json'


def detect_text(imgPath):
    client = vision.ImageAnnotatorClient()

    with open(imgPath, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    print('Texts:')
    for text in texts:
        print('\n"{}"'.format(text.description))


def check_rollcall(imgPath, student_list):
    result = dict()

    # 影像前處理

    detect_text(imgPath)

    # 辨識演算法

    return result


if __name__ == '__main__':
    detect_text('source/sheet_samples/1.jpg')

# if __name__ == '__main__':
#     # 指定剛剛下載tesseract.exe的完整路徑
#     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#     image = Image.open('source/1-2.jpg')
#     # 這裡的lang就是剛剛下載的model
#     text = pytesseract.image_to_string(image, lang='chi_tra')
#     text = text.replace("\n", "").replace(" ", "")
#     text = text.strip()
#     print(text)
