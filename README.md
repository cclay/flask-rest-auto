
# Car REST service


python flask-restful app to deliver info about cars with the following specs:
 - description
 - engine (cylindree)
 - make (mark)
 - year (annee)
 - owner (nom du proprietaire)
 - photo (photo de la voiture)

API supports GET,POST,PUT,DELETE, and PATCH

### json structure for curl:
```sh
{"json_str":{
        "description":"timecar",
      "engine":"333",
      "make":"delorian",
      "year":"1900",
      "owner":"john",
      },
 "photoupload": <Binary data>
 }
```

###testing http server with curl
There is a server running at http://limitless-coast-3433.herokuapp.com/
the rest endpoint is at http://limitless-coast-3433.herokuapp.com/cars

To test out the REST-api on the heroku server, use the scripts inside the heroku_curl_tests folder
 ```sh
    $ ./heroku_curl_tests/get-car.sh
    $ ./heroku_curl_tests/post-car.sh
    **see post results**
    $ ./heroku_curl_tests/get-car.sh
 ```

###accessing photo data
The photo value is reachable by appending to the root site:
so with an example item with json:
```sh
{"name": "john", "photo": "/static/images/default.jpg", "year": "1988", "description": "roadster", "make": "honda", "engine": "1300"}
  ```
The photo would be accessible via a static folder at:
```sh
http://limitless-coast-3433.herokuapp.com/static/images/default.jpg
```

###python testing
tests are located in the tests.py file
```sh
    $ python tests.py
```

### Setting up to run locally
Clone, Install requirements into a virtualenv, then run:

```sh
  $ mkdir rest-auto && cd rest-auto
  $ git clone git@github.com:cclay/flask-rest-auto.git .
  $ virtualenv env
  $ source env/bin/activate
  $ pip install -r requirements.txt
  $ python app.py
  $ deactivate # Stop virtualenv when you are done
```