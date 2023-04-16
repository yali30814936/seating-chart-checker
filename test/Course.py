
class Course:

    def __init__(self, name, ID):
        self._name = name
        self._ID = ID

        self._student_list = []
        self._rollcall_records = []

    def get_student_list(self):
        return self._student_list
        pass

    def add_rollcall_record(self, date, rollcall_result):
        pass

    def add_student(self, name, ID, department):
        pass

    def remove_student(self, ID):
        pass

    def get_dates_of_rollcall_records(self):
        pass

    def edit_rollcall_record(self):
        # 待定義
        pass

    def get_name(self):
        return self._name
