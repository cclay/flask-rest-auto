#!/bin/bash

curl -X POST -v \
	-H "Content-Type: multipart/form-data" \
	-F "photoupload=@c6.jpg"	\
	-F 'json_str={"description":"ho","engine":"heya","make":"honda","year":"1990","owner":"hernry"}' \
	http://localhost:8080/cars

