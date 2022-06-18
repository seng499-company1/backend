'''
Import json to assert json responses
Import requests to support api requests
'''
import json
import requests
from ...api import professor

SERVICE_URL = "http://127.0.0.1:5000/professors/"

def test_schedule_hello():
    '''Tests hello endpoint of professors service.'''
    endpoint = "hello"
    response = requests.get(url=SERVICE_URL+endpoint)
    assert response.status_code == 200
    assert response.text == "Hello from Professors"

def test_get_all_professors():
    '''Tests Get All Professors endpoint of professors service.'''
    endpoint = ""
    response = requests.get(url=SERVICE_URL+endpoint)
#   response_json = json.loads(response.text)
    assert response.status_code == 200
#   assert response_json == professor.PROFESSORS

def test_get_professor():
    '''Tests Get Professor endpoint of professors service.'''
    endpoint = ""
    professor_id = '0e90ab30-c380-4034-acdb-238856a88df3'
    response = requests.get(url=SERVICE_URL+endpoint+professor_id)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json == professor.PROFESSORS[professor.UUIDS.index(professor_id)]

def test_get_professor_preferences():
    '''Tests Get Professor Preferences endpoint of professors service.'''
    endpoint = "/preferences"
    professor_id = '0e90ab30-c380-4034-acdb-238856a88df3'
    response = requests.get(url=SERVICE_URL+professor_id+endpoint)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json == professor.RELIEFS[professor.UUIDS.index(professor_id)]

def test_get_professor_preference_valid():
    '''Tests Get Professor Preference endpoint of professors service with valid preference id.'''
    endpoint = "/preferences/"
    professor_id = '0e90ab30-c380-4034-acdb-238856a88df3'
    preference_id = 1
    response = requests.get(url=SERVICE_URL+professor_id+endpoint+str(preference_id))
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json == professor.RELIEFS[professor.UUIDS.index(professor_id)]

def test_get_professor_preference_invalid():
    '''Tests Get Professor Preference endpoint of professors service with invalid preference id.'''
    endpoint = "/preferences/"
    professor_id = '0e90ab30-c380-4034-acdb-238856a88df3'
    preference_id = 4
    response = requests.get(url=SERVICE_URL+professor_id+endpoint+str(preference_id))
    assert response.status_code == 404
    assert response.text == 'couldn\'t find that preference id'

def test_post_professor():
    '''Tests Post Professor endpoint of professors service.'''
    endpoint = ""
    payload = '{"first_name":"Mr", "last_name":"Engineer", "is_peng":true, "is_teaching":true, "email":"email@uvic.ca", "department":"ECE" }'
    response = requests.post(url=SERVICE_URL+endpoint, data=payload)
    assert response.status_code == 200
    assert response.text == 'posted a professor'

def test_post_professor_preferences():
    '''Tests Post Professor Preferences endpoint of professors service.'''
    endpoint = "/preferences"
    professor_id = '0e90ab30-c380-4034-acdb-238856a88df3'
    response = requests.post(url=SERVICE_URL+professor_id+endpoint)
    assert response.status_code == 200
    assert response.text == f'updates a prof with professor_id {professor_id}'

def test_update_professor_preferences():
    '''Tests Update Professor Preferences of professors service.'''
    endpoint = "/preferences/"
    professor_id = '0e90ab30-c380-4034-acdb-238856a88df3'
    preference_id = 1
    response = requests.put(url=SERVICE_URL+professor_id+endpoint+str(preference_id))
    assert response.status_code == 200
    assert response.text == f'updates the preferences with id {preference_id} for \
     professor with id {professor_id}'

def test_delete_professor():
    '''Tests Delete Professor of professors service.'''
    endpoint = ""
    professor_id = '0e90ab30-c380-4034-acdb-238856a88df3'
    response = requests.delete(url=SERVICE_URL+endpoint+professor_id)
    assert response.status_code == 200
    assert response.text == f'deleted prof with id {professor_id}'

def test_delete_professor_preferences():
    '''Tests Delete Professor Preferences endpoint of professors service.'''
    endpoint = "/preferences/"
    professor_id = '0e90ab30-c380-4034-acdb-238856a88df3'
    preference_id = 1
    response = requests.delete(url=SERVICE_URL+professor_id+endpoint+str(preference_id))
    assert response.status_code == 200
    assert response.text == f'deleted preference with id {preference_id} for \
     professor with id {professor_id}'
