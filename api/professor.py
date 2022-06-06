'''
contains all API /professors endpoints
'''
from flask import Blueprint, jsonify
PROFESSOR_BP = Blueprint('professor', __name__)
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
    return jsonify(PROFESSORS), 200

@PROFESSOR_BP.route('/<professor_id>', methods=['GET'])
def get_professor(professor_id):
    '''
    returns a professor with an ID
    '''
    return jsonify(PROFESSORS[UUIDS.index(professor_id)]), 200

@PROFESSOR_BP.route('/<professor_id>/preferences', methods=['GET'])
def get_professor_preferences(professor_id):
    '''
    returns all of professor's preferences
    '''
    return jsonify(RELIEFS[UUIDS.index(professor_id)]), 200

@PROFESSOR_BP.route('/<professor_id>/preferences/<preference_id>', methods=['GET'])
def get_professor_preference(professor_id, preference_id):
    '''
    returns a professor's preferences for a certain year
    '''
    response = ''
    if RELIEFS[UUIDS.index(professor_id)]['id'] != int(preference_id):
        response = 'couldn\'t find that preference id', 404
    else:
        response = jsonify(RELIEFS[UUIDS.index(professor_id)]), 200
    return response

@PROFESSOR_BP.route('/', methods=['POST'])
def post_professor():
    '''
    adds a new professor
    '''
    return 'posted a professor', 200

@PROFESSOR_BP.route('/<professor_id>/preferences', methods=['POST'])
def post_professor_preferences(professor_id):
    '''
    adds a new professor's preferences
    '''
    return f'updates a prof with professor_id {professor_id}', 200

@PROFESSOR_BP.route('/<professor_id>/preferences/<preference_id>', methods=['PUT'])
def update_professor_preferences(professor_id, preference_id):
    '''
    updates a professor's preferences
    '''
    return f'updates the preferences with id {preference_id} for \
     professor with id {professor_id}', 200

@PROFESSOR_BP.route('/<professor_id>', methods=['DELETE'])
def delete_professor(professor_id):
    '''
    deletes a professor
    '''
    return f'deleted prof with id {professor_id}', 200

@PROFESSOR_BP.route('/<professor_id>/preferences/<preference_id>', methods=['DELETE'])
def delete_professor_preferences(professor_id, preference_id):
    '''
    deletes a professor's preferences
    '''
    return f'deleted preference with id {preference_id} for professor with id {professor_id}', 200
