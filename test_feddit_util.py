import unittest
from datetime import datetime
from textblob import TextBlob
from util.feddit_util import FedditUtil

class TestFedditUtil(unittest.TestCase):
    def test_get_polarity_score_positive(self):
        comment = "It looks great!"
        result = FedditUtil.get_polarity_score(comment)
        self.assertEqual(result['classification'], 'Positive')

    def test_get_polarity_score_negative(self):
        comment = "Not good at all."
        result = FedditUtil.get_polarity_score(comment)
        self.assertEqual(result['classification'], 'Negative')

    def test_get_epoch_from_date(self):
        mydate = "2023-12-02"
        result = FedditUtil.get_epoch_from_date(mydate)
        expected_result = int(datetime(2023, 12, 2).timestamp())
        self.assertEqual(result, expected_result)

    def test_select_fields(self):
        input_dict = {'id': 1, 'username': 'user_1', 'text': 'Great!', 'created_at': 1701729843, 'score': 0.8}
        selected_fields = ['id', 'text', 'score']
        result = FedditUtil.select_fields(input_dict, selected_fields)
        expected_result = {'id': 1, 'text': 'Great!', 'score': 0.8}
        self.assertEqual(result, expected_result)

    def test_date_validation_invalid_format(self):
        start = "2023/12/01"
        end = "2023-12-02"
        with self.assertRaises(Exception):
            FedditUtil.date_validation(start, end)

    def test_date_validation_end_greater_than_start(self):
        start = "2023-12-02"
        end = "2023-12-01"
        with self.assertRaises(Exception):
            FedditUtil.date_validation(start, end)

    def test_is_valid_date_valid(self):
        mydate = "2023-12-02"
        format = "%Y-%m-%d"
        result = FedditUtil.is_valid_date(mydate, format)
        self.assertTrue(result)

    def test_is_valid_date_invalid(self):
        mydate = "2023/12/02"
        format = "%Y-%m-%d"
        result = FedditUtil.is_valid_date(mydate, format)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
