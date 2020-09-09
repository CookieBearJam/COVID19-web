from django.test import TestCase

import unittest

from hospital.views import parse_file


class ParseFileTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_file(self):
        filepath = "static/upload/patient_test2.xlsx"
        self.assertEqual(parse_file(filepath), True)

    # def test_save_patient(self):
    #     self.assertEqual(save)

if __name__ == '__main__':
    unittest.main()
