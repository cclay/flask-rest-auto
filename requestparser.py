__author__ = 'cscharfe'
import werkzeug
from flask_restful import reqparse
import json

def args_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('json_str', type=str)
    parser.add_argument('photoupload', type=werkzeug.datastructures.FileStorage,
                        location='files')
    return parser.parse_args()


def get_json_from_args(args):
    return json.loads(args['json_str'])