import unittest

from flask import Flask,request
import app
import json




class TestGet(unittest.TestCase):
	def setUp(self):
		
		app.db = {
				  "id1":{
						"description":"timecar",
						"engine":"333",
						"make":"delorian",
						"year":"1900",
						"name":"john",
						"photo":"/static/restauto/images/default.jpg"
						},
				    "id2":{
						"description":"bent bumper",
						"engine":"rx900",
						"make":"ford",
						"year":"2014",
						"name":"donald",
						"photo":"/static/restauto/images/default.jpg"
						}
					}

		self.app = app.myapp
		self.test_client = app.myapp.test_client()
		pass

	def tearDown(self):
		pass

	def testIndex(self):
		r = self.test_client.get('/')

	def test_get(self):
		resp = self.test_client.get('/cars')
		json_data = json.loads(resp.data)
		self.assertEqual(len(json_data),2)


	def test_post(self):
		pass


if __name__ == '__main__':
	unittest.main()