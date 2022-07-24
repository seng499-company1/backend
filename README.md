# backend

## Docker
**To run entire Backend Server:**
- Ensure pwd is backend root (backend/)
- On your terminal run

To build docker images for web and database
```
docker-compose build
```

To create and start web and database containers in detached mode (run in background)
```
docker-compose up -d
```

Expected:
- app should now be hosted [here](http://127.0.0.1:5000/)
- should see `all is good :)` if running successfully

Current Endpoints are:
- http://127.0.0.1:5000/courses/hello/
- http://127.0.0.1:5000/professors/hello/
- http://127.0.0.1:5000/schedule/hello/
- http://127.0.0.1:5000/admins/hello/


To stop services:
```
docker-compose stop
```

**To run just the Web App (API):**
- Ensure pwd is backend root (backend/)
- On your terminal run

To build image
```
docker build --tag api .
```

To run container
```
docker run -p 5000:5000 api
```

To run container in detached mode (run in background)
```
docker run -d -p 5000:5000 api
```

To view running containers
```
docker ps
```
To stop container
```
docker stop <container_id>
```


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
as the image for the container is not deleted. This means that the container can be started and stopped without any loss of data. To build and run the database along with the rest of the backend server, see *Docker* section.

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

## Performance Testing
The peformance testing plan was built using the JMeter platform GUI. The performance test files are located in the [/tests/performance] directory. To run the performance tests, you will need to:

- Install JMeter binaries on your device, available at [https://jmeter.apache.org/download_jmeter.cgi] .
- Extract the files from the downloaded compressed file, tgz or zip.
- Navigate to the \bin\ directory within the extracted jmeter folder.
- Run jmeter.bat for Windows and jmeter.sh for UNIX based systems.
- Once GUI is open, copy files in [/tests/performance] over to the [bin\] folder.
- In JMeter GUI, click file > open and select either of your just copied files.
- Once test plan is open, open the thread group dropdown (Prof. Group or Admin Group).
- Click `Immortal Minds Server` and change the value of `Server Name` to the target server.
- Save test plan.
- Click start button.

NOTE: The requests sent during this test actually populate the database and there is currently no automated method to clean-up after the test. To prevent unwanted behavior from your server, make sure to manually delete all newly added data from the test. Variables are defined in the test plan.