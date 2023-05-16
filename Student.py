
class Student:

    def __init__(self, name, ID, department):
        self._name = name
        self._ID = ID
        self._department = department

    @property
    def name(self):
        return self._name

    @property
    def ID(self):
        return self._ID

    @property
    def department(self):
        return self._department
