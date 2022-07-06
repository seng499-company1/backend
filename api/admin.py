'''
contains all functions for /admins endpoints
'''
import json
from flask import Blueprint, request
from .dbconn import DB_CONN

ADMIN_BP = Blueprint('admin', __name__)


@ADMIN_BP.route('/hello/')
def hello():
    '''
    says hello
    '''
    return "Hello from Admins", 200
ADMINS = [
    {'uuid': 'd86a6640-d267-42f0-9dcd-8c0d06bf884c', 'first_name': 'Rich', 'last_name': 'Little',
     'email': 'richlittle@uvic.ca'},
    {'uuid': 'ace7c38c-a6dd-467a-b73f-aaaafe9a38b2', 'first_name': 'Dan', 'last_name': 'Mai',
     'email': 'danmai@uvic.ca'}
]
UUIDS = [admin['uuid'] for admin in ADMINS]

@ADMIN_BP.route('/', methods=['GET'])
def get_all_admins():
    '''
    returns all ADMINS and their URIs
    '''
    sql = """SELECT BIN_TO_UUID(id) as id,
                first_name, 
                last_name, 
                email FROM Admin;"""
    results = DB_CONN.select(sql)
    return results, 200

@ADMIN_BP.route('/<admin_id>', methods=['GET'])
def get_admin(admin_id):
    '''
    returns a specific admin's account information
    '''
    sql = f"""SELECT BIN_TO_UUID(id) as id,
                    first_name, 
                    last_name, 
                    email FROM Admin WHERE BIN_TO_UUID(id) = \'{admin_id}\'"""
    result = DB_CONN.select_one(sql)
    if result is None:
        # if empty string - admin not found
        return 'Not Found', 404
    # return 200 OK
    return json.loads(result.response[0]), 200

@ADMIN_BP.route('/', methods=['POST'])
def post_admin():
    '''
    posts a new admin
    '''
    data = request.json
    uuid = DB_CONN.uuid()
    sql = f"""INSERT INTO Admin Values(UUID_TO_BIN(\"{uuid}\"),
                                           \"{data['first_name']}\",
                                           \"{data['last_name']}\",
                                           \"{data['email']}\");"""
    if not DB_CONN.execute(sql):
        return 'Error adding admin', 500
    return uuid, 200

@ADMIN_BP.route('/<admin_id>', methods=['DELETE'])
def delete_admin(admin_id):
    '''
    deletes an admin from the admin table
    '''
    sql = f"""DELETE FROM Admin WHERE BIN_TO_UUID(id) = \'{admin_id}\'"""
    if not DB_CONN.execute(sql):
        return f'Unable to delete prof with id {admin_id}', 500

    return f'Deleted admin with id {admin_id}', 200
