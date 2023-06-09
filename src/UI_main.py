# import IdentifyModule
from Course import *
from RollcallRecord import *
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter import messagebox, simpledialog
from Course import load_courses

class Application:
    def __init__(self):
        # set UI...

        self.photo_path = "photo.jpg"
        self.course_list = load_courses()
        # self.course_list = [
        #     Course("人格發展與精神分析", "B9M014TG"),
        #     Course("戰爭、武器、流亡詩人與全球公民", "B9M014V8"),
        #     Course("性別、身體與意識型態", "B9M014TV"),
        # ]
        self.operating_course = None
        self.windows = []
        self.file_path = "tmp.png"
        self.flag = 1
        self.open_homepage()

    def set_flag(self, k):
        self.flag = k

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
        # set UI show the student_list
        self.windows.destroy()
        self.set_flag(1)
        while self.flag:
            window = Tk()
            window.geometry("1000x700")
            window.title("課程點名系統")
            self.windows = window

            # 按鈕一
            button1 = tk.Button(
                window,
                text="返回主頁面",
                command=lambda: (self.set_flag(0), window.destroy()),
                width=20,
                height=2,
            )
            button1.place(x=600, y=450)

            tree = ttk.Treeview(window, columns=(1, 2, 3), show="headings")
            tree.configure(height=20)
            tree.pack()
            # 設置列標題
            tree.heading(1, text="姓名")
            tree.heading(2, text="學號")
            tree.heading(3, text="系級")
            elements = self.operating_course.get_student_list()
            for element in elements:
                tree.insert(
                    "",
                    tk.END,
                    values=(
                        element.name,
                        element.ID,
                        element.department,
                    ),
                )

            # 新增學生按鈕
            button2 = tk.Button(
                window,
                text="新增學生",
                command=lambda: (self.adding_student(), window.destroy()),
                width=20,
                height=2,
            )
            button2.place(x=200, y=450)

            button3 = tk.Button(
                window,
                text="刪除學生",
                command=lambda: (
                    self.removing_student(tree.index(tree.focus())),
                    window.destroy(),
                ),
                width=20,
                height=2,
            )
            button3.place(x=400, y=450)
            window.mainloop()

    def adding_student(self):
        # 使用者輸入欲新增學生之 name, ID, department
        name = simpledialog.askstring("新增學生", "格式 : 學生姓名,學號,系級\n\nex:王大明,00001,資工系")

        data = name.split(",")
        if name:
            self.operating_course.add_student(data[0], data[1], data[2])
            messagebox.showinfo(
                "新增目標", f"已新增目標：\nName: {data[0]}\nID: {data[1]}\n系級:{data[2]}"
            )

    def removing_student(self, ID):
        self.operating_course.remove_student(ID)

    def reload_tree(self, tree, rcord):
        tree.delete(*tree.get_children())
        tree.heading(1, text="學號")
        tree.heading(2, text="有無出席")
        for student_id, attendance in rcord.items():
            tree.insert(
                "",
                tk.END,
                text=student_id,
                value=(
                    student_id,
                    attendance,
                ),
            )

    def show_rollcall_records(self, dates):
        window = Tk()
        window.geometry("600x450")
        window.title(dates)
        tree = ttk.Treeview(window, columns=(1, 2), show="headings")
        tree.configure(height=10)
        tree.pack()
        # 設置列標題
        self.reload_tree(tree, self.operating_course.get_rollcall_record(dates))

        button1 = tk.Button(
            window, text="返回", command=lambda: window.destroy(), width=20, height=2
        )
        button1.place(x=350, y=250)
        button2 = tk.Button(
            window,
            text="編輯",
            command=lambda: (
                self.editing_rollcall_record(
                    dates,
                    tree.item(tree.selection())["values"],
                    tree.item(tree.selection())["text"],
                ),
                self.reload_tree(
                    tree, self.operating_course.get_rollcall_record(dates)
                ),
            ),
            width=20,
            height=2,
        )
        button2.place(x=100, y=250)
        window.mainloop()
        # set UI 列出所有日期的按鈕

    def open_file(self, canvas):
        self.file_path = filedialog.askopenfilename()  # 讓使用者選擇檔案
        if self.file_path:
            with Image.open(self.file_path) as image:
                image = image.resize((500, 500))
                photo = ImageTk.PhotoImage(image)
                canvas.delete("all")  # 清空畫布
                canvas.create_image(0, 0, anchor="nw", image=photo)
                canvas.image = photo

    def open_a_rollcall_record(self, date=0):
        # set UI 進入對點名紀錄操作頁面
        self.windows.destroy()
        window = Tk()
        window.geometry("1000x700")
        window.title("課程點名系統")
        self.windows = window
        button1 = tk.Button(
            window, text="返回主畫面", command=lambda: window.destroy(), width=20, height=2
        )
        button1.place(x=600, y=300)

        # 圖片路徑
        button2 = tk.Button(
            window,
            text="選擇圖片",
            command=lambda: (self.open_file(canvas)),
            width=20,
            height=2,
        )
        button2.place(x=600, y=100)

        # 確定點名 ### 點名function放這裡
        button2 = tk.Button(
            window,
            text="確定點名",
            command=lambda: (),
            width=20,
            height=2,
        )
        button2.place(x=600, y=200)

        # 畫面暫時顯示
        image = Image.open("tmp.png")
        image = image.resize((500, 500))
        init_photo = ImageTk.PhotoImage(image)
        canvas = tk.Canvas(window, width=400, height=400)
        canvas.create_image(0, 0, anchor="nw", image=init_photo)
        canvas.image = init_photo
        canvas.place(x=100, y=100)
        window.mainloop()

    def editing_rollcall_record(self, date, std, id):
        self.operating_course.edit_rollcall_record(date, id, (std[1] + 1) % 2)

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
                window,
                text="新增課程",
                command=lambda: (self.adding_course(), window.destroy()),
                width=20,
                height=2,
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
        button1 = tk.Button(
            window_cource,
            text="點名",
            command=lambda: self.open_a_rollcall_record(),
            width=20,
            height=2,
        )
        button1.place(x=500, y=100)
        button2 = tk.Button(
            window_cource,
            text="學生名單",
            command=lambda: self.open_student_list(),
            width=20,
            height=2,
        )
        button2.place(x=500, y=200)
        button3 = tk.Button(
            window_cource,
            text="返回",
            command=lambda: window_cource.destroy(),
            width=20,
            height=2,
        )
        button3.place(x=500, y=300)

        # list 全部點名紀錄
        listbox = tk.Listbox(window_cource, width=50, height=30)
        # 添加項目到 Listbox
        elements = self.operating_course.get_dates_of_rollcall_records()
        for element in elements:
            listbox.insert(tk.END, element)
        # 綁定選擇事件處理函式
        listbox.bind(
            "<<ListboxSelect>>",
            lambda event: self.show_rollcall_records(
                listbox.get(listbox.curselection())
            ),
        )

        listbox.place(x=100, y=100)
        window_cource.mainloop()

    def adding_course(self):
        # 使用者輸入 name, ID
        data = simpledialog.askstring("新增課程：", "輸入:課程名稱,ID\n\nex:軟體工程,B1234567")
        datas = data.split(",")
        if data:
            self.course_list.append(Course(datas[0], datas[1]))
            messagebox.showinfo("新增目標", f"已新增目標：\nName: {datas[0]}\nID: {datas[1]}")


ctr = Application()
