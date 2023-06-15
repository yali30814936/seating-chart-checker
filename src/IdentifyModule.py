from typing import Tuple, Any, Dict, Optional, List, Union
from google.cloud import vision
from PIL import ImageFont, ImageDraw, Image
import os
import cv2
import numpy as np


# 設定 Google API 憑證環境變數
os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = r"resource/seating-chart-checker-2389976159cf.json"


# 可能只適用 sample 測資
def _getRectCorners(vertices, width, height):
    left, top = width, height
    right, bottom = 0, 0
    for vertex in vertices:
        left = vertex.x if vertex.x < left else left
        top = vertex.y if vertex.y < top else top
        right = vertex.x if vertex.x > right else right
        bottom = vertex.y if vertex.y > bottom else bottom
    return (left, top), (right, bottom)
    # left, top = height, width
    # right, bottom = 0, 0
    # for vertex in vertices:
    #     left = vertex.x if vertex.x < left else left
    #     top = vertex.y if vertex.y < top else top
    #     right = vertex.x if vertex.x > right else right
    #     bottom = vertex.y if vertex.y > bottom else bottom
    # return (width-bottom, left), (width-top, right)


def _put_chinese_text(img, string, pos, color):
    font_path = "resource/NotoSansTC-Bold.otf"  # 設定字型路徑
    font = ImageFont.truetype(font_path, img.shape[1]//40)  # 設定字型與文字大小
    imgPil = Image.fromarray(img)  # 將 img 轉換成 PIL 影像
    draw = ImageDraw.Draw(imgPil)
    draw.text(pos, string, fill=color, font=font)  # 畫入文字，\n 表示換行
    return np.array(imgPil)  # 將 PIL 影像轉換成 numpy 陣列


def _detect_text(img: np.ndarray) -> list:
    """
    Use Google cloud vision API to detect text.
    return a list of detected words.
    """

    client = vision.ImageAnnotatorClient()
    success, encoded_image = cv2.imencode(".jpg", img)
    content = encoded_image.tobytes()
    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    return texts


def check_rollcall(
    img: np.ndarray, student_list: list[str]
) -> tuple[np.ndarray, dict[str, int], list[str]]:
    """
    Detect text on the image, and match to the student list, and return the attendance status.

    Args:
        img (ndarray): the image to detect.
        student_list (list): a list of all student names, currently haven't considered non-three-word names yet.
    Returns:
        image ndarray: image that display the roll call result.
        dict[str, int]: attendance status.
            str: all students in given student_list.
            int: their attendance status. (0:缺席 1:出席)
        list[str]: a name list that records those who has been yellow-framed
    """

    # -1. 辨識文字

    texts_info = _detect_text(img)
    word_list = texts_info[0].description.split("\n")
    # word_list = ['日期:QCT/5', '俞浩君', '某洢岑', '張文虹', '范文瑄', 'FIL', 'TTF', '講臺', '陳長', '戴柏儀', '劉明融', '姜紹淳',
    #              'TOO', '技政偉孔繁道張慈芸大型陳慧慧', '劉品萱', '周远', '省達', '强思淇', '陈宇軒', '关系数', '天家', '陳芃铵',
    #              '黄雅欣', '駱宥亘|郭家佑']  # detect_text('resource/sheet_samples/1.jpg') 出來的結果
    print("detected words\t:", word_list)
    height, width = img.shape[:2]

    # -2. 配對演算法

    unmatched_words = set(word_list)
    unmatched_students = set(student_list)
    # 防呆有學生完全同名，同名的直接排除不進入配對，最後再補為缺席
    repeated_students = set()
    if len(unmatched_students) != len(student_list):
        for stud in unmatched_students:
            if student_list.count(stud) > 1:
                repeated_students.add(stud)
    for stud in repeated_students:
        unmatched_students.remove(stud)

    # 標示框格用
    # dict[text: their bounding_poly (list)]，因可能有一樣的 detected_text，value將不只一個，故用 list
    unframed_texts = {text.description: [] for text in texts_info[1:]}
    for text in texts_info[1:]:
        unframed_texts[text.description].append(text.bounding_poly)

    # -2.1 完全相等的 先配對

    target = unmatched_students
    green_marks = []  # 在 -3.1 -3.2 match 到的文字段 (mask的.會還原為原字)
    to_add, to_remove = [], []
    for word in unmatched_words:
        if len(word) < 3:
            continue
        c = 0
        while c < len(word) - 2:  # c只會逐步+1，或可能在途中歸 0 並且減少 len(word)
            if word[c : c + 3] in target:
                green_marks.append(word[c : c + 3])  # 標示框格用
                try:
                    unmatched_students.remove(word[c : c + 3])
                except KeyError:
                    # pass
                    print(
                        "文字重複辨識，或兩人名字不相同辨識成完全相同，導致重複 remove / 學生名字:",
                        target[word[c : c + 3]],
                    )
                to_remove.append(word)
                # 若此為長字串，就以該三字做分割，切出兩個字串，空字串就不用切出來了
                if c != 0:
                    to_add.append(word[:c])
                if c + 3 != len(word):
                    word = word[c + 3 :]  # 將當前處理的 word 替換為剩下的這段
                    to_add.append(word)
                    c = 0  # 從新 word 的頭開始掃
                else:
                    c += 1  # c會等於 len(word)-2，將不會繼續下一次迴圈
            else:
                c += 1
    for ele in to_add:
        unmatched_words.add(ele)
    for ele in to_remove:
        unmatched_words.remove(ele)
    # print('unmatched words\t:', unmatched_words)

    # -2.2 兩個字相同且其相對位置相同的 再配對

    target = dict()  # target 為所有 unmatched_student 產生的 3個 mask
    to_remove = set()
    for name in unmatched_students:
        for mask in [name[0:2] + ".", name[0] + "." + name[2], "." + name[1:3]]:
            # 若有兩人名字中有兩字相同且位置相同，做 mask 就會重複，故不能放進 target
            if mask in target:
                to_remove.add(mask)  # 可能第三個人名字有兩字相同的，所以不能直接刪除
            else:
                target[mask] = name
    for ele in to_remove:
        del target[ele]
    # print(target)
    to_add, to_remove = [], []
    for word in unmatched_words:
        if len(word) == 1:
            continue
        if len(word) == 2:
            for mask in [word + ".", "." + word]:
                if mask in target:
                    green_marks.append(word)  # 標示框格用
                    try:
                        unmatched_students.remove(target[mask])
                    except KeyError:
                        # pass
                        print(
                            "文字重複辨識，或兩人名字兩字不相同辨識成相同，導致重複 remove / 學生名字:",
                            target[mask],
                            "/ mask:",
                            mask,
                        )
                    to_remove.append(word)
                    break
            continue
        c = 0
        while c < len(word) - 2:  # c只會逐步+1，或可能在途中歸 0 並且減少 len(word)
            for m, mask in enumerate(
                [
                    word[c : c + 2] + ".",
                    word[c] + "." + word[c + 2],
                    "." + word[c + 1 : c + 3],
                ]
            ):
                if mask in target:
                    green_marks.append(word[c : c + 3])  # 標示框格用
                    try:
                        unmatched_students.remove(target[mask])
                    except KeyError:
                        # pass
                        print(
                            "文字重複辨識，或兩人名字兩字不相同辨識成相同，導致重複 remove / 學生名字:",
                            target[mask],
                            "/ mask:",
                            mask,
                        )
                    to_remove.append(word)
                    # 如果 '.' 不是夾在中間，就只要以兩字做分割，否則一樣三字
                    # 但若 '.' 的那側只剩它一個字了，代表那個字大概只是辨識錯字，就不用切出來了
                    if c != 0:
                        to_add.append(word[: c + 1 if m == 2 else c])
                    if c + 3 != len(word):
                        word = word[
                            c + 2 if m == 0 else c + 3 :
                        ]  # 將當前處理的 word 替換為剩下的這段
                        to_add.append(word)
                        c = 0  # 從新 word 的頭開始掃
                    else:
                        c += 1  # c會等於 len(word)-2，將不會繼續下一次迴圈
                    # c += 2 if (m == 0 and c + 3 != len(word)) else 3
                    break  # 不看剩下的 mask
            else:
                c += 1
    for ele in to_add:
        unmatched_words.add(ele)
    for ele in to_remove:
        unmatched_words.remove(ele)
    # print('unmatched words\t:', unmatched_words)

    # -2.3 標示綠色框

    to_frame = set()
    for mark in green_marks:
        if mark in unframed_texts:
            to_frame.add(mark)
        elif len(mark) == 3:
            for segm in [mark[:2], mark[1:], mark[0], mark[1], mark[2]]:
                if segm in unframed_texts:
                    to_frame.add(segm)
        elif len(mark) == 2:
            for segm in [mark[0], mark[1]]:
                if segm in unframed_texts:
                    to_frame.add(segm)
    for ele in to_frame:
        for unframed_text in unframed_texts[ele]:  # 可能有一樣的 detected_text，通常只有一個
            corners = _getRectCorners(unframed_text.vertices, width, height)
            cv2.rectangle(img, corners[0], corners[1], (0, 120, 0), img.shape[1]//600)
        del unframed_texts[ele]

    # -2.4 所有人裡只出現一次的字 且 偵測文字中也只出現一次 再配對

    # dict[所有剩餘學生中只出現一次的字: 該student]
    stud_with_only_char = dict()
    to_remove = set()
    for stud in unmatched_students:
        for ch in stud:
            if ch in stud_with_only_char:
                to_remove.add(ch)  # 該字可能出現三次，故不能直接 del
            else:
                stud_with_only_char[ch] = stud
    for ch in to_remove:
        del stud_with_only_char[ch]
    # dict[所有剩餘學生中只出現一次 且 所有剩餘word中也只出現一次 的字: (該student, 該word)]
    match_pair_with_only_char = dict()
    to_remove = set()
    for word in unmatched_words:
        for ch in word:
            if ch in stud_with_only_char:
                if ch in match_pair_with_only_char:
                    to_remove.add(ch)  # 該字可能出現三次，故不能直接 del
                else:
                    match_pair_with_only_char[ch] = (stud_with_only_char[ch], word)
    for ch in to_remove:
        del match_pair_with_only_char[ch]

    for match_pair in match_pair_with_only_char.values():
        try:
            unmatched_students.remove(match_pair[0])
        except KeyError:
            print("可能發生一個簽名被偵測為兩個word的狀況，或發生像 8.jpg 那樣(abc->ac)，目前沒想過其他可能")
        try:
            unmatched_words.remove(
                match_pair[1]
            )  # 目前後面沒再用到 unmatched_words，因此此 remove 沒特別設計，不然應該再切左右兩段出來
        except KeyError:
            print("可能發生一個簽名被偵測為兩個word的狀況，或發生像 8.jpg 那樣(abc->ac)，目前沒想過其他可能")

    print("yellow-matched\t:", match_pair_with_only_char)
    print("unmatched words\t:", unmatched_words)

    # -2.5 標示黃色框

    to_remove = set()
    frame_times = 0  # 印出用
    yellow_framed_names = set()  # 回傳用
    for text in unframed_texts:
        lay = 0
        for ch in text:
            if ch in match_pair_with_only_char:
                lay += 1
                frame_times += 1  # 相同的 detected text 算一次
                yellow_framed_names.add(match_pair_with_only_char[ch][0])
                for unframed_text in unframed_texts[text]:
                    corners = _getRectCorners(unframed_text.vertices, width, height)
                    cv2.rectangle(img, corners[0], corners[1], (0, 200, 255), img.shape[1]//600)
                    img = _put_chinese_text(
                        img,
                        match_pair_with_only_char[ch][0],
                        (corners[0][0], corners[0][1] - (img.shape[1]//30 * lay)),
                        (0, 150, 150),
                    )
                to_remove.add(text)  # 複雜到不想解釋，總之用set保險
        if lay > 1:
            print("text重複黃標，已把疊起來的字移開")  # 應該極罕見
    for ele in to_remove:
        del unframed_texts[ele]
    # 發生該黃標的 text 被重複綠標的情況
    if len(match_pair_with_only_char) != frame_times:
        print(
            "yellow_match:",
            len(match_pair_with_only_char),
            "/ yellow_frame:",
            frame_times,
        )

    # -2.6 剩下沒配對上的 標示為紅色框

    for _list in unframed_texts.values():
        for unframed_text in _list:  # 可能有一樣的 detected_text，通常只有一個
            corners = _getRectCorners(unframed_text.vertices, width, height)
            cv2.rectangle(img, corners[0], corners[1], (50, 50, 255), img.shape[1]//600)

    # -3. 回傳圖片出勤記錄
    # small_img = cv2.resize(img, (1000, 750))
    # cv2.imshow("image", small_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    attendance = dict()
    for student in student_list:
        attendance[student] = 0 if student in unmatched_students else 1

    for student in repeated_students:
        attendance[student] = 0  # 給老師人工補點名

    return img, attendance, list(yellow_framed_names)


if __name__ == "__main__":
    # student_list = ['俞浩君', '葉洢岑', '劉昀融', '張慈芸', '周子丞']
    student_list = [
        "俞浩君",
        "廖令弘",
        "曾昱翔",
        "林政偉",
        "周子娟",
        "黃雅欣",
        "郭家佑",
        "駱宥亘",
        "周暐翔",
        "劉昀融",
        "姜紹淳",
        "陳晏慈",
        "葉洢岑",
        "羅苡心",
        "黃偉綸",
        "陳慧雲",
        "陳芃銨",
        "劉凱菁",
        "張慈芸",
        "孔繁瑄",
        "周子丞",
        "王大埊",
        "陳振榕",
        "蔡宇軒",
        "戴柏儀",
    ]

    # attendance_record = check_rollcall('resource/sheet_samples/1.jpg', student_list)
    # print('出席紀錄\t\t\t:', attendance_record)

    total = 0
    for i in range(1, 13):
        print("\n[test " + str(i) + ".jpg]")

        img, attendance_record, yellow_list = check_rollcall(
            cv2.imread("resource/sheet_samples/" + str(i) + ".jpg"), student_list
        )
        print("出席紀錄\t\t\t:", attendance_record)
        print("黃標名單\t\t\t:", yellow_list)
        # count = sum(value == 1 for value in attendance_record.values())
        # total += count
        # print('出席率:', count/len(student_list))
    # print('\n平均出席率:', total/12/len(student_list))
