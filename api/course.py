'''
contains all /courses endpoints
'''
import json
from flask import Blueprint, request
from .dbconn import DB_CONN
COURSE_BP = Blueprint('course', __name__)
@COURSE_BP.route('/hello/')
def hello():
    '''
    blah
    '''
    return 'Hello from Courses'

@COURSE_BP.route('/', methods=['GET'])
def get_all_courses():
    '''
    Return JSON object containing a list of courses and their course ids
    '''
    sql = """SELECT BIN_TO_UUID(id) as id,
                    course_code,
                    course_name,
                    min_offering,
                    spring_req,
                    summer_req,
                    fall_req,
                    spring_peng_req,
                    summer_peng_req,
                    fall_peng_req,
                    course_desc,
                    prof_prereq,
                    year_req
                    FROM CourseOffering"""
    results = DB_CONN.select(sql, ['spring_req', 'summer_req', 'fall_req',
                                   'spring_peng_req', 'summer_peng_req', 'fall_peng_req'])
    with open('populate_prof_prefs/curr_courses.json', 'w', encoding='utf-8') as file_handle:
        json.dump(results.json,file_handle)
    return results, 200

@COURSE_BP.route('/<course_id>', methods=['GET'])
def get_course(course_id):
    '''
    Return JSON object containing that course’s information
    '''
    sql = f"""SELECT BIN_TO_UUID(id) as id,
                    course_code,
                    course_name,
                    min_offering,
                    spring_req,
                    summer_req,
                    fall_req,
                    spring_peng_req,
                    summer_peng_req,
                    fall_peng_req,
                    course_desc,
                    prof_prereq,
                    year_req
                    FROM CourseOffering 
                    WHERE BIN_TO_UUID(id) = \'{course_id}\'"""
    result = DB_CONN.select_one(sql, ['spring_req', 'summer_req', 'fall_req',
                                      'spring_peng_req', 'summer_peng_req', 'fall_peng_req'])
    if result is None:
        # if empty string - course not found
        return 'Not Found', 404
    # return 200 OK
    return json.loads(result.response[0]), 200

@COURSE_BP.route('/', methods=['POST'])
def add_course():
    '''
    Request contains JSON object containing information about the course being posted
    Add a new course to the table of courses
    Returns new course’s id
    '''
    data = request.json
    uuid = DB_CONN.uuid()
    sql = f"""INSERT INTO CourseOffering Values(UUID_TO_BIN(\"{uuid}\"),
                                            \"{data['course_name']}\",
                                            \"{data['course_code']}\",
                                            \"{data['course_desc']}\",
                                            \"{data['prof_prereq']}\",
                                            \"{data['min_offering']}\",
                                            {data['spring_req']},
                                            {data['summer_req']},
                                            {data['fall_req']},
                                            {data['spring_peng_req']},
                                            {data['summer_peng_req']},
                                            {data['fall_peng_req']},
                                            {data['year_req']});
                                            """
    if not DB_CONN.execute(sql):
        return 'Error adding course', 500
    return uuid, 200

@COURSE_BP.route('/<course_id>', methods=['PUT'])
def put_course(course_id):
    '''
    Update a course's information
    '''
    data = request.json
    sql = f"""UPDATE CourseOffering SET course_name = \"{data['course_name']}\",
                                        course_code = \"{data['course_code']}\",
                                        course_desc = \"{data['course_desc']}\",
                                        prof_prereq = \"{data['prof_prereq']}\",
                                        min_offering = {data['min_offering']},
                                        spring_req = {data['spring_req']},
                                        summer_req = {data['summer_req']},
                                        fall_req = {data['fall_req']},
                                        spring_peng_req = {data['spring_peng_req']},
                                        summer_peng_req = {data['summer_peng_req']},
                                        fall_peng_req = {data['fall_peng_req']},
                                        year_req = {data['year_req']}
                                        WHERE BIN_TO_UUID(id) = \'{course_id}\';"""
    if not DB_CONN.execute(sql):
        return 'Error updating course', 500
    return f'Updated {course_id}', 200

@COURSE_BP.route('/<course_id>', methods=['DELETE'])
def delete_course(course_id):
    '''
    Deletes a course from the course table
    '''

    sql = f"""DELETE FROM CourseOffering WHERE BIN_TO_UUID(id) = \'{course_id}\'"""
    if not DB_CONN.execute(sql):
        return f'Unable to delete course with id {course_id}', 500
    return course_id, 200
