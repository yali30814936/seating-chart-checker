import json
import os
from google.cloud import vision


# 設定 Google API 憑證環境變數
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'resource/seating-chart-checker-2389976159cf.json'


def detect_text(imgPath: str) -> list:
    """
    Use Google cloud vision API to detect text.
    return a list of detected words.
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


def check_rollcall(imgPath: str, student_list: list) -> dict[str, int]:
    """
    Detect text on the image, and match to the student list, and return the attendance status.

    Args:
        imgPath (str): the image path to detect.
        student_list (list): a list of all student names, currently haven't considered non-three-word names yet.
    Returns:
        dict[str, int]: attendance status.
            str: all students in student_list.
            int: their attendance status. (0:缺席 1:出席)
    """

    # --- 影像前處理 ---

    # --- 辨識文字 ---

    word_list = detect_text(imgPath)
    # word_list = ['日期:QCT/5', '俞浩君', '某洢岑', '張文虹', '范文瑄', 'FIL', 'TTF', '講臺', '陳長', '戴柏儀', '劉明融', '姜紹淳',
    #              'TOO', '技政偉孔繁道張慈芸大型陳慧慧', '劉品萱', '周远', '省達', '强思淇', '陈宇軒', '关系数', '天家', '陳芃铵',
    #              '黄雅欣', '駱宥亘|郭家佑']  # detect_text('resource/sheet_samples/1.jpg') 出來的結果
    print('detected words\t:', word_list)

    # --- 配對演算法 ---

    unmatched_words = set(word_list)
    unmatched_students = set(student_list)
    # 防呆有學生完全同名
    repeated_students = set()
    if len(unmatched_students) != len(student_list):
        for stud in unmatched_students:
            if student_list.count(stud) > 1:
                repeated_students.add(stud)
    for stud in repeated_students:
        unmatched_students.remove(stud)

    # # --- 完全相等的 先配對 ---
    target = unmatched_students
    to_add, to_remove = set(), set()
    for word in unmatched_words:
        if len(word) < 3:
            continue
        c = 0
        while c < len(word)-2:
            if word[c:c+3] in target:
                try:
                    unmatched_students.remove(word[c:c+3])
                except KeyError:
                    print('文字重複辨識，或兩人名字不相同辨識成完全相同，導致重複 remove / 學生名字:', target[word[c:c+3]])
                to_remove.add(word)
                # 若此為長字串，就以該三字做分割，切出兩個字串，空字串就不用切出來了
                if c != 0:
                    to_add.add(word[:c])
                if c+3 != len(word):
                    to_add.add(word[c+3:])
                c += 3
            else:
                c += 1
    for ele in to_add:
        unmatched_words.add(ele)
    for ele in to_remove:
        unmatched_words.remove(ele)
    print('unmatched words\t:', unmatched_words)

    # # --- 兩個字相同且其相對位置相同的 再配對 ---
    target = dict()
    to_remove = set()
    for name in unmatched_students:
        for mask in [name[0:2] + '.', name[0] + '.' + name[2], '.' + name[1:3]]:
            # 若有兩人名字中有兩字相同且位置相同，做 mask 就會重複，故不能放進 target
            if mask in target:
                to_remove.add(mask)     # 可能第三個人名字有兩字相同的，所以不能直接刪除
            else:
                target[mask] = name
    for ele in to_remove:
        del target[ele]
    # print(target)
    to_add, to_remove = set(), set()
    for word in unmatched_words:
        if len(word) == 1:
            continue
        if len(word) == 2:
            for mask in [word + '.', '.' + word]:
                if mask in target:
                    try:
                        unmatched_students.remove(target[mask])
                    except KeyError:
                        print('文字重複辨識，或兩人名字兩字不相同辨識成相同，導致重複 remove / 學生名字:', target[mask], '/ mask:', mask)
                    to_remove.add(word)
                    break
            continue
        c = 0
        while c < len(word) - 2:
            for i, mask in enumerate([word[c:c+2] + '.', word[c] + '.' + word[c+2], '.' + word[c+1:c+3]]):
                if mask in target:
                    try:
                        unmatched_students.remove(target[mask])
                    except KeyError:
                        print('文字重複辨識，或兩人名字兩字不相同辨識成相同，導致重複 remove / 學生名字:', target[mask], '/ mask:', mask)
                    to_remove.add(word)
                    # 如果 '.' 不是夾在中間，就只要以兩字做分割，否則一樣三字
                    # 但若 '.' 的那側只剩它一個字了，代表那個字大概只是辨識錯字，就不用切出來了
                    if c != 0:
                        to_add.add(word[:c+1 if i == 2 else c])
                    if c + 3 != len(word):
                        to_add.add(word[c+2 if i == 0 else c+3:])
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

    for student in repeated_students:
        attendance[student] = 0     # 給老師人工補點名

    return attendance


if __name__ == '__main__':
    # student_list = ['俞浩君', '葉洢岑', '劉昀融', '張慈芸', '周子丞']
    student_list = ['俞浩君', '廖令弘', '曾昱翔', '林政偉', '周子娟', '黃雅欣', '郭家佑', '駱宥亘', '周暐翔', '劉昀融', '姜紹淳',
                    '陳晏慈', '葉洢岑', '羅苡心', '黃偉綸', '陳慧雲', '陳芃銨', '劉凱菁', '張慈芸', '孔繁瑄', '周子丞', '王大埊',
                    '陳振榕', '蔡宇軒', '戴柏儀']

    # attendance_record = check_rollcall('resource/sheet_samples/1.jpg', student_list)
    # print('出席紀錄\t\t\t:', attendance_record)

    total = 0
    for i in range(1, 13):
        print('\n[test '+str(i)+'.jpg]')

        attendance_record = check_rollcall('resource/sheet_samples/'+str(i)+'.jpg', student_list)

        print('出席紀錄\t\t\t:', attendance_record)
        count = sum(value == 1 for value in attendance_record.values())
        total += count
        print('出席率:', count/len(student_list))
    print('\n平均出席率:', total/12/len(student_list))


# if __name__ == '__main__':
#     # 指定剛剛下載tesseract.exe的完整路徑
#     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#     image = Image.open('source/1-2.jpg')
#     # 這裡的lang就是剛剛下載的model
#     text = pytesseract.image_to_string(image, lang='chi_tra')
#     text = text.replace("\n", "").replace(" ", "")
#     text = text.strip()
#     print(text)
