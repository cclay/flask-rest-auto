__author__ = 'cscharfe'

from unittest import TestCase
from mock import patch, Mock, ANY, call
import app
import werkzeug


class ParseArgsTests(TestCase):
    @patch('requestparser.RequestParser')
    def test_can_parse_args_from_request(self, RequestParser):
        request_parser_mock = Mock()
        RequestParser.return_value = request_parser_mock
        self.app = app.myapp
        self.test_client = app.myapp.test_client()
        self.test_client.get('/cars/1')
        calls = [
            call('json_str', type=str),
            call('photoupload', type=werkzeug.datastructures.FileStorage, location='files')
        ]
        request_parser_mock.add_argument.assert_has_calls(calls)
        request_parser_mock.parse_args.assert_called_with()
