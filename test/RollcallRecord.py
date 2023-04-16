
class RollcallRecord:

    def __init__(self, date, rollcall_result):
        self._date = date
        self._attendance = rollcall_result

    def edit(self, student_ID, attend_status):
        self._attendance[student_ID] = attend_status
