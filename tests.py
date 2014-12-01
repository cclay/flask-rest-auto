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
						"photo":"/static/images/default.jpg"
						},
				    "id2":{
						"description":"bent bumper",
						"engine":"rx900",
						"make":"ford",
						"year":"2014",
						"owner":"donald",
						"photo":"/static/images/default.jpg"
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

	def test_get_single(self):
		car_id = "1"
		path = '/cars/' + car_id
		response = self.test_client.get(path)
		json_data = json.loads(response.data)
		self.assertEqual(len(json_data),6)
		
		for field in app.TXT_FIELDS:
			self.assertTrue(json_data.has_key(field))
		self.assertTrue(json_data.has_key("photo"))

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
		

	def test_put_good_json_good_photo(self):
		car_id = "1"
		old_item = app.db["id"+car_id]
		put_filename="test2.jpg"
		test_file = open(put_filename)
		json_str = '{"description":"Silver Shine","engine":"490PR","make":"toyota",\
		"year":"1984","owner":"h.g. wells"}'
		post_data = {'json_str':json_str,'photoupload':test_file}
		path = '/cars/' + str(car_id)
		response = self.test_client.put(path,data=post_data)

		self.assertEqual(response.status_code,200)
		new_item = app.db["id"+car_id]
		self.assertEqual(old_item["description"], "timecar")
		self.assertEqual(old_item["engine"], "333")
		self.assertEqual(old_item["make"], "delorian")
		self.assertEqual(old_item["year"], "1900")
		self.assertEqual(old_item["owner"], "john")
		self.assertEqual(old_item["photo"], "/static/images/default.jpg")

		self.assertEqual(new_item["description"], "Silver Shine")
		self.assertEqual(new_item["engine"], "490PR")
		self.assertEqual(new_item["make"], "toyota")
		generated_filename = car_id + "_" + put_filename
		self.assertEqual(new_item["photo"], 
			"/static/images/" + generated_filename)


	def test_put_good_json_no_photo_failure(self):
		car_id = "1"
		test_file = None
		json_str = '{"description":"Silver Shine","engine":"490PR","make":"toyota",\
		"year":"1984","owner":"h.g. wells"}'
		post_data = {'json_str':json_str,'photoupload':test_file}
		path = '/cars/' + str(car_id)
		response = self.test_client.put(path,data=post_data)
		self.assertEqual(response.status_code,404)

	def test_put_bad_json_failure(self):
		car_id = "1"
		test_file = open("test.png")
		json_str = '{"description":"Silver Shine"}'
		post_data = {'json_str':json_str,'photoupload':test_file}
		path = '/cars/' + str(car_id)
		response = self.test_client.put(path,data=post_data)
		self.assertEqual(response.status_code,404)




if __name__ == '__main__':
	unittest.main()