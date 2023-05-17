from IdentifyModule import IdentifyModule
from Course import Course
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image


class Controller:
    def __init__(self):
        # set UI...

        self.identifyModule = IdentifyModule()
        self.photo_path = "photo.jpg"
        self.course_list = [
            Course("course1", "0001"),
            Course("course2", "0002"),
            Course("course3", "0003"),
        ]
        self.operating_course = None

        self.open_homepage()

    def check_rollcall(self):
        student_list = self.operating_course.get_student_list()
        result = self.identifyModule.check_rollcall(self.photo_path, student_list)
        # set UI show the result

    def open_student_list(self):
        student_list = self.operating_course.get_student_list()
        # set UI show the student_list

    def adding_student(self):
        # 使用者輸入欲新增學生之 name, ID, department
        name, ID, department = "", "", ""
        self.operating_course.add_student(name, ID, department)

    def removing_student(self):
        # 使用者輸入欲新增學生之 ID
        ID = ""
        self.operating_course.remove_student(ID)

    def open_rollcall_records(self):
        dates = self.operating_course.get_dates_of_rollcall_records()
        # set UI 列出所有日期的按鈕

    def open_a_rollcall_record(self, date):
        # set UI 進入對點名紀錄操作頁面
        pass

    def editing_rollcall_record(self):
        # 待定義
        pass

    def open_homepage(self):
        # set UI 把所有課程按鈕列出來
        root = Tk()
        root.geometry("1000x700")
        root.title("課程點名系統")
        # 上方圖片
        image = Image.open("tmp.png")
        image = image.resize((500, 500))
        photo = ImageTk.PhotoImage(image)
        picture = tk.Label(root, image=photo)
        picture.pack()

        # 中間選單
        selected_option = tk.StringVar()
        combo_box = ttk.Combobox(root, textvariable=selected_option)
        value = []
        for c in self.course_list:
            value.append(c.name)
        combo_box["values"] = value
        combo_box.pack()
        button1 = tk.Button(
            root,
            text="選擇課程",
            command=lambda: self.open_a_course(combo_box.current()),
            width=20,
            height=2,
        )
        button1.pack(padx=10, pady=10)
        button2 = tk.Button(
            root, text="新增課程", command=self.adding_course, width=20, height=2
        )
        button2.pack(padx=10, pady=10)
        root.mainloop()

    def open_a_course(self, index):
        self.operating_course = self.course_list[index]
        print(self.operating_course)
        # set UI 進入對課程操作頁面

    def adding_course(self):
        # 使用者輸入 name, ID
        name = ""
        ID = ""
        self.course_list.append(Course(name, ID))


ctr = Controller()
