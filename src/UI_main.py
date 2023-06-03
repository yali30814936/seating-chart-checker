# import IdentifyModule
from Course import Course
from RollcallRecord import *
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image


class Application:
    def __init__(self):
        # set UI...

        self.photo_path = "photo.jpg"
        self.course_list = [
            Course("人格發展與精神分析", "B9M014TG"),
            Course("戰爭、武器、流亡詩人與全球公民", "B9M014V8"),
            Course("性別、身體與意識型態", "B9M014TV"),
        ]
        self.operating_course = None
        self.windows = []
        self.rt_flag = 0
        self.open_homepage()

    def check_rollcall(self):
        student_list = self.operating_course.get_student_list()
        # result = IdentifyModule.check_rollcall(self.photo_path, student_list)
        result = RollcallRecord(
            {
                "00000001": 0,
                "00000002": 0,
                "00000003": 0,
            }
        )
        date = "1120601"
        self.operating_course.add_rollcall_record(date, result)
        # switch to rollcall_record page to show the result
        self.open_a_rollcall_record(date)

    def open_student_list(self):
        student_list = self.operating_course.get_student_list()
        # set UI show the student_list
        self.windows.destroy()
        window = Tk()
        window.geometry("1000x700")
        window.title("課程點名系統")
        self.windows = window
        button1 = tk.Button(
            window,
            text="返回主頁面",
            command=lambda: window.destroy(),
            width=20,
            height=2,
        )
        button1.pack(padx=10, pady=10)
        window.mainloop()

    def adding_student(self):
        # 使用者輸入欲新增學生之 name, ID, department
        name, ID, department = "", "", ""
        self.operating_course.add_student(name, ID, department)

    def removing_student(self):
        # 使用者輸入欲新增學生之 ID
        ID = ""
        self.operating_course.remove_student(ID)

    def show_rollcall_records(self):
        dates = self.operating_course.get_dates_of_rollcall_records()
        # set UI 列出所有日期的按鈕

    def open_a_rollcall_record(self, date=0):
        # set UI 進入對點名紀錄操作頁面
        self.windows.destroy()
        window = Tk()
        window.geometry("1000x700")
        window.title("課程點名系統")
        self.windows = window
        button1 = tk.Button(
            window, text="返回主畫面", command=window.destroy(), width=20, height=2
        )
        button1.pack(padx=10, pady=10)
        window.mainloop()

    def editing_rollcall_record(self):
        # 待定義
        pass

    def open_homepage(self):
        while 1:
            self.operating_course = None
            # set UI 把所有課程按鈕列出來
            window = Tk()
            self.windows = window
            window.geometry("1000x700")
            window.title("課程點名系統")
            # 上方圖片
            image = Image.open("tmp.png")
            image = image.resize((500, 500))
            photo = ImageTk.PhotoImage(image)
            picture = tk.Label(window, image=photo)
            picture.pack()

            # 中間選單
            selected_option = tk.StringVar()
            combo_box = ttk.Combobox(window, textvariable=selected_option)
            value = []
            for c in self.course_list:
                value.append(c.name)
            combo_box["values"] = value
            combo_box.pack()
            button1 = tk.Button(
                window,
                text="選擇課程",
                command=lambda: (self.open_a_course(combo_box.current())),
                width=20,
                height=2,
            )
            button1.pack(padx=10, pady=10)
            button2 = tk.Button(
                window, text="新增課程", command=self.adding_course, width=20, height=2
            )
            button2.pack(padx=10, pady=10)
            window.mainloop()

    def open_a_course(self, index):
        self.windows.destroy()
        self.operating_course = self.course_list[index]
        window_cource = Tk()
        window_cource.geometry("1000x700")
        window_cource.title("課程點名系統")
        self.windows = window_cource
        # 上方圖片
        button1 = tk.Button(
            window_cource,
            text="點名",
            command=lambda: self.open_a_rollcall_record(),
            width=20,
            height=2,
        )
        button1.pack(padx=10, pady=10)
        button2 = tk.Button(
            window_cource,
            text="學生名單",
            command=lambda: self.open_student_list(),
            width=20,
            height=2,
        )
        button2.pack(padx=10, pady=10)
        button3 = tk.Button(
            window_cource,
            text="返回",
            command=lambda: window_cource.destroy(),
            width=20,
            height=2,
        )
        button3.pack(padx=10, pady=10)
        window_cource.mainloop()

    def adding_course(self):
        # 使用者輸入 name, ID
        name = ""
        ID = ""
        self.course_list.append(Course(name, ID))


ctr = Application()
