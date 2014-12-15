__author__ = 'cscharfe'

from unittest import TestCase
import json
from mock import patch

from invaliddatachecker import has_some_valid_fields, has_all_valid_fields, InvalidDataException
import app
from memdatabase import MemDatabase
from dbdata import DB_DATA as TEST_DB_DATA


class InvalidDataCheckerHelperFunctionsTestCase(TestCase):
    def test_has_some_valid_fields_validates_dictionary_against_list_of_fields(self):
        valid_fields = ["engine", "make"]

        self.assertTrue(has_some_valid_fields({ "engine": "V8"}, valid_fields))
        self.assertTrue(has_some_valid_fields({ "make": "toyota"}, valid_fields))
        self.assertFalse(has_some_valid_fields({"unknown_field": "value"}, valid_fields))

    def test_has_all_valid_fields_validates_dictionary_against_list_of_fields(self):
        valid_fields = ["engine", "make"]

        self.assertTrue(has_all_valid_fields({"engine": "V8", "make": "honda"}, valid_fields))
        self.assertFalse(has_all_valid_fields({"engine": "v8"}, valid_fields))
        self.assertFalse(has_all_valid_fields({"unknown_field": "value"}, valid_fields))


class InvalidDataCheckerUnitTests(TestCase):
    def setUp(self):
        from invaliddatachecker import InvalidDataChecker
        db = MemDatabase()
        db.init_data(TEST_DB_DATA)
        self.invalid_data_checker = InvalidDataChecker(db)

    def test_can_check_incoming_data_with_no_car_id_and_raises_exception(self):
        def dummy_args_parser():
            return {}

        self.invalid_data_checker.args_parser = dummy_args_parser
        self.invalid_data_checker.rest_method = 'get'
        self.assertRaises( InvalidDataException, self.invalid_data_checker.check_data)

    def test_can_check_incoming_data_for_invalid_car_id_and_raises_exception(self):
        def dummy_args_parser():
            return {}
        self.invalid_data_checker.args_parser = dummy_args_parser
        self.invalid_data_checker.rest_method = 'get'

        self.assertRaises(InvalidDataException, self.invalid_data_checker.check_data,  "-1")
        self.assertRaises(InvalidDataException, self.invalid_data_checker.check_data, "word_id")

    def test_can_check_incoming_data_for_valid_car_id_throws_no_error(self):
        def dummy_args_parser():
            return {}
        self.invalid_data_checker.args_parser = dummy_args_parser
        self.invalid_data_checker.rest_method = 'get'

        self.invalid_data_checker.check_data(1)

    def test_can_check_incoming_data_for_post_with_bad_json_str_and_raises_error(self):
        def dummy_args_parser():
            return {"json_str": None}
        self.invalid_data_checker.args_parser = dummy_args_parser
        self.invalid_data_checker.rest_method = 'post'

        self.assertRaises(InvalidDataException, self.invalid_data_checker.check_data, "1")

    def test_can_check_incoming_data_for_post_with_existing_json_str_bad_photo_and_raise_error(self):
        def dummy_args_parser():
            return {"json_str": '{"description": "roadster"} ', "photoupload": None}
        self.invalid_data_checker.args_parser = dummy_args_parser
        self.invalid_data_checker.rest_method = 'post'

        self.assertRaises(InvalidDataException, self.invalid_data_checker.check_data, "1")

    def test_can_check_incoming_data_for_post_with_good_json_str_good_photo_is_success(self):
        def dummy_args_parser():
            return {"json_str": '{"description": "roadster", \
            "engine": "v8", "make": "toyota", "year": "1999", "owner":"joe"} ',
            "photoupload": "dummy_data_value"}
        self.invalid_data_checker.args_parser = dummy_args_parser
        self.invalid_data_checker.rest_method = 'post'

        self.invalid_data_checker.check_data("1")


    def test_can_check_incoming_data_for_patch_with_no_valid_fields_raise_error(self):
        def dummy_args_parser():
            return {"json_str": '{"unknown_description_key":"test value"}'}
        self.invalid_data_checker.args_parser = dummy_args_parser
        self.invalid_data_checker.rest_method = 'patch'

        self.assertRaises(InvalidDataException, self.invalid_data_checker.check_data, "1")