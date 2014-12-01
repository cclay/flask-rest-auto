from flask import Flask, request, send_from_directory
from flask.ext.restful import reqparse, abort, Api, Resource
from sys import argv
import werkzeug
import os
import json


UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
myapp = Flask(__name__)
myapp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api(myapp)

TXT_FIELDS = ["description","engine","make","year","owner"]
#in memory test db
db = {
	'id1': {
			"description":"roadster",
			"engine":"1300",
			"make":"honda",
			"year":"1988",
			"name":"john",
			"photo":"/static/restauto/images/default.jpg"
			},
	'id2': {	"description":"rhog",
			"engine":"1300",
			"make":"honda",
			"year":"1988",
			"name":"john",
			"photo":"/static/restauto/images/default.jpg"
			},

}


parser = reqparse.RequestParser()
parser.add_argument('json_str', type=str)
parser.add_argument('photoupload', type=werkzeug.datastructures.FileStorage,
					location='files')



@myapp.route('/images/<filename>')
def uploaded_file(filename):
	return send_from_directory(myapp.config['UPLOAD_FOLDER'],filename)

@myapp.route('/')
def index():
	ret = "<html>"
	for i in os.environ:
		ret += str(i) + " : " + os.environ[i] 
		ret += "</br>\n"
	ret += "</html>"
	return ret

@myapp.route('/test', methods=[ 'POST', 'PUT', 'GET'])
def tester():
	
	ret = ""
	ret += "\n<br/>method is : %s" % request.method
	ret += "\n<br/>files are : %s" % str(request.files)
	ret += "\n<br/>form are : %s" % str(request.form)
	ret += "\n<br/>json are : %s" % str(request.get_json())
	if len(request.files) > 0:
		ret += '\n<br/>file is : %s' % str(request.files[0])
	ret += "\n<br/> data is: %s" % str(request.data)
	ret += "\n"
	return ret




class Car(Resource):
	def get(self, car_id):
		if not db.has_key("id"+str(car_id)):
			msg = "Invalid car id requested"
			return msg, 404
		return db[c_id]

	def delete(self, car_id):
		pass

	def put(self, car_id):
		pass

class CarList(Resource):
	def get(self):
		return db

	def post(self):
		args = parser.parse_args()  # (json_str : {... }, 'photoupload' : <file>)
		if args['json_str'] == None:
			msg = "communicate with json inside field : 'json_str'"
			return msg,404

		js_dict = json.loads(args['json_str'])
		car_id = len(db) + 1
		if not(args['photoupload'] and has_valid_fields(js_dict,TXT_FIELDS)):
			msg = "Bad fields in json"
			return msg,404

		photo_savepath="not set"
		if request.files.has_key('photoupload'):
			photo_file = request.files['photoupload']
			photo_savepath = "./static/images/"+ photo_file.filename
			save_file(photo_file,photo_savepath)

	
		js_dict["photo"] = photo_savepath[1:] #remove the .
		db[car_id] = js_dict
		return db[car_id], 201



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

def has_valid_fields(field_dictionary,list_of_fields):
	for field in list_of_fields:
		if not field_dictionary.has_key(field):
			return False
	return True

#Add resources after defining above
api.add_resource(CarList, '/cars')
api.add_resource(Car, '/cars/<string:car_id>')

if __name__ == '__main__':
	app_port = argv[1] if len(argv) > 1 else 8080
	myapp.run(debug=True,port=int(app_port))