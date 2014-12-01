#!/bin/bash

curl -X PUT -v \
	-H "Content-Type: multipart/form-data" \
	-F "photoupload=@script_photo.jpg"	\
	-F 'json_str={"description":"ho","engine":"heya","make":"honda","year":"1990","owner":"hernry"}' \
	http://localhost:8080/cars/1

