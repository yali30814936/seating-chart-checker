from Student import Student
from RollcallRecord import RollcallRecord


class Course:
    def __init__(self, name, ID):
        self._name = name
        self._ID = ID

        self._student_list = [
            Student("Steven", "00000001", "資工系"),
            Student("Amelia", "00000002", "資工系"),
            Student("Marco", "00000003", "電機系"),
            Student("Steven", "00000004", "資工系"),
            Student("Amelia", "00000005", "資工系"),
            Student("Marco", "00000006", "電機系"),
            Student("Steven", "00000007", "資工系"),
            Student("Amelia", "00000008", "資工系"),
            Student("Marco", "00000009", "電機系"),
            Student("Steven", "000000010", "資工系"),
            Student("Amelia", "00000011", "資工系"),
            Student("Marco", "00000012", "電機系"),
            Student("Steven", "00000013", "資工系"),
            Student("Amelia", "00000014", "資工系"),
            Student("Marco", "00000015", "電機系"),
        ]

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
        return self._student_list

    def add_rollcall_record(self, date, rollcall_result: dict()):
        self._rollcall_records[date] = RollcallRecord(rollcall_result)

    def add_student(self, name, ID, department):
        self._student_list.append(Student(name, ID, department))

    def remove_student(self, ID):
        del self._student_list[ID]

    def get_dates_of_rollcall_records(self):
        return list(self._rollcall_records.keys())

    def get_rollcall_record(self, date):
        return self._rollcall_records[date].attendance_list

    def edit_rollcall_record(self, date, student_ID, attend_status):
        self._rollcall_records[date].edit(student_ID, attend_status)
