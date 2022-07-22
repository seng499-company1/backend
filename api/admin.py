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

    if isinstance(results, str):
        return results, 400

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

    if isinstance(result, str):
        return result, 400

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
    result = DB_CONN.execute(sql)

    if isinstance(result, str):
        return result, 400

    if not result:
        return 'Error adding admin', 500

    return uuid, 200

@ADMIN_BP.route('/<admin_id>', methods=['DELETE'])
def delete_admin(admin_id):
    '''
    deletes an admin from the admin table
    '''
    sql = f"""DELETE FROM Admin WHERE BIN_TO_UUID(id) = \'{admin_id}\'"""
    result = DB_CONN.execute(sql)

    if isinstance(result, str):
        return result, 400

    if not result:
        return f'Unable to delete admin with id {admin_id}', 500

    return f'Deleted admin with id {admin_id}', 200
