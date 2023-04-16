from IdentifyModule import IdentifyModule
from Course import Course


class Controller:

    def __init__(self):
        # set UI...

        self.identifyModule = IdentifyModule()
        self.photo_path = "photo.jpg"
        self.courses = []
        self.operating_course = None

        self.open_homepage()

    def check_rollcall(self):
        student_list = self.operating_course.get_student_list()
        result = self.identifyModule.check_rollcall(self.photo_path, student_list)
        # set UI show the result
        pass

    def open_student_list(self):
        student_list = self.operating_course.get_student_list()
        # set UI show the student_list
        pass

    def adding_student(self):
        # 使用者輸入欲新增學生之 name, ID, department
        name, ID, department = "", "", ""
        self.operating_course.add_student(name, ID, department)
        pass

    def removing_student(self):
        # 使用者輸入欲新增學生之 ID
        ID = ""
        self.operating_course.remove_student(ID)
        pass

    def open_rollcall_records(self):
        dates = self.operating_course.get_dates_of_rollcall_records()
        # set UI 列出所有日期的按鈕
        pass

    def open_a_rollcall_record(self, date):
        # set UI 進入對點名紀錄操作頁面
        pass

    def editing_rollcall_record(self):
        # 待定義
        pass

    def open_homepage(self):
        # set UI 把所有課程按鈕列出來
        pass

    def open_a_course(self, index):
        self.operating_course = self.courses[index]
        # set UI 進入對課程操作頁面
        pass

    def adding_course(self):
        # 使用者輸入 name, ID
        name = ""
        ID = ""
        self.courses.append(Course(name, ID))
