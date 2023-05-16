import pytesseract
from PIL import Image


class IdentifyModule:

    def check_rollcall(self, imgPath, student_list):
        result = dict()

        # 指定剛剛下載tesseract.exe的完整路徑
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        image = Image.open(imgPath)
        # 這裡的lang就是剛剛下載的model
        text = pytesseract.image_to_string(image, lang='chi_tra')
        text = text.replace("\n", "").replace(" ", "")
        text = text.strip()
        print(text)

        # 辨識演算法
        return result


if __name__ == '__main__':
    # 指定剛剛下載tesseract.exe的完整路徑
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    image = Image.open('source/1-2.jpg')
    # 這裡的lang就是剛剛下載的model
    text = pytesseract.image_to_string(image, lang='chi_tra')
    text = text.replace("\n", "").replace(" ", "")
    text = text.strip()
    print(text)
