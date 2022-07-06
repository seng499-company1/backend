'''
contains all /schedule endpoints
'''
from flask import Blueprint, request, jsonify
from c1algo1.scheduler import generate_schedule as c1alg1
#from c1algo2 import forecast as c1alg2 ## not working right now, algo2 needs to debug this
from coursescheduler import generate_schedule as c2alg1
from forecaster.forecaster import forecast as c2alg2
from .helper import get_prof_array, get_empty_schedule
from .dbconn import DB_CONN

SCHEDULE_BP = Blueprint('schedule', __name__)
@SCHEDULE_BP.route('/hello/')
def hello():
    '''
    blah
    '''
    return 'Hello from Schedules'

@SCHEDULE_BP.route('/', methods=['GET'])
def get_all_schedules():
    '''
    Return JSON object containing a list of schedules with their year, semester and id
    '''
    sql = f"""SELECT
                *
        FROM Schedule;"""
    results = DB_CONN.select(sql)
    return results, 200

@SCHEDULE_BP.route('/<schedule_id>', methods=['GET'])
def get_schedule(schedule_id):
    '''
    Return a schedule with a particular id
    '''
    sql = f"""SELECT
                *
        FROM Schedule
        WHERE BIN_TO_UUID(id) = \'{schedule_id}\';"""
    results = DB_CONN.select_one(sql)
    if results == None:
        return 'Schedule not found',404
    return results, 200

@SCHEDULE_BP.route('/company/<company_num>', methods=['GET'])
def get_company_schedule(company_num):
    '''
    Return JSON object containing a list of schedules with their year, semester and id  as
    generated from <company_num>.
    '''
    prof_array = get_prof_array()
    schedule = get_empty_schedule()
    message = f'company {company_num} not recognized'
    status = 200
    # input to Algo 2
    # historicalData: HistoricalCourseOffering[]
    # previousEnrolment: ProgramEnrolment
    # schedule: Schedule
    # algo2_schedule = c1alg2(historical_data, previous_enrolment, schedule)
    # input schedule to algo 1
    # final_schedule = c1alg1(prof_array, algo2_schedule)
    # post schedule
    # return schedule
    if company_num == '1':
        message = 'Algo 1: ' + c1alg1(None, None, None)
        # message += ' Algo 2: ' + c1alg2(None, None, None) << not working same as above
    elif company_num == '2':
        message = 'Algo 1: ' + c2alg1(None, None, None)
        message += ' Algo 2: ' + c2alg2(None, None, None)
    else:
        status = 404
    return message, status

@SCHEDULE_BP.route('/<schedule_id>', methods=['PUT'])
def update_schedule(schedule_id):
    '''
    Update the schedule 
    '''
    return f'update schedule {schedule_id}', 200

@SCHEDULE_BP.route('/<schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    '''
    Deletes a schedule from the schedules table
    '''
    return f'deleted schedule {schedule_id}', 200
