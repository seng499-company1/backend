import json
import requests
import jsonpath

SERVICE_URL = "http://127.0.0.1:5000/schedule/"

def test_schedule_hello():
    '''Tests hello endpoint of schedule service.'''
    endpoint = "hello"
    response = requests.get(url=SERVICE_URL+endpoint)
    assert response.status_code == 200
    assert response.text == "Hello from Schedules"
    