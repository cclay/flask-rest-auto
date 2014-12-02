#!/bin/bash

curl -X PUT -v \
	-H "Content-Type: multipart/form-data" \
	-F "photoupload=@script_photo.jpg"	\
	-F 'json_str={"description":"ho","engine":"heya","make":"honda","year":"1990","owner":"hernry"}' \
	http://limitless-coast-3433.herokuapp.com/1

