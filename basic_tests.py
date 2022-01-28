import unittest
from main import open_day
import sms


class BasicTestCases(unittest.TestCase):
    def test_no_open_days(self):
        days = ["50", "50", "50"]
        open_days = []
        available_day = open_day("Test", days, open_days)
        self.assertEqual(available_day, False)

    def test_open_days(self):
        days = ["35", "35", "34"]
        open_days = []
        available_day = open_day("Test", days, open_days)
        self.assertEqual(available_day, True)
        self.assertEqual(len(open_days), 3)

    def test_basic_sms_send(self):
        rv = sms.send("Test message")
        self.assertEqual(rv, True)


if __name__ == '__main__':
    unittest.main()
