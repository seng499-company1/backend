'''
contains all /schedule endpoints
'''
import json
import yaml
import sys
from flask import Blueprint, jsonify, request
from pymysql.converters import escape_string
from forecaster.forecaster import forecast as c2alg2
from c1algo1 import scheduler as c1alg1
from c1algo2.forecaster import forecast as c1alg2
from coursescheduler import generate_schedule as c2alg1
from .helper import get_prof_array, get_empty_schedule, get_previous_enrolment, get_historical_data
from .dbconn import DB_CONN

SCHEDULE_BP = Blueprint('schedule', __name__)
@SCHEDULE_BP.route('/hello/')
def hello():
    '''
    Sanity Endpoint
    '''
    return 'Hello from Schedules'

@SCHEDULE_BP.route('/', methods=['GET'])
def get_all_schedules():
    '''
    Return JSON object containing a list of schedules with their year, semester and id
    '''
    sql = """SELECT
                BIN_TO_UUID(id) as id,
                year,
                result
        FROM Schedule;"""
    results = DB_CONN.select(sql)

    if isinstance(results, str):
        return results, 400

    my_json = results.get_json()
    if my_json == []:
        return 'No schedules found', 404
    #render json properly for each schedule
    for schedule in my_json:
        schedule['result'] = yaml.safe_load(schedule['result'])
    return jsonify(my_json), 200

@SCHEDULE_BP.route('/<schedule_id>', methods=['GET'])
def get_schedule(schedule_id):
    '''
    Return a schedule with a particular id
    '''
    sql = f"""SELECT
                BIN_TO_UUID(id) as id,
                year,
                result
        FROM Schedule
        WHERE BIN_TO_UUID(id) = \'{schedule_id}\';"""
    results = DB_CONN.select_one(sql)

    if isinstance(results, str):
        return results, 400

    my_json = results.get_json()

    if results is None:
        return 'Schedule not found', 404
    # render json properly
    my_json['result'] = yaml.safe_load(my_json['result'])
    return my_json, 200

@SCHEDULE_BP.route('/company/<company_num>', methods=['GET'])
def get_company_schedule(company_num):
    '''
    Return JSON object containing a list of schedules with their year, semester and id  as
    generated from <company_num>.
    '''
    professors = get_prof_array()
    previous_enrolment = get_previous_enrolment()
    historical_data = get_historical_data()
    if company_num == '1':
        schedule = get_empty_schedule(1)
        schedule = c1alg2(historical_data, previous_enrolment, schedule)
        final_schedule, errors = c1alg1.generate_schedule(professors, schedule)
    elif company_num == '2':
        schedule = get_empty_schedule(2)
        schedule = c2alg2(historical_data, previous_enrolment, schedule)
        final_schedule, errors = c2alg1(professors, schedule)
    else:
        return f'Company {company_num} Not Found.', 404
    # post schedule
    print(errors, file=sys.stderr)
    data = final_schedule
    uuid = DB_CONN.uuid()
    json_schedule = json.dumps(data)
    json_schedule = escape_string(json_schedule)
    sql = f"""INSERT INTO Schedule
                    (
                        id,
                        year,
                        semester,
                        result
                    ) Values(
                        UUID_TO_BIN(\"{uuid}\"),
                        2022,
                        'a',
                        \'{json_schedule}\'
                    );"""
    result = DB_CONN.execute(sql)

    if isinstance(result, str):
        return result, 400

    return {"id": uuid, "year": 2022, "schedule":final_schedule}, 200

@SCHEDULE_BP.route('/<schedule_id>', methods=['PUT'])
def update_schedule(schedule_id):
    '''
    Update and validate the schedule.
    '''
    data = request.json
    professors = get_prof_array()
    schedule = data['schedule']
    errors = c1alg1.validate(schedule, professors)
    json_schedule = json.dumps(data['schedule'])
    json_schedule = escape_string(json_schedule)
    sql = f"""UPDATE Schedule SET result = \"{json_schedule}\"
                                        WHERE BIN_TO_UUID(id) = \'{schedule_id}\';"""
    if not DB_CONN.execute(sql):
        return 'Error updating course', 500
    return {"errors": errors}, 200

@SCHEDULE_BP.route('/<schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    '''
    Deletes a schedule from the schedules table
    '''
    sql = f"""DELETE FROM Schedule WHERE BIN_TO_UUID(id) = \'{schedule_id}\';"""
    result = DB_CONN.execute(sql)

    if isinstance(result, str):
        return result, 400

    return f'deleted schedule with id {schedule_id}', 200
