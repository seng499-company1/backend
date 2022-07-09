'''
contains all /schedule endpoints
'''
from flask import Blueprint, request, jsonify
import pickle
from c1algo1.scheduler import generate_schedule as c1alg1
from c1algo2.forecaster import forecast ## not working right now, algo2 needs to debug this
from coursescheduler import generate_schedule as c2alg1
#from forecaster.forecaster import forecast as c2alg2
<<<<<<< HEAD
from .helper import get_prof_array, get_empty_schedule, get_previous_enrolment, get_historical_data
from .dbconn import DB_CONN
=======
>>>>>>> origin/main

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
    professors = get_prof_array()
    schedule = get_empty_schedule()
    previous_enrolment = get_previous_enrolment()
    historical_data = get_historical_data()
    message = f'company {company_num} not recognized'
    status = 200
    outfile= open('historical_data', 'wb')
    pickle.dump(historical_data, outfile)
    outfile.close()
    outfile= open('previous_enrolment', 'wb')
    pickle.dump(previous_enrolment, outfile)
    outfile.close()
    outfile= open('schedule', 'wb')
    pickle.dump(schedule, outfile)
    outfile.close()
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
        message = 'Algo 1: ' + c1alg1(historical_data, previous_enrolment, schedule)
        message += ' Algo 2: ' + forecast(historical_data, previous_enrolment, schedule)# << not working same as above
    elif company_num == '2':
<<<<<<< HEAD
        input_sch = schedule 
        message = c2alg1(historical_data,professors, schedule)
        print(schedule == input_sch)
=======
        message = 'Algo 1: ' + c2alg1(None, None, None)
>>>>>>> origin/main
        #message += ' Algo 2: ' + c2alg2(None, None, None)
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
