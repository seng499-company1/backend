# backend

## API
To  run API locally:
- Navigate the api directory
- On your terminal run

For Linux/Mac users:
```
export FLASK_APP=app
flask run
```
For Windows users:
```
set FLASK_APP=app
python -m flask run
```
- app should now be hosted [here](http://127.0.0.1:5000/)
- should see `all is good :)` if running successfully

Current Endpoints are:
- http://127.0.0.1:5000/courses/hello/
- http://127.0.0.1:5000/professors/hello/
- http://127.0.0.1:5000/schedule/hello/
- http://127.0.0.1:5000/admins/hello/

## Database
The database is a mysql database built using docker. The data for the database is stored inside the docker image however, the data will be persistent as long 
as the image for the container is not deleted. This means that the container can be started and stopped without any loss of data. To build a docker image for
the database (and hopefully later the entire backend) run 

```
$ docker-compose build
```

To start the mysql docker container in the background (and hopefully later the entire backend) run

```
$ docker-compose up -d
```

Note: If the container is being started for the first time scripts in [/database/sql/](/database/sql/) will be run in alphabetical order to create and initialize the database. 

## Testing
The test suite is located under the /tests directory of the project. To run the test cases, first install dependencies by either running:

```
$ pip install -r requirements.txt
```

OR by doing separate installs via

```
$ pip install pytest
$ pip install requests
```

Next, start the flask app by following the instructions under API section and then simply run the `pytest` from the repo root to run all tests. See pytest documentation for other test configurations.
