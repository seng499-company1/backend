'''
Import json to assert json responses
Import requests to support api requests
'''
import json
import requests
from ...api import admin

SERVICE_URL = "http://127.0.0.1:5000/admins/"

def test_admin_hello():
    '''Tests hello endpoint of admins service.'''
    endpoint = "hello"
    response = requests.get(url=SERVICE_URL+endpoint)
    assert response.status_code == 200
    assert response.text == "Hello from Admins"

def test_get_all_admins():
    '''Tests Get All Admins endpoint of admins service.'''
    endpoint = ""
    response = requests.get(url=SERVICE_URL+endpoint)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json == admin.ADMINS

def test_get_admin_valid():
    '''Tests Get Admin endpoint of admins service with valid id.'''
    endpoint = ""
    admin_id = 'd86a6640-d267-42f0-9dcd-8c0d06bf884c'
    response = requests.get(url=SERVICE_URL+endpoint+admin_id)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json == admin.ADMINS[admin.UUIDS.index(admin_id)]

def test_get_admin_invalid():
    '''Tests Get Admin endpoint of admins service with invalid id.'''
    endpoint = ""
    admin_id = 'invalid-id'
    response = requests.get(url=SERVICE_URL+endpoint+admin_id)
    assert response.status_code == 404
    assert response.text == 'id not valid'

def test_post_admin():
    '''Tests Post Admin endpoint of admins service.'''
    endpoint = ""
    response = requests.post(url=SERVICE_URL+endpoint)
    assert response.status_code == 200
    assert response.text == 'added user '

def test_delete_admin():
    '''Tests Delete Admin endpoint of admins service.'''
    endpoint = ""
    admin_id = 'd86a6640-d267-42f0-9dcd-8c0d06bf884c'
    response = requests.delete(url=SERVICE_URL+endpoint+admin_id)
    assert response.status_code == 200
    assert response.text == f'deleted user with id {admin_id}'
