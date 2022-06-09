'''Import py requests to support api requests'''
import requests

SERVICE_URL = "http://127.0.0.1:5000/courses/"

def test_course_hello():
    '''Tests hello endpoint of course service.'''
    endpoint = "hello"
    response = requests.get(url=SERVICE_URL+endpoint)
    assert response.status_code == 200
    assert response.text == "Hello from Courses"
   