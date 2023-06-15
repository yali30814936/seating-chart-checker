import cv2
import numpy as np
from Course import *
from IdentifyModule import check_rollcall
from PIL import Image, ImageTk


def load_image(path: str):
    """讀取圖片並回傳 np 格式的照片

    Args:
        path (str): 圖片檔案路徑

    Returns:
        ndarray: numpy 型態的圖片
    """
    img = cv2.imread(path)
    return img


def rotate_image(img):
    """順時針旋轉圖片 90 度

    Args:
        img (ndarray): numpy 型態的圖片

    Returns:
        ndarray: numpy 型態轉完90度的圖片
    """
    return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)


def check_rollcall_adapter(img: np.ndarray, course: Course):
    """點名功能接口

    Args:
        img (np.ndarray): 影像 ndarray
        course (Course): 課程物件

    Returns:
        來自 `IdentifyModule.check_rollcall()` 的原始輸出:
        _image ndarray: image that display the roll call result.
        dict[str, int]: attendance status.
            str: all students in given student_list.
            int: their attendance status. (0:缺席 1:出席)
        list[str]: a name list that records those who has been yellow-framed
    """

    stu_list = [n.ID for n in course.get_student_list()]
    return check_rollcall(img, stu_list)


def to_readable_attendence_list(attendence: dict, course: Course):
    """將出席名單轉換成 「學號: [名字, 出席]」格式

    Args:
        attendence (dict): 出席清單，格式為「學號: 出席」
        course (Course): 課程物件

    Returns:
        dict: 「學號: [名字, 出席]」格式的字典
    """
    stu_list = [[i.ID, i.name] for i in course.get_student_list()]
    res = attendence.copy()

    def search(ls: list, id: str):
        for i in ls:
            if i[1] == id:
                return i[0]

    for id, at in res.items():
        res[id] = [search(stu_list, id), at]

    return res


def docking_attendence(course:Course, attendence:dict):
    """將「姓名：出席」格式轉換為「學號：出席」格式

    Args:
        course (Course): 課程物件
        attendence (dict): 「姓名：出席」格式的字典

    Returns:
        dict: 「學號：出席」格式的字典
    """
    stu_list = [[i.ID, i.name] for i in course.get_student_list()]
    res = dict.fromkeys([i.name for i in course.get_student_list()], 0)
    
    def search(ls: list, name: str):
        _res = []
        for i in ls:
            if i[0] == name:
                _res.append(i[1])
        return _res
    
    for nm, at in attendence.items():
        s = search(stu_list, nm)
        for id in s:
            res[id] = at
            
    return res
