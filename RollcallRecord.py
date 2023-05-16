
class RollcallRecord:

    def __init__(self, rollcall_result):
        self._attendance_list = rollcall_result

    @property
    def attendance_list(self):
        return self._attendance_list

    def edit(self, student_ID, attend_status):
        self._attendance_list[student_ID] = attend_status
