'''
contains all /schedule endpoints
'''
from flask import Blueprint, request, jsonify
from c1algo1.scheduler import generate_schedule as c1alg1
# from c1algo2 import forecast as c1alg2 << not working right now, algo2 needs to debug this
from coursescheduler import generate_schedule as c2alg1
from forecaster.forecaster import forecast as c2alg2
from .dbconn import DB_CONN

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
    prof_array = get_prof_array()
    print(prof_array)
    message = f'company {company_num} not recongnized'
    status = 200
    if company_num == '1':
        message = 'Algo 1: ' + c1alg1(None, None, None)
        # message += ' Algo 2: ' + c1alg2(None, None, None) << not working same as above
    elif company_num == '2':
        message = 'Algo 1: ' + c2alg1(None, None, None)
        message += ' Algo 2: ' + c2alg2(None, None, None)
    else:
        status = 404
    return message, status
def get_prof_array():
    '''
    Creates and returns an array of Professors
    '''
    sql = f"""SELECT
                    BIN_TO_UUID(ProfessorAvailability.id) as id,
                    BIN_TO_UUID(ProfessorAvailability.prof_id) as prof_id, 
                    ProfessorAvailability.year, 
                    ProfessorAvailability.num_relief,
                    ProfessorAvailability.num_summer_courses, 
                    ProfessorAvailability.num_fall_courses, 
                    ProfessorAvailability.num_spring_courses,
                    Professor.first_name,
                    Professor.last_name,
                    Professor.is_peng,
                    Professor.is_teaching
            FROM ProfessorAvailability
            LEFT JOIN Professor
            ON ProfessorAvailability.prof_id = Professor.id;"""
    results = DB_CONN.select(sql, ['is_peng', 'is_teaching'])
    my_json = results.get_json()
    prof_array = []
    
    i = 0
    for prof in my_json:
        new_prof = {}
        prof_avail_id = my_json[i]['id']
        new_prof['id'] = my_json[i]['prof_id']
        new_prof['name'] = f"{my_json[i]['first_name']} {my_json[i]['last_name']}"
        new_prof['isPeng'] = my_json[i]['is_peng']
        if(my_json[i]['is_teaching']):
            new_prof['facultyType'] = 'TEACHING'
            num_classes = 6
        else:
            new_prof['facultyType'] = 'RESEARCH'
            num_classes = 3
        num_classes -= my_json[i]['num_relief']
        if(num_classes<0):
            num_classes = 0
        new_prof['teachingObligations'] = num_classes
        preferred_courses_per_semester = {}
        preferred_courses_per_semester['fall'] = my_json[i]['num_fall_courses']
        preferred_courses_per_semester['spring'] = my_json[i]['num_spring_courses']
        preferred_courses_per_semester['summer'] = my_json[i]['num_summer_courses']
        new_prof['preferredCoursesPerSemester'] = preferred_courses_per_semester
        if(preferred_courses_per_semester['fall'] == 0):
            new_prof['preferredNonTeachingSemester'] = 'FALL'
        elif(preferred_courses_per_semester['spring'] == 0):
            new_prof['preferredNonTeachingSemester'] = 'SPRING'
        elif(preferred_courses_per_semester['summer'] == 0):
            new_prof['preferredNonTeachingSemester'] = 'SUMMER'
        # now added course Preferences
        sql = f"""SELECT
                    ProfessorCoursePreference.will_to_teach,
                    ProfessorCoursePreference.able_to_teach,
                    CourseOffering.course_code
            FROM ProfessorAvailability
            LEFT JOIN ProfessorCoursePreference
            ON ProfessorAvailability.id = ProfessorCoursePreference.prof_avail_id
            LEFT JOIN CourseOffering
            ON ProfessorCoursePreference.course_id = CourseOffering.id
            WHERE ProfessorCoursePreference.prof_avail_id = UUID_TO_BIN(\"{prof_avail_id}\");"""
        results = DB_CONN.select(sql)
        course_preferences_json = results.get_json()
        course_preferences = []
        pref_index = 0
        for pref in course_preferences_json:
            new_course_pref = {}
            new_course_pref['courseCode'] = pref['course_code']
            new_course_pref['enthusiasmScore'] = get_score(pref['able_to_teach'], pref['will_to_teach'])
            course_preferences.append(new_course_pref)
            pref_index += 1
        new_prof['coursePreferences'] = course_preferences
        prof_array.append(new_prof)
        i += 1
    return prof_array
def get_score(able_to_teach:str, will_to_teach:str):
    '''
    Given an able to teach enum and will to teach returns the numerical score 
    '''
    score = 0
    if able_to_teach== 'WITH_EFFORT':
        if will_to_teach == 'UNWILLING':
            score = 20
        elif will_to_teach == 'WILLING':
            score = 40
        elif will_to_teach == 'VERY_WILLING':
            score = 100
    elif able_to_teach == 'ABLE':
        if will_to_teach == 'UNWILLING':
            score = 39
        elif will_to_teach == 'WILLING':
            score = 78
        elif will_to_teach == 'VERY_WILLING':
            score = 195
    return score
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
