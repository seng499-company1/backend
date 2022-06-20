'''
contains all API /professors/{id}/preferences endpoints
'''
from flask import Blueprint, jsonify, request
from .dbconn import DB_CONN

PREFERENCE_BP = Blueprint('preference', __name__)
@PREFERENCE_BP.route('/hello/')
def hello():
    '''
    blah
    '''
    return "Hello from Professor Preferences"
@PREFERENCE_BP.route('/<professor_id>/preferences/', methods=['GET'])
def get_professor_preferences(professor_id):
    '''
    returns professor's preference
    '''
    sql = f"""SELECT * FROM ProfessorAvailability WHERE UUID_TO_BIN(\"{professor_id}\")=id"""
    # CASE: PROF DNE; RET 404
    results = DB_CONN.select(sql)
    return results, 200

@PREFERENCE_BP.route('/<professor_id>/preferences/', methods=['POST'])
def post_professor_preferences(professor_id):
    '''
    adds a new professor's preferences
    '''
    data = request.json
    uuid = DB_CONN.uuid()
    sql = f"""INSERT INTO ProfessorAvailability Values(UUID_TO_BIN(\"{uuid}\"),
                                            UUID_TO_BIN(\"{professor_id}\"),
                                           {data['year']},
                                           {data['num_relief']},
                                           \"{data['why_relief']}\", 
                                           {data['num_summer_courses']}, 
                                           {data['num_fall_courses']}, 
                                           {data['num_spring_courses']},
                                           {data['preferred_times']});""" #preferred times is JSON; any formatting needed?
    DB_CONN.insert(sql)
    # CASE INVALID JSON; RET 400
    return uuid, 200

@PREFERENCE_BP.route('/<professor_id>/preferences/', methods=['PUT'])
def update_professor_preferences(professor_id):
    '''
    updates a professor's preferences
    '''
    # CASE PROF DNE; RET 404
    return f'updates the preferences for \
     professor with id {professor_id}', 200


@PREFERENCE_BP.route('/<professor_id>/preferences/', methods=['DELETE'])
def delete_professor_preferences(professor_id):
    '''
    deletes a professor's preferences
    '''
    # CASE PROF DNE; RET 404
    return f'deleted preference for \
     professor with id {professor_id}', 200
