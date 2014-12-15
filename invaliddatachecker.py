__author__ = 'cscharfe'
import json
from jsontextfields import TXT_FIELDS
from requestparser import args_parser

def has_some_valid_fields(dictionary, valid_fields):
    return any([field in valid_fields for field in dictionary])


def has_all_valid_fields(dictionary, valid_fields):
    return all([field in dictionary for field in valid_fields])



class InvalidDataException(Exception):
    pass


class InvalidDataChecker(object):
    def __init__(self, db,  **kwargs):
        self.db = db
        self.args_parser = args_parser
        self.rest_method = None

    def __call__(self, car_method):
        self.rest_method = car_method.__name__
        def wrapped(*args, **kwargs):
            try:
                self.check_data(**kwargs)
            except InvalidDataException as e:
                return e.message, 404
            return car_method(self, **kwargs)
        return wrapped

    def _must_contain_car_id(self, car_id):
        if not self.db.contains(car_id):
            raise InvalidDataException("Invalid car id")

    def _args_must_contain_json_data(self, args):
        if args['json_str'] is None:
            raise InvalidDataException("communicate with json inside field : 'json_str'")

    def _has_photoupload_and_all_valid_fields_in_json_str(self, args, js_dict):
         if not (args['photoupload'] and has_all_valid_fields(js_dict, TXT_FIELDS)):
             raise InvalidDataException("Bad fields in json")

    def _has_no_valid_field(self, js_dict):
        if not has_some_valid_fields(js_dict, TXT_FIELDS):
            raise InvalidDataException("Bad fields in json")

    def check_data(self, car_id=None):
        """wrapper function to handle invalid data sent in
        the REST request, and return an appropriate error response
        based on the type of method used
        """
        args = self.args_parser()  # (json_str : {... }, 'photoupload' : <file>)
        if self.rest_method in ["get", "delete", "put", "patch"]:
            self._must_contain_car_id(car_id)

        if self.rest_method in ["post", "put", "patch"]:
            self._args_must_contain_json_data(args)
            js_dict = json.loads(args['json_str'])

            if self.rest_method in ["post", "put"]:
                self._has_photoupload_and_all_valid_fields_in_json_str(args, js_dict)
            elif self.rest_method == "patch":
                self._has_no_valid_field(js_dict)

