#!/bin/bash

curl -X PATCH -v \
	-H "Content-Type: multipart/form-data" \
	-F "photoupload=@script_photo.jpg"	\
	-F 'json_str={"description":"New Chrome Body, See Picture"}' \
	http://limitless-coast-3433.herokuapp.com/1

