import json
import os
from google.cloud import vision


# 設定 Google API 憑證環境變數
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'resource/seating-chart-checker-2389976159cf.json'


def detect_text(imgPath: str):
    """
    Use Google cloud vision API to detect text.

    return: a list of detected words
    """

    client = vision.ImageAnnotatorClient()

    with open(imgPath, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    # print('Texts:')
    # for text in texts:
    #     print('\n"{}"'.format(text.description))
    return texts[0].description.split('\n')


def check_rollcall(imgPath: str, student_list: list):
    """
    Detect text on the image, and match to the student list, and return the attendance status.

    student_list: a list of all student names, currently haven't considered non-three-word names yet
    return: a dict, key for all students in student_list, value for their attendance status (0:缺席 1:出席)
    """

    # --- 影像前處理 ---

    # --- 辨識文字 ---

    # word_list = detect_text(imgPath)
    word_list = ['日期:QCT/5', '俞浩君', '某洢岑', '張文虹', '范文瑄', 'FIL', 'TTF', '講臺', '陳長', '戴柏儀', '劉明融', '姜紹淳',
                 'TOO', '技政偉孔繁道張慈芸大型陳慧慧', '劉品萱', '周远', '省達', '强思淇', '陈宇軒', '关系数', '天家', '陳芃铵',
                 '黄雅欣', '駱宥亘|郭家佑']  # detect_text('resource/sheet_samples/1.jpg') 出來的結果
    print('detected words\t:', word_list)

    # --- 配對演算法 ---

    unmatched_students = set(student_list)
    unmatched_words = set(word_list)

    # # --- 完全相等的 先配對 ---
    target = unmatched_students
    to_add, to_remove = [], []
    for word in unmatched_words:
        if len(word) < 3:
            continue
        c = 0
        while c < len(word)-2:
            if word[c:c+3] in target:
                unmatched_students.remove(word[c:c+3])
                to_remove.append(word)
                # 若此為長字串，就以該三字做分割，切出兩個字串，空字串就不用切出來了
                if c != 0:
                    to_add.append(word[:c])
                if c+3 != len(word):
                    to_add.append(word[c+3:])
                c += 3
            else:
                c += 1
    for ele in to_add:
        unmatched_words.add(ele)
    for ele in to_remove:
        unmatched_words.remove(ele)
    # print('unmatched words\t:', unmatched_words)

    # # --- 兩個字相同且其相對位置相同的 再配對 ---
    target = dict()
    to_remove = []
    for name in unmatched_students:
        for mask in [name[0:2] + '.', name[0] + '.' + name[2], '.' + name[1:3]]:
            if mask in target:
                to_remove.append(mask)     # 可能第三個人名字有兩字相同的，所以不能直接刪除
            else:
                target[mask] = name
    for ele in to_remove:
        target.remove(ele)
    # print(target)
    to_add, to_remove = [], []
    for word in unmatched_words:
        if len(word) == 1:
            continue
        if len(word) == 2:
            for mask in [word + '.', '.' + word]:
                if mask in target:
                    unmatched_students.remove(target[mask])
                    to_remove.append(word)
                    break
            continue
        c = 0
        while c < len(word) - 2:
            for i, mask in enumerate([word[c:c+2] + '.', word[c] + '.' + word[c+2], '.' + word[c+1:c+3]]):
                if mask in target:
                    unmatched_students.remove(target[mask])
                    to_remove.append(word)
                    # 如果 '.' 不是夾在中間，就只要以兩字做分割，否則一樣三字
                    # 但若 '.' 的那側只剩它一個字了，代表那個字大概只是辨識錯字，就不用切出來了
                    if c != 0:
                        to_add.append(word[:c+1 if i == 2 else c])
                    if c + 3 != len(word):
                        to_add.append(word[c+2 if i == 0 else c+3:])
                    c += 2 if (i == 0 and c + 3 != len(word)) else 3
                    break
            else:
                c += 1
    for ele in to_add:
        unmatched_words.add(ele)
    for ele in to_remove:
        unmatched_words.remove(ele)
    print('unmatched words\t:', unmatched_words)

    # # --- 配對剩餘的 最好標示給使用者檢查 ---

    # # --- 將沒配對上的框起來 ---

    # --- 回傳出勤記錄 ---
    attendance = dict()
    for student in student_list:
        attendance[student] = 0 if student in unmatched_students else 1

    return attendance


if __name__ == '__main__':
    student_list = ['俞浩君', '葉洢岑', '劉昀融', '張慈芸', '周子丞']
    attendance_record = check_rollcall('resource/sheet_samples/1.jpg', student_list)
    print('出席紀錄\t\t\t:', attendance_record)


# if __name__ == '__main__':
#     # 指定剛剛下載tesseract.exe的完整路徑
#     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#     image = Image.open('source/1-2.jpg')
#     # 這裡的lang就是剛剛下載的model
#     text = pytesseract.image_to_string(image, lang='chi_tra')
#     text = text.replace("\n", "").replace(" ", "")
#     text = text.strip()
#     print(text)
