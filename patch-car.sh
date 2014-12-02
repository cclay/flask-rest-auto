#!/bin/bash

curl -X PATCH -v \
	-H "Content-Type: multipart/form-data" \
	-F "photoupload=@script_photo.jpg"	\
	-F 'json_str={"description":"New Chrome Body, See Picture"}' \
	http://localhost:8080/cars/1

