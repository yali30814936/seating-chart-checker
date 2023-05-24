from src.IdentifyModule import check_rollcall
import csv
from unittest import TestCase
import logging
import unittest

class TestIdentifyModule(TestCase):
    def test_check_rollcall(self):
        """Test check_rollcall()
        """
        dir = "resource/TestCase/1/"
        for i in range(1, 4):
            with self.subTest(f"IdTest_1-{i}"):
                with open(f"{dir}{i}.csv", encoding='utf-8') as fp:
                    # Load test data
                    rows = csv.reader(fp)
                    stu_list = []
                    expected = {}
                    for row in rows:
                        stu_list.append(row[0])
                        expected[row[0]] = int(row[1])
                    # Testing
                    result = check_rollcall(f"{dir}{i}.jpg", stu_list)
                    self.assertDictEqual(result, expected)
                    
    def test_check_rollcall_recall(self):
        """Test check_rollcall()
           testing with recall method
        """
        # logger = logging.getLogger(__name__)
        # logger.setLevel(logging.INFO)
        dir = "resource/TestCase/2/"
        for i in range(1, 13):
            with self.subTest(f"IdTest_1-{i}"):
                with open(f"{dir}{i}.csv", encoding='utf-8') as file:
                    # Load test data
                    rows = csv.reader(file)
                    stu_list = []
                    expected = {}
                    for row in rows:
                        stu_list.append(row[0])
                        expected[row[0]] = int(row[1])
                    # Testing
                    result = check_rollcall(f"{dir}{i}.jpg", stu_list)
                    sz = len(expected)
                    tp, tn, fp, fn = 0, 0, 0, 0
                    for [rk, rv], [ek, ev] in zip(result.items(), expected.items()):
                        if rv == ev:
                            if rv == 1:
                                tp += 1
                            else:
                                tn += 1
                        else:
                            if rv == 1:
                                fp += 1
                            else:
                                fn += 1
                    logging.warning(f"IdTest_2-{i}: Recall = {tp}/{tp}+{fn} = {tp/(tp+fn)}")
                    # logging.warning(f"IdTest_1-{i}: False Recall = {tn}/{tn}+{fp} = {tn/(tn+fp)}")
                    # self.assertDictEqual(result, expected)
# if __name__ == '__main__':
#     # DEBUG for demonstration purposes, but you could set the level from
#     # cmdline args to whatever you like
#     logging.basicConfig(level=logging.DEBUG, format='%(name)s %(levelname)s %(message)s')
#     unittest.main()