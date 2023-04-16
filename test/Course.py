from Student import Student
from RollcallRecord import RollcallRecord


class Course:

    def __init__(self, name, ID):
        self._name = name
        self._ID = ID

        self._student_list = []
        self._rollcall_records = dict()

    @property
    def name(self):
        return self._name

    @property
    def ID(self):
        return self._ID

    def get_student_list(self):
        return self._student_list

    def add_rollcall_record(self, date, rollcall_result):
        self._rollcall_records[date] = RollcallRecord(rollcall_result)

    def add_student(self, name, ID, department):
        self._student_list.append(Student(name, ID, department))

    def remove_student(self, ID):
        self._student_list.remove(ID)

    def get_dates_of_rollcall_records(self):
        return list(self._rollcall_records.keys())

    def edit_rollcall_record(self):
        # 待定義
        pass
