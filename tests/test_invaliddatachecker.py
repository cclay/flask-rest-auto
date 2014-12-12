__author__ = 'cscharfe'

from unittest import TestCase
from invaliddatachecker import has_all_valid_fields, has_valid_fields

class InvalidDataCheckerTestCase(TestCase):
    def test_has_valid_fields_validates_dictionary_against_list_of_fields(self):
        valid_fields = ["engine", "make"]

        self.assertTrue(has_valid_fields({ "engine": "V8"}, valid_fields))
        self.assertTrue(has_valid_fields({ "make": "toyota"}, valid_fields))
        self.assertFalse(has_valid_fields({"unknown_field": "value"}, valid_fields))

    def test_has_all_valid_fields_validates_dictionary_against_list_of_fields(self):
        valid_fields = ["engine", "make"]

        self.assertTrue(has_all_valid_fields({"engine": "V8", "make": "honda"}, valid_fields))

        self.assertFalse(has_all_valid_fields({"engine": "v8"}, valid_fields))
        self.assertFalse(has_all_valid_fields({"unknown_field": "value"}, valid_fields))