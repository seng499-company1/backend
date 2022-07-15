'''
contains all API /professors/{id}/preferences endpoints
'''
import json
import yaml
from pymysql.converters import escape_string
from flask import Blueprint, request, jsonify, Response
from .dbconn import DB_CONN

PREFERENCE_BP = Blueprint('preference', __name__)
@PREFERENCE_BP.route('/hello/')
def hello():
    '''
    blah
    '''
    return "Hello from Professor Preferences"

@PREFERENCE_BP.route('/preferences/times/<year>', methods=['GET'])
def get_professor_preference_entry_times(year):
    '''
    returns a list of professor preference entry times for the specified year
    '''
    sql = f"""SELECT
                    BIN_TO_UUID(Professor.id) as prof_id,
                    Professor.first_name,
                    Professor.last_name,
                    ProfessorAvailability.time_stamp
            FROM ProfessorAvailability
            LEFT JOIN Professor
            ON ProfessorAvailability.prof_id = Professor.id
            WHERE ProfessorAvailability.year = {year};"""
    result = DB_CONN.select(sql)

    if not isinstance(result, Response):
        return result, 400

    if result.get_json() == []:
        return f'No preference entries exist for year {year}', 404

    return result, 200


@PREFERENCE_BP.route('/<professor_id>/preferences/', methods=['GET'])
def get_professor_preferences(professor_id):
    '''
    returns professor's preference
    '''
    sql = f"""SELECT
                    BIN_TO_UUID(ProfessorAvailability.id) as id,
                    BIN_TO_UUID(ProfessorAvailability.prof_id) as prof_id, 
                    ProfessorAvailability.time_stamp, 
                    ProfessorAvailability.year, 
                    ProfessorAvailability.semester_off,
                    ProfessorAvailability.num_relief,
                    ProfessorAvailability.why_relief, 
                    ProfessorAvailability.num_summer_courses, 
                    ProfessorAvailability.num_fall_courses, 
                    ProfessorAvailability.num_spring_courses,
                    ProfessorAvailability.preferred_times,
                    BIN_TO_UUID(ProfessorCoursePreference.course_id) as course_id,
                    ProfessorCoursePreference.will_to_teach,
                    ProfessorCoursePreference.able_to_teach
            FROM ProfessorAvailability 
            LEFT JOIN ProfessorCoursePreference 
            ON ProfessorCoursePreference.prof_avail_id = ProfessorAvailability.id
            WHERE ProfessorAvailability.prof_id=UUID_TO_BIN(\"{professor_id}\");"""
    results = DB_CONN.select(sql)
    my_json = results.get_json()

    if my_json == []:
        return 'Prof preferences not found', 404

    course_pref = []

    for entry in my_json:
        if entry["course_id"] is None:
            continue
        course_item = {}
        course_item["course_id"] = entry["course_id"]
        course_item["will_to_teach"] = entry["will_to_teach"]
        course_item["able_to_teach"] = entry["able_to_teach"]
        course_pref.append(course_item)

    preferred_times_string = yaml.safe_load(my_json[0]['preferred_times'])
    output = {}
    output["id"] = my_json[0]["id"]
    output["time_stamp"] = my_json[0]["time_stamp"]
    output["year"] = my_json[0]["year"]
    output["semester_off"] = my_json[0]["semester_off"]
    output["num_relief"] = my_json[0]["num_relief"]
    output["num_summer_courses"]= my_json[0]["num_summer_courses"]
    output["num_fall_courses"]= my_json[0]["num_fall_courses"]
    output["num_spring_courses"]= my_json[0]["num_spring_courses"]
    output["why_relief"]= my_json[0]["why_relief"]
    output["preferred_times"] = preferred_times_string
    output["course_preference"] = course_pref

    return jsonify(output), 200

@PREFERENCE_BP.route('/<professor_id>/preferences/', methods=['POST'])
def post_professor_preferences(professor_id):
    '''
    adds a new professor's preferences
    '''
    data = request.json
    uuid = DB_CONN.uuid()
    sqls = []
    data = json.loads(data)
    json_preferred_times = json.dumps(data['preferred_times'])
    insert_json = escape_string(json_preferred_times)
    sqls.append(f"""INSERT INTO ProfessorAvailability
                    (
                        id,
                        prof_id, 
                        year, 
                        semester_off,
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
                        {data['semester_off']},
                        {data['num_relief']},
                        \"{data['why_relief']}\", 
                        {data['num_summer_courses']}, 
                        {data['num_fall_courses']}, 
                        {data['num_spring_courses']},
                        \'{insert_json}\'
                    );""")

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

    result = DB_CONN.multi_execute(sqls)

    if result is not True:
        return result, 400

    return uuid, 200

@PREFERENCE_BP.route('/<professor_id>/preferences/', methods=['PUT'])
def update_professor_preferences(professor_id):
    '''
    updates a professor's preferences
    '''
    data = request.json
    sqls = []
    json_preferred_times = json.dumps(data['preferred_times'])
    insert_json = escape_string(json_preferred_times)
    sqls.append(f"""UPDATE ProfessorAvailability SET
                        year = {data['year']},
                        semester_off = {data['semester_off']},
                        num_relief = {data['num_relief']},
                        why_relief = \"{data['why_relief']}\",
                        num_summer_courses = {data['num_summer_courses']},
                        num_fall_courses = {data['num_fall_courses']},
                        num_spring_courses = {data['num_spring_courses']},
                        preferred_times = \'{insert_json}\'
                    WHERE BIN_TO_UUID(prof_id)=\"{professor_id}\";""")

    course_prefs = data['course_preferences']

    for course in course_prefs:
        sqls.append(f"""UPDATE ProfessorCoursePreference SET
                                year = {data['year']},
                                will_to_teach = \"{course['will_to_teach']}\",
                                able_to_teach = \"{course['able_to_teach']}\"
                            WHERE BIN_TO_UUID(course_id)=\"{course['course_id']}\";""")

    result = DB_CONN.multi_execute(sqls)

    if result is not True:
        return result, 400

    return f'updates the preferences for \
     professor with id {professor_id}', 200


@PREFERENCE_BP.route('/<professor_id>/preferences/', methods=['DELETE'])
def delete_professor_preferences(professor_id):
    '''
    deletes a professor's preferences
    '''
    sql = """DELETE FROM ProfessorAvailability
                    WHERE BIN_TO_UUID(prof_id) = \'{professor_id}\'"""

    result = DB_CONN.execute(sql)
    if result is not True:
        return result, 400

    return f'deleted preference for \
     professor with id {professor_id}', 200
