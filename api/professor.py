'''
contains all API /professors endpoints
'''
import json
from flask import Blueprint, jsonify, request
from .dbconn import DB_CONN
from .preference import PREFERENCE_BP

PROFESSOR_BP = Blueprint('professor', __name__)
PROFESSOR_BP.register_blueprint(PREFERENCE_BP, url_prefix='')
@PROFESSOR_BP.route('/hello/')
def hello():
    '''
    blah
    '''
    return "Hello from Professors"
PROFESSORS = [
    {'first_name':'Celina', 'last_name':'Berg', 'uuid':'0e90ab30-c380-4034-acdb-238856a88df3',
     'department':'CSC', 'is_teaching':True, 'email':'email@uvic.ca'},
    {'first_name':'Bill', 'last_name':'Bird', 'uuid':'8b8829ec-4615-4708-a0cd-5103f080ae56',
     'department':'CSC', 'is_teaching':True, 'email':'email@uvic.ca'},
    {'first_name':'Anthony', 'last_name':'Estey', 'uuid':'6e46c60b-6709-4af5-ab4e-7a1c89c8ae0b',
     'department':'CSC', 'is_teaching':True, 'email':'email@uvic.ca'},
]
RELIEFS = [
    {'prof_id':'0e90ab30-c380-4034-acdb-238856a88df3', 'id':1, 'year':2022, 'num_relief': 2,
     'num_summer_courses':1, 'num_fall_courses':1, 'num_spring_courses':2},
    {'prof_id':'8b8829ec-4615-4708-a0cd-5103f080ae56', 'id':2, 'year':2022, 'num_relief': 2,
     'num_summer_courses':1, 'num_fall_courses':1, 'num_spring_courses':2},
    {'prof_id':'6e46c60b-6709-4af5-ab4e-7a1c89c8ae0b', 'id':3, 'year':2022, 'num_relief': 2,
     'num_summer_courses':1, 'num_fall_courses':1, 'num_spring_courses':2},
]
UUIDS = [prof['uuid'] for prof in PROFESSORS]

@PROFESSOR_BP.route('/', methods=['GET'])
def get_all_professors():
    '''
    returns all professors
    '''
    sql = """SELECT BIN_TO_UUID(id) as id,
                    first_name, 
                    last_name, 
                    email, 
                    department, 
                    is_teaching, 
                    is_peng FROM Professor"""
    results = DB_CONN.select(sql, ['is_teaching', 'is_peng'])
    return results, 200

@PROFESSOR_BP.route('/', methods=['POST'])
def post_professor():
    '''
    adds a new professor
    '''
    data = request.json
    uuid = DB_CONN.uuid()
    sql = f"""INSERT INTO Professor Values(UUID_TO_BIN(\"{uuid}\"),
                                           \"{data['first_name']}\",
                                           \"{data['last_name']}\",
                                           \"{data['email']}\", 
                                           \"{data['department']}\", 
                                           {data['is_teaching']}, 
                                           {data['is_peng']});"""
    if not DB_CONN.execute(sql):
        return 'Error adding professor', 500
    return uuid, 200


@PROFESSOR_BP.route('/<professor_id>', methods=['GET'])
def get_professor(professor_id):
    '''
    returns a professor with an ID
    '''
    sql = f"""SELECT BIN_TO_UUID(id) as id,
                    first_name, 
                    last_name, 
                    email, 
                    department, 
                    is_teaching, 
                    is_peng FROM Professor WHERE BIN_TO_UUID(id) = \'{professor_id}\'"""
    result = DB_CONN.select_one(sql, ['is_teaching', 'is_peng'])

    if result is None:
        # if empty string - professor not found
        return 'Not Found', 404
    # return 200 OK
    return json.loads(result.response[0]), 200

@PROFESSOR_BP.route('/<professor_id>', methods=['DELETE'])
def delete_professor(professor_id):
    '''
    deletes a professor
    '''
    sql = f"""DELETE FROM Professor WHERE BIN_TO_UUID(id) = \'{professor_id}\'"""
    if not DB_CONN.execute(sql):
        return f'Unable to delete prof with id {professor_id}', 500
    return f'Deleted prof with id {professor_id}', 200