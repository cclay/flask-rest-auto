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
						"owner":"john",
						"photo":"/static/restauto/images/default.jpg"
						},
				    "id2":{
						"description":"bent bumper",
						"engine":"rx900",
						"make":"ford",
						"year":"2014",
						"owner":"donald",
						"photo":"/static/restauto/images/default.jpg"
						}
					}

		self.app = app.myapp
		self.test_client = app.myapp.test_client()
		pass

	def tearDown(self):
		pass

	# def testIndex(self):
	# 	r = self.test_client.get('/')

	def test_get(self):
		response = self.test_client.get('/cars')
		json_data = json.loads(response.data)
		self.assertEqual(len(json_data),2)

	def test_get_invalid_car_id(self):
		response = self.test_client.get('/cars/elvis')
		self.assertEqual(response.status_code,404)

	def test_get_out_of_bounds_car_id(self):
		response = self.test_client.get('/cars/-1')
		self.assertEqual(response.status_code,404)

	def test_post_good_json_with_photoupload(self):
		test_file = open("./test.png")
		json_str = '{"description":"Silver Shine","engine":"490PR","make":"toyota",\
		"year":"1984","owner":"h.g. wells"}'
		post_data = {'json_str':json_str,'photoupload':test_file}
		response = self.test_client.post('/cars',data=post_data)
		# print response.data
		self.assertEqual(response.status_code,201)
		

	def test_post_bad_json(self):
		json_str = '{"descrippption":"rusty","enge":"490PR","makr":"toyota",\
		"yer":"1984","ownnner":"h.g. wells"}'
		post_data = {'json_str':json_str}
		response = self.test_client.post('/cars',data=post_data)
		self.assertEqual(response.status_code,404)
		

	def test_post_no_photo(self):
		json_str = '{"description":"rusty","engine":"490PR","make":"toyota",\
		"year":"1984","owner":"h.g. wells"}'
		post_data = {'json_str':json_str}
		response = self.test_client.post('/cars',data=post_data)
		self.assertEqual(response.status_code,404)
		


if __name__ == '__main__':
	unittest.main()