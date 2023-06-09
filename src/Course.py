from Student import Student
from RollcallRecord import RollcallRecord
import csv
import os

_DATA_DIR = r"..\data"
_COURSES_FN = r"courses.csv"

class Course:
    def __init__(self, name, ID):
        self._name = name
        self._ID = ID

        self._student_list = None
        self._student_list = self.get_student_list()
        # self._student_list = [
        #     Student("Steven", "00000001", "資工系"),
        #     Student("Amelia", "00000002", "資工系"),
        #     Student("Marco", "00000003", "電機系"),
        #     Student("Steven", "00000004", "資工系"),
        #     Student("Amelia", "00000005", "資工系"),
        #     Student("Marco", "00000006", "電機系"),
        #     Student("Steven", "00000007", "資工系"),
        #     Student("Amelia", "00000008", "資工系"),
        #     Student("Marco", "00000009", "電機系"),
        #     Student("Steven", "000000010", "資工系"),
        #     Student("Amelia", "00000011", "資工系"),
        #     Student("Marco", "00000012", "電機系"),
        #     Student("Steven", "00000013", "資工系"),
        #     Student("Amelia", "00000014", "資工系"),
        #     Student("Marco", "00000015", "電機系"),
        # ]

        self._rollcall_records = {
            "1120518": RollcallRecord(
                {
                    "00000001": 1,
                    "00000002": 1,
                    "00000003": 0,
                }
            ),
            "1120525": RollcallRecord(
                {
                    "00000001": 1,
                    "00000002": 0,
                    "00000003": 1,
                    "01231245": 1,
                }
            ),
        }

    @property
    def name(self):
        return self._name

    @property
    def ID(self):
        return self._ID

    def get_student_list(self):
        _crdr = os.path.join(_DATA_DIR, self._ID)
        _stls = os.path.join(_crdr, self._ID + ".csv")
        # 第一次讀取
        if self._student_list == None:
            self._student_list = []
            if os.path.exists(_stls):
                # 檔案存在則讀檔
                with open(_stls, 'r', encoding='utf-8') as fp:
                    rows = csv.reader(fp)
                    for row in rows:
                        self._student_list.append(Student(row[0], row[1], row[2]))
            else:
                # 資料夾不在則建夾
                if not os.path.exists(_crdr):
                    os.mkdir(_crdr)
                # 建檔
                with open(_stls, 'w', encoding='utf-8') as fp:
                    fp.close()
                    
        return self._student_list

    def add_rollcall_record(self, date, rollcall_result: dict()):
        self._rollcall_records[date] = RollcallRecord(rollcall_result)

    def _save_student_list(self):
        _stls = os.path.join(_DATA_DIR, self._ID, self._ID + ".csv")
        with open(_stls, 'w', encoding='utf-8') as fp:
            writer = csv.writer(fp)
            writer.writerows(self._student_list)
    
    def add_student(self, name, ID, department):
        self._student_list.append(Student(name, ID, department))
        self._save_student_list()
        
    def remove_student(self, idx):
        self._student_list.pop(idx)
        self._save_student_list()

    def get_dates_of_rollcall_records(self):
        return list(self._rollcall_records.keys())

    def get_rollcall_record(self, date):
        return self._rollcall_records[date].attendance_list

    def edit_rollcall_record(self, date, student_ID, attend_status):
        self._rollcall_records[date].edit(student_ID, attend_status)


def get_course_list():
    """讀取課程清單

    Returns:
        tuple[tuple(str, str)]: (課名, 課號) 列表，唯讀
    """
    _res = []
    _cfile = os.path.join(_DATA_DIR, _COURSES_FN)
    # 確認是否存在課程清單
    if os.path.exists(_cfile):
        # 讀取課程清單
        with open(_cfile, 'r', encoding='utf-8') as fp:
            rows = csv.reader(fp)
            for row in rows:
                _res.append(tuple(row))
    else:
        # 連 data 資料夾都不存在的話，先創資料夾
        if not os.path.exists(_DATA_DIR):
            os.mkdir(_DATA_DIR)
        # 開檔
        with open(_cfile, 'w', encoding='utf-8') as fp:
            fp.close()
                
    return tuple(_res)


def load_courses():
    """讀取課程物件清單

    Returns:
        Tuple(Course): Course 陣列，唯讀
    """
    _course_list = get_course_list()
    _res = []
    for course in _course_list:
        _res.append(Course(course[0], course[1]))
    return tuple(_res)