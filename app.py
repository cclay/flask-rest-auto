from sys import argv
import os
from flask import Flask, request, send_from_directory
from flask_restful import Api, Resource

from dbdata import DB_DATA
from filesavers import save_photoupload
from invaliddatachecker import InvalidDataChecker
from memdatabase import MemDatabase
from requestparser import args_parser, get_json_from_args

UPLOAD_FOLDER = './images'
myapp = Flask(__name__)

api = Api(myapp)
db = MemDatabase()
db.init_data(DB_DATA)


@myapp.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(myapp.config['UPLOAD_FOLDER'], filename)


@myapp.route('/')
def index():
    print myapp.config["SERVER_NAME"]
    ret = "<html>"
    for i in os.environ:
        ret += str(i) + " : " + os.environ[i]
        ret += "</br>\n"
    ret += "</html>"
    return ret


class Car(Resource):
    @InvalidDataChecker(db)
    def get(self, car_id):
        return db.get_item(car_id)

    @InvalidDataChecker(db)
    def delete(self, car_id):
        db.remove_item(car_id)
        return {}, 200

    @InvalidDataChecker(db)
    def put(self, car_id):
        args = args_parser()
        js_dict = get_json_from_args(args)
        js_dict["photo"] = save_photoupload(request, car_id)
        return db.set_item(car_id, js_dict), 200

    @InvalidDataChecker(db)
    def patch(self, car_id):
        args = args_parser()
        js_dict = get_json_from_args(args)
        if args['photoupload']:
            js_dict["photo"] = save_photoupload(request, car_id)

        db.partially_update_item(car_id, js_dict)
        return db.get_item(car_id), 200


class CarList(Resource):
    def get(self):
        return db.get_all_items()

    @InvalidDataChecker(db)
    def post(self):
        args = args_parser()  # (json_str : {... }, 'photoupload' : <file>)
        js_dict = get_json_from_args(args)
        new_car_id = db.add_item(js_dict)
        js_dict["photo"] =save_photoupload(request, new_car_id)
        return db.get_item(new_car_id), 201, {'Location': '/cars/' + str(new_car_id)}


#Add resources after defining above
api.add_resource(CarList, '/cars')
api.add_resource(Car, '/cars/<string:car_id>')

if __name__ == '__main__':
    app_port = argv[1] if len(argv) > 1 else 8080
    myapp.run(debug=True,port=int(app_port))
