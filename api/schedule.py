'''
contains all /schedule endpoints
'''
from flask import Blueprint, request, jsonify
from c1algo1.scheduler import generate_schedule as c1alg1
from forecaster.forecaster import forecast as c2alg1

SCHEDULE_BP = Blueprint('schedule', __name__)
@SCHEDULE_BP.route('/hello/')
def hello():
    '''
    blah
    '''
    return 'Hello from Schedules'
SCHEDULES = [
    {
        'uuid': '4e90ab30-c380-4034-acdb-238856a88df3',
        'semester': 'Fall',
        'year': '2022',
        'schedule': [
            {
                'timeslot': 'MWF 10am-10:50am',
                'course_code': 'CSC230',
                'prof': 'Bill Bird',
                'section': 'A1',
                'capacity': 100,
            },
            {
                'timeslot': 'MWF 10am-10:50am',
                'course_code': 'CSC230',
                'prof': 'Bill Bird',
                'section': 'A2',
                'capacity': 20,
            },
            {
                'timeslot': 'MTh 10am-10:50am',
                'course_code': 'CSC111',
                'prof': 'Hausi Muller',
                'section': 'A1',
                'capacity': 100,
            },
            {
                'timeslot': 'MTh 10am-10:50am',
                'course_code': 'CSC111',
                'prof': 'Hausi Muller',
                'section': 'A2',
                'capacity': 20,
            },
        ]
    },
    {
        'uuid': '5e90ab30-c380-4034-acdb-238856a88df3',
        'semester': 'Spring',
        'year': '2022',
        'schedule': [
            {
                'timeslot': 'MWF 11am-11:50am',
                'course_code': 'CSC370',
                'prof': 'Bill Bird',
                'section': 'A1',
                'capacity': 40,
            },
            {
                'timeslot': 'MWF 11am-11:50am',
                'course_code': 'CSC370',
                'prof': 'Bill Bird',
                'section': 'A2',
                'capacity': 10,
            },
            {
                'timeslot': 'MTh 2pm-2:50pm',
                'course_code': 'SENG275',
                'prof': 'Mike Zastre',
                'section': 'A1',
                'capacity': 100,
            },
            {
                'timeslot': 'MTh 2pm-2:50pm',
                'course_code': 'SENG275',
                'prof': 'Mike Zastre',
                'section': 'A2',
                'capacity': 20,
            },
        ]
    }
]
UUIDS = [schedule['uuid'] for schedule in SCHEDULES]

@SCHEDULE_BP.route('/', methods=['GET'])
def get_all_schedules():
    '''
    Return JSON object containing a list of schedules with their year, semester and id
    '''
    return jsonify(SCHEDULES), 200

@SCHEDULE_BP.route('/company/<company_num>', methods=['GET'])
def get_company_schedule(company_num):
    '''
    Return JSON object containing a list of schedules with their year, semester and id  as
    generated from <company_num>.
    '''
    message = f'company {company_num} not recongnized'
    status = 200
    if company_num == '1':
        message = c1alg1(None, None, None)
    elif company_num == '2':
        message = c2alg1(None, None, None)
    else:
        status = 404
    return message, status

@SCHEDULE_BP.route('<schedule_id>', methods=['GET'])
def get_schedule(schedule_id):
    '''
    Return JSON object containing schedule
    '''
    if schedule_id not in UUIDS:
        return 'couldn\'t find that schedule', 404
    return jsonify(SCHEDULES[UUIDS.index(schedule_id)]), 200

@SCHEDULE_BP.route('/', methods=['POST'])
def add_schedule():
    '''
    Request contains JSON object containing a new schedule
    Add a new schedule to the table of schedules
    Returns new schedule’s id
    '''
    return f'schedule id of new entry\n\nJSON object:\n{request.data}\n\n', 200

@SCHEDULE_BP.route('/<schedule_id>/<course_id>', methods=['PUT'])
def update_course_time(schedule_id, course_id):
    '''
    Update the time slot of a course in the schedule
    '''
    return f'update timeslot of course {course_id} in schedule {schedule_id}', 200

@SCHEDULE_BP.route('/<schedule_id>/<course_id>/<prof_id>', methods=['PUT'])
def update_course_prof(schedule_id, course_id, prof_id):
    '''
    Update the professor of a course in the existing schedule
    '''
    return f'update prof teaching course {course_id} to \
        prof {prof_id} in schedule {schedule_id}', 200

@SCHEDULE_BP.route('/<schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    '''
    Deletes a schedule from the schedules table
    '''
    return f'deleted schedule {schedule_id}', 200

@SCHEDULE_BP.route('/<schedule_id>/<course_id>', methods=['DELETE'])
def delete_course_from_schedule(schedule_id, course_id):
    '''
    Deletes a course from the schedule
    '''
    return f'deleted course {course_id} from schedule {schedule_id}', 200
