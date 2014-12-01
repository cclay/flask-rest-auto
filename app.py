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
api.add_resource(CarList, '/cars')
api.add_resource(Car, '/cars/<string:c_id>')

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
parser.add_argument('picture', type=werkzeug.datastructures.FileStorage,
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
	def get(self, c_id):
		return db[c_id]

	def delete(self, c_id):
		pass

	def put(self, c_id):
		pass

class CarList(Resource):
	def get(self):
		return db

	def post(self):
		args = parser.parse_args()
		for afile in request.files:
			print afile
			dat = request.files['photo'].read()
			request.files['photo'].seek(0)
			print "leno f data is: %d" % (len(dat))
			fil = request.files['photo']
			
			save_file(fil)
			#save_file(fil)

		print "="*10
		
		js_dict = json.loads(args['json_str'])
		print "parse json is"

		js_dict["photo"] = "notset"
		db[c_id] = js_dict
		return db[c_id], 201

def save_file(fil):
	name = fil.filename
	try:
		f = open("./static/images/"+name,"wb")
		f.write(dat)
		f.close()
	except IOError as e:
		print e




if __name__ == '__main__':
	app_port = argv[1] if len(argv) > 1 else 8080
	myapp.run(debug=True,port=int(app_port))