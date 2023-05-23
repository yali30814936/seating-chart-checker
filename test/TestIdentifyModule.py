from src.IdentifyModule import check_rollcall
import csv
from unittest import TestCase
import unittest

class TestIdentifyModule(TestCase):
    def test_check_rollcall(self, sub="1"):
        """Test check_rollcall()
        """
        dir = "resource/TestCase/2/"
        with open(f"{dir}{sub}.csv", encoding='utf-8') as fp:
            # Load test data
            rows = csv.reader(fp)
            stu_list = []
            expected = {}
            for row in rows:
                stu_list.append(row[0])
                expected[row[0]] = int(row[1])
            # Testing
            result = check_rollcall(f"{dir}{sub}.jpg", stu_list)
            self.assertDictEqual(result, expected)
            
def _add_test(name):
    def test_method(self):
        self.test_check_rollcall(name)
    setattr(TestIdentifyModule, 'test_' + name, test_method)
    test_method.__name__ = 'test_' + name
    
for i in range(2, 4):
    _add_test(str(i))