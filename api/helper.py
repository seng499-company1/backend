import json
from .dbconn import DB_CONN

TimeRange = tuple[str,str]
START = 0
END = 1
def get_previous_enrolment()->dict[str:dict]:
    '''
    Gets and returns a dictionary of previous enrollment stored in json file
    TODO: Make this more efficient - static data, we don't need to read from file everytime 
    '''
    file_handle = open('../database/init_data/algo_data/previous_enrolment.json')
    data = json.load(file_handle)

    file_handle.close()
    return {'enrolmentByCalendarYear': data}
def get_historical_data()->list:
    '''
    Gets and returns a list of the historical data
    '''
    file_handle = open('../database/init_data/algo_data/historical_data.json')
    data = json.load(file_handle)
    file_handle.close()
    return data
def get_empty_schedule():
    '''
    Creates and returns an empty schedule pre-populated with courses
    '''
    #TODO: add non-eng classes and timeslots
    schedule = {}
    schedule['fall'] = get_course_offering('fall_req')
    schedule['spring'] = get_course_offering('spring_req')
    schedule['summer'] = get_course_offering('summer_req')
    return schedule
def get_course_offering(semester:str):
    '''
    get and return the list of courseOffering for a certain semester
    PARAMETERS: 'spring_req' or 'summer_req' or 'fall_req'
    '''
    sql = f"""SELECT
                    course_code,
                    course_name,
                    spring_req,
                    summer_req,
                    fall_req,
                    spring_peng_req,
                    summer_peng_req,
                    fall_peng_req,
                    year_req
            FROM CourseOffering
            WHERE {semester} = 1;"""
    results = DB_CONN.select(sql, ['spring_peng_req','summer_peng_req', 'fall_peng_req'])
    courses_json = results.get_json()
    courses = []
    for course in courses_json:
        new_course = {}
        new_course['code'] = course['course_code']
        new_course['title'] = course['course_name']
        peng_required = {}
        peng_required['fall'] = course['fall_peng_req']
        peng_required['spring'] = course['spring_peng_req']
        peng_required['summer'] = course['summer_peng_req']
        new_course['pengRequired'] = peng_required
        new_course['yearRequired'] = course['year_req']
        course_section = {}
        course_sections = [course_section]
        course_offering = {}
        course_offering['course'] = new_course
        course_offering['sections'] = course_sections
        courses.append(course_offering)
    return courses
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
                    ProfessorAvailability.preferred_times,
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
        # add preferred Times
        new_prof['preferredTimes'] = get_preferred_times(my_json[i]['preferred_times'])
        new_prof['preferredCourseDaySpreads'] = get_preferred_day_spread(my_json[i]['preferred_times'])
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
def get_preferred_day_spread(preferred_times:str)->list[str]:
    '''
    Creates and returns a list of the prof's preferred day spreads: M, T, W, Th, F, TWF, MTh
    TODO: There is probably a better way to do this
    '''
    list_of_day_spreads = []
    fall_input = json.loads(preferred_times)['fall']
    if fall_input['mon']['preferredDay']:
        list_of_day_spreads.append("M")
    if fall_input['tues']['preferredDay']:
        list_of_day_spreads.append("T")
    if fall_input['wed']['preferredDay']:
        list_of_day_spreads.append("W")
    if fall_input['thurs']['preferredDay']:
        list_of_day_spreads.append("Th")
    if fall_input['fri']['preferredDay']:
        list_of_day_spreads.append("F")
    if fall_input['fri']['preferredDay'] and fall_input['wed']['preferredDay'] and fall_input['tues']['preferredDay']:
        list_of_day_spreads.append("TWF")
    if fall_input['mon']['preferredDay'] and fall_input['thurs']['preferredDay']:
        list_of_day_spreads.append("MTh")
    return list_of_day_spreads

def get_preferred_times(preferred_times:str)-> dict[str, dict]:
    '''
    Creates a dictionary of the professor's preferred times 
    TODO: Optimize this  
    '''
    my_json = json.loads(preferred_times)
    fall_input  = my_json['fall']
    fall_output = {}
    fall_output['monday'] = get_daily_times_list('mon', fall_input)
    fall_output['tuesday'] = get_daily_times_list('tues', fall_input)
    fall_output['wednesday'] = get_daily_times_list('wed', fall_input)
    fall_output['thursday'] = get_daily_times_list('thurs', fall_input)
    fall_output['friday'] = get_daily_times_list('fri', fall_input)

    spring_input  = my_json['spring']
    spring_output = {}
    spring_output['monday'] = get_daily_times_list('mon', spring_input)
    spring_output['tuesday'] = get_daily_times_list('tues', spring_input)
    spring_output['wednesday'] = get_daily_times_list('wed', spring_input)
    spring_output['thursday'] = get_daily_times_list('thurs', spring_input)
    spring_output['friday'] = get_daily_times_list('fri', spring_input)

    summer_input  = my_json['summer']
    summer_output = {}
    summer_output['monday'] = get_daily_times_list('mon', summer_input)
    summer_output['tuesday'] = get_daily_times_list('tues', summer_input)
    summer_output['wednesday'] = get_daily_times_list('wed', summer_input)
    summer_output['thursday'] = get_daily_times_list('thurs', summer_input)
    summer_output['friday'] = get_daily_times_list('fri', summer_input)
    preferred_times_dict = {'fall':fall_output, 'spring':spring_output, 'summer':summer_output}
    return preferred_times_dict

def get_daily_times_list(day_of_week:str, input_json)->list[TimeRange]:
    '''
    Creates and returns a list of TimeRange tuples indicating the starting and ending times a prof would like to teach for one day.
    '''
    list_of_times = input_json[day_of_week]['times'][0].replace("(","").replace(")","").replace(u"\u201c", "").replace(u"\u201d", "").split()
    index = 0
    list_of_tuples = []
    while index < len(list_of_times):
        list_of_tuples.append((list_of_times[index], list_of_times[index+1]))
        index += 2
    return list_of_tuples
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