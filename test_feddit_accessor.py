import unittest
from unittest.mock import MagicMock, patch
from feddit_accessor import FedditAccessor

class TestFedditAccessor(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_subfeddit_ids_from_title(self, mock_get):
        accessor = FedditAccessor()
        mock_response = MagicMock()
        mock_response.json.return_value = {'subfeddits': [{'id': 1, 'title': 'Example1'}, {'id': 2, 'title': 'Example2'}]}
        mock_get.return_value = mock_response

        result = accessor.fetch_subfeddit_ids_from_title('Example1')

        self.assertEqual(result, [1])
        mock_get.assert_called_with('http://0.0.0.0:8080/api/v1/subfeddits/?skip=0&limit=10')

    @patch('requests.get')
    def test_get_total_comment_list_for_subfeddit_ids(self, mock_get):
        accessor = FedditAccessor()
        mock_response = MagicMock()
        mock_response.json.return_value = {'comments': [{'id': 1, 'text': 'Comment1'}, {'id': 2, 'text': 'Comment2'}]}
        mock_get.return_value = mock_response

        result = accessor.get_total_comment_list_for_subfeddit_ids([1, 2])

        self.assertEqual(result, [{'id': 1, 'text': 'Comment1'}, {'id': 2, 'text': 'Comment2'}])
        mock_get.assert_called_with('http://0.0.0.0:8080/api/v1/subfeddit/?subfeddit_id=1')

if __name__ == '__main__':
    unittest.main()
