'''
contains all API /professors/{id}/preferences endpoints
'''
import json
import pymysql
import yaml
from pymysql.converters import escape_string
from flask import Blueprint, request
from .dbconn import DB_CONN

PREFERENCE_BP = Blueprint('preference', __name__)
@PREFERENCE_BP.route('/hello/')
def hello():
    '''
    blah
    '''
    return "Hello from Professor Preferences"
pref_times = {}
@PREFERENCE_BP.route('/<professor_id>/preferences/', methods=['GET'])
def get_professor_preferences(professor_id):
    '''
    returns professor's preference
    '''
    sql = f"""SELECT
                    BIN_TO_UUID(ProfessorAvailability.id) as id,
                    BIN_TO_UUID(ProfessorAvailability.prof_id) as prof_id, 
                    ProfessorAvailability.year, 
                    ProfessorAvailability.num_relief,
                    ProfessorAvailability.why_relief, 
                    ProfessorAvailability.num_summer_courses, 
                    ProfessorAvailability.num_fall_courses, 
                    ProfessorAvailability.num_spring_courses,
                    ProfessorAvailability.preferred_times,
                    BIN_TO_UUID(ProfessorCoursePreference.course_id) as course_id,
                    ProfessorCoursePreference.will_to_teach,
                    ProfessorCoursePreference.able_to_teach,
                    ProfessorCoursePreference.time_stamp
            FROM ProfessorAvailability 
            LEFT JOIN ProfessorCoursePreference 
            ON ProfessorCoursePreference.prof_avail_id = ProfessorAvailability.id
            WHERE ProfessorAvailability.prof_id=UUID_TO_BIN(\"{professor_id}\");"""
    results = DB_CONN.select(sql)
    my_json = results.get_json()
    course_pref = []
    for entry in my_json:
        if entry["course_id"] is None:
            continue
        course_item = {}
        course_item["course_id"] = entry["course_id"]
        course_item["will_to_teach"] = entry["will_to_teach"]
        course_item["able_to_teach"] = entry["able_to_teach"]
        course_item["time_stamp"] = entry["time_stamp"]
        course_pref.append(course_item)
    if my_json == []:
        return 'Prof preferences not found',404
    my_str = yaml.safe_load(my_json[0]['preferred_times'])
    preferred_times_string = my_str.replace('\\u201c', '"').replace('\\u201d', '\"')
    output = {}
    output["id"] = my_json[0]["id"]
    output["year"] = my_json[0]["year"]
    output["num_relief"] = my_json[0]["num_relief"]
    output["num_summer_courses"]= my_json[0]["num_summer_courses"]
    output["num_fall_courses"]= my_json[0]["num_fall_courses"]
    output["num_spring_courses"]= my_json[0]["num_spring_courses"]
    output["why_relief"]= my_json[0]["why_relief"]
    output["preferred_times"] = preferred_times_string #pref_times[str(my_json[0]["prof_id"])]
    output["course_preference"] = course_pref
    # CASE: PROF DNE; RET 404
    return json.dumps(output), 200

@PREFERENCE_BP.route('/<professor_id>/preferences/', methods=['POST'])
def post_professor_preferences(professor_id):
    '''
    adds a new professor's preferences
    '''
    data = request.json
    uuid = DB_CONN.uuid()
    sqls = []
    json_preferred_times = json.dumps(data['preferred_times'])
    insert_json = escape_string(json_preferred_times)
    sqls.append(f"""INSERT INTO ProfessorAvailability
                    (
                        id,
                        prof_id, 
                        year, 
                        num_relief, 
                        why_relief, 
                        num_summer_courses, 
                        num_fall_courses, 
                        num_spring_courses,
                        preferred_times
                    ) Values(
                        UUID_TO_BIN(\"{uuid}\"),
                        UUID_TO_BIN(\"{professor_id}\"),
                        {data['year']},
                        {data['num_relief']},
                        \"{data['why_relief']}\", 
                        {data['num_summer_courses']}, 
                        {data['num_fall_courses']}, 
                        {data['num_spring_courses']},
                        \'{insert_json}\'
                    );""")

    pref_times[str(professor_id)] = data['preferred_times']
    course_prefs = data['course_preferences']
    for course in course_prefs:
        sqls.append(f"""INSERT INTO ProfessorCoursePreference
                            (
                                course_id,
                                prof_avail_id,
                                year,
                                will_to_teach,
                                able_to_teach
                            ) Values(
                                UUID_TO_BIN(\"{course['course_id']}\"),
                                UUID_TO_BIN(\"{uuid}\"),
                                {data['year']},
                                \"{course['will_to_teach']}\",
                                \"{course['able_to_teach']}\"
                            );""")
    DB_CONN.multi_execute(sqls)
    # CASE INVALID JSON; RET 400
    return uuid, 200

@PREFERENCE_BP.route('/<professor_id>/preferences/', methods=['PUT'])
def update_professor_preferences(professor_id):
    '''
    updates a professor's preferences
    '''
    data = request.json
    sqls = []
    sqls.append(f"""UPDATE ProfessorAvailability SET
                        year = {data['year']},
                        num_relief = {data['num_relief']},
                        why_relief = \"{data['why_relief']}\",
                        num_summer_courses = {data['num_summer_courses']},
                        num_fall_courses = {data['num_fall_courses']},
                        num_spring_courses = {data['num_spring_courses']}
                    WHERE BIN_TO_UUID(prof_id)=\"{professor_id}\";""")

    pref_times[str(professor_id)] = data['preferred_times']

    course_prefs = data['course_preferences']
    for course in course_prefs:
        sqls.append(f"""UPDATE ProfessorCoursePreference SET
                                year = {data['year']},
                                will_to_teach = \"{course['will_to_teach']}\",
                                able_to_teach = \"{course['able_to_teach']}\"
                            WHERE BIN_TO_UUID(course_id)=\"{course['course_id']}\";""")
    DB_CONN.multi_execute(sqls)
    # CASE PROF DNE; RET 404
    return f'updates the preferences for \
     professor with id {professor_id}', 200


@PREFERENCE_BP.route('/<professor_id>/preferences/', methods=['DELETE'])
def delete_professor_preferences(professor_id):
    '''
    deletes a professor's preferences
    '''
    sql = """DELETE FROM ProfessorCoursePreference
                    WHERE BIN_TO_UUID(prof_id) = \'{professor_id}\'"""
    if not DB_CONN.execute(sql):
        return f'Unable to delete prof pref with id {professor_id}', 500
    return f'deleted preference for \
     professor with id {professor_id}', 200
