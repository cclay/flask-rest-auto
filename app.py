from sys import argv
import werkzeug
import os
import json
from flask import Flask, request, send_from_directory
from flask_restful import reqparse, Api, Resource

from memdatabase import MemDatabase
from dbdata import DB_DATA
from invaliddatachecker import InvalidDataChecker
from jsontextfields import TXT_FIELDS

UPLOAD_FOLDER = './images'
myapp = Flask(__name__)

api = Api(myapp)




db = MemDatabase()
db.init_data(DB_DATA)

parser = reqparse.RequestParser()
parser.add_argument('json_str', type=str)
parser.add_argument('photoupload', type=werkzeug.datastructures.FileStorage,
                    location='files')


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
    @InvalidDataChecker(db, parser)
    def get(self, car_id):
        return db.get_item(car_id)

    @InvalidDataChecker(db, parser)
    def delete(self, car_id):
        db.remove_item(car_id)
        return {}, 200

    @InvalidDataChecker(db, parser)
    def put(self, car_id):

        args = parser.parse_args()
        js_dict = json.loads(args['json_str'])
        photo_savepath = save_photoupload(request, car_id)
        js_dict["photo"] = photo_savepath[1:]  #remove the .

        new_item = db.set_item(car_id, js_dict)

        return new_item, 200

    @InvalidDataChecker(db, parser)
    def patch(self, car_id):
        args = parser.parse_args()
        js_dict = json.loads(args['json_str'])

        if args['photoupload']:
            photo_savepath = save_photoupload(request, car_id)
            js_dict["photo"] = photo_savepath[1:]  #remove the .

        db.partially_update_item(car_id, js_dict)
        patched_item = db.get_item(car_id)
        return patched_item, 200


class CarList(Resource):
    def get(self):
        return db.get_all_items()

    @InvalidDataChecker(db, parser)
    def post(self):
        args = parser.parse_args()  # (json_str : {... }, 'photoupload' : <file>)
        js_dict = json.loads(args['json_str'])

        new_car_id = db.add_item(js_dict)
        photo_savepath = save_photoupload(request, new_car_id)
        js_dict["photo"] = photo_savepath[1:]  #remove the .
        new_item = db.get_item(new_car_id)
        return new_item, 201, {'Location': '/cars/' + str(new_car_id)}


def save_photoupload(request, car_id):
    photo_savepath = "not set"
    if request.files.has_key('photoupload'):
        photo_file = request.files['photoupload']
        unique_filename = get_clean_filename(photo_file.filename, car_id)
        photo_savepath = "./static/images/" + unique_filename
        save_file(photo_file, photo_savepath)
    return photo_savepath


def get_clean_filename(filename, car_id):
    name = filename.replace("../", "").replace("./", "")
    return str(car_id) + "_" + name


def save_file(fil, path):
    data = fil.read()
    try:
        path = path.encode('ascii', 'ignore')
        f = open(path, "wb")
        f.write(data)
        f.close()
        return path
    except IOError as e:
        print e
        return ""


def save_photoupload(request,car_id):
	photo_savepath="not set"
	if request.files.has_key('photoupload'):
		photo_file = request.files['photoupload']
		unique_filename = get_clean_filename(photo_file.filename,car_id)
		photo_savepath = "./static/images/"+ unique_filename
		save_file(photo_file,photo_savepath)
	return photo_savepath

def get_clean_filename(filename,car_id):
	name = filename.replace("../","").replace("./","")
	return str(car_id) + "_" + name

def save_file(fil,path):
	data = fil.read()
	try:
		path = path.encode('ascii','ignore')
		f = open(path,"wb")
		f.write(data)
		f.close()
		return path
	except IOError as e:
		print e
		return ""



#Add resources after defining above
api.add_resource(CarList, '/cars')
api.add_resource(Car, '/cars/<string:car_id>')

if __name__ == '__main__':
	app_port = argv[1] if len(argv) > 1 else 8080
	myapp.run(debug=True,port=int(app_port))
