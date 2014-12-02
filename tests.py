import unittest

from flask import Flask,request
import app
import json
import os



class TestRest(unittest.TestCase):
	def setUp(self):
		
		
		test_data = {
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
		app.db.init_data(test_data)

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
		json_data = json.loads(response.data)
		self.assertEqual(len(json_data),6)

		location = response.headers['Location']
		new_id_num = location.split('/')[-1]
		unique_file_path = json_data["photo"]
		unique_file_name = os.path.basename(unique_file_path)
		id_num_prefix = unique_file_name.split("_")[0]
		self.assertEqual(id_num_prefix,new_id_num)
		

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
		old_item = app.db.get_item(car_id)
		put_filename="test2.jpg"
		test_file = open(put_filename)
		json_str = '{"description":"Silver Shine","engine":"490PR","make":"toyota",\
		"year":"1984","owner":"h.g. wells"}'
		put_data = {'json_str':json_str,'photoupload':test_file}
		path = '/cars/' + str(car_id)
		response = self.test_client.put(path,data=put_data)

		self.assertEqual(response.status_code,200)
		new_item = app.db.get_item(car_id)
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
		put_data = {'json_str':json_str,'photoupload':test_file}
		path = '/cars/' + str(car_id)
		response = self.test_client.put(path,data=put_data)
		self.assertEqual(response.status_code,404)

	def test_put_bad_json_failure(self):
		car_id = "1"
		test_file = open("test.png")
		json_str = '{"description":"Silver Shine"}'
		put_data = {'json_str':json_str,'photoupload':test_file}
		path = '/cars/' + str(car_id)
		response = self.test_client.put(path,data=put_data)
		self.assertEqual(response.status_code,404)

	def test_delete_id(self):
		car_id = "1"
		original_size = app.db.get_size()
		self.assertTrue(app.db.contains(car_id))
		
		path = '/cars/' + car_id
		response = self.test_client.delete(path)
		self.assertEqual(response.status_code,200)
		size_after_delete = app.db.get_size()
		self.assertEqual(original_size - 1, size_after_delete)
		self.assertFalse(app.db.contains(car_id))

	def test_delete_invalid_id(self):
		car_id = "900"
		path = '/cars/' + car_id
		response = self.test_client.delete(path)
		self.assertEqual(response.status_code,404)

		car_id = "myCar"
		path = '/cars/' + car_id
		response = self.test_client.delete(path)
		self.assertEqual(response.status_code,404)

	def test_PATCH_good_json_good_photo(self):
		car_id = "1"
		old_item = app.db.get_item(car_id)
		patch_filename="test2.jpg"
		test_file = open(patch_filename)
		json_str = '{"description":"Newly Done Silver Shine, See Photo"}'
		patch_data = {'json_str':json_str,'photoupload':test_file}
		path = '/cars/' + str(car_id)
		response = self.test_client.patch(path,data=patch_data)

		self.assertEqual(response.status_code,200)
		new_item = app.db.get_item(car_id)

		unchanged_fields = ["engine","make","year","owner"]
		for field in unchanged_fields:
			self.assertEqual(new_item[field],old_item[field])
		
		self.assertNotEqual(new_item["description"],old_item["description"])
		self.assertNotEqual(new_item["photo"],old_item["photo"])

	def test_PATCH_bad_json(self):
		car_id = "1"
		json_str = '{"description":"Updated for 2014: Transmission","wingspan":"20m"}'
		patch_data = {'json_str':json_str,'photoupload':None}
		path = '/cars/' + car_id
		response = self.test_client.put(path,data=patch_data)
		self.assertEqual(response.status_code,404)

if __name__ == '__main__':
	unittest.main()