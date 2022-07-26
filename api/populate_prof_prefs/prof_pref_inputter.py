'''
Inputs randomized prof preferences for all professors in db.
Instructions on how to use in the README.md.
Based on Algo1 Kai's randomizer.
'''
import random
import json
import requests
input_json = {"year": 2022}

time_slots = ['8:30',
'9:00',
'9:30',
'10:00',
'10:30',
'11:00',
'11:30',
'12:30',
'13:00',
'13:30',
'14:00',
'14:30',
'15:00',
'15:30',
'16:00',
'16:30',
'17:00',
'17:30',
'18:00',
'18:30',
'19:00',
'19:30',
'20:00',
'20:30',
]

willingness_scores = ['VERY_WILLING', 'WILLING', 'UNWILLING', 'NO']
able_to_teach_scores = ['ABLE', 'WITH_EFFORT','NO']

non_teaching_semester = ['FALL', 'SPRING', 'SUMMER']
course_day_spread = ['TWF', 'MTh']

def get_randomized_time_ranges():
    '''
    Returns randomized time ranges
    '''
    time_range = ''
    range_start = 0 # 8:30
    range_end = 22 # 20:30
    end_of_start_times = 20 # 7:00, last time class should ever START
    max_time_range = random.randint(1, 3) # how many different time ranges will the prof give
    range_counter = 0
    while(range_start <= end_of_start_times and range_counter < max_time_range):
        # try to push the starting values earlier to make it more realistic
        earliest_start_time_list = [random.randint(range_start, end_of_start_times), \
            random.randint(range_start, end_of_start_times), \
            random.randint(range_start, end_of_start_times)]
        start_time = min(earliest_start_time_list)
        end_time = random.randint(start_time+2, range_end)
        time_range += f'("{time_slots[start_time]}" "{time_slots[end_time]}") '
        range_start = end_time + 1
        range_counter += 1

    # get anything that slips through the cracks
    if len(time_range) == 0:
        time_range += f'(\"{time_slots[range_start]}\" \"{time_slots[range_end]}\") '

    return [time_range]

def get_course_preferences():#(is_peng):
    '''
    returns course prefs
    '''
    course_preferences = []
    with open('curr_courses.json', encoding='utf-8') as file_handle:
        all_courses = json.load(file_handle)
    for course in all_courses:
        #randomly make it so most course have 0's and dont get added to prof,
        #probably a better way to do this
        enter = [random.randint(0, 6), random.randint(0, 6), random.randint(0, 6)]
        if 0 not in enter:
            # enthusiasm_score_index = random.randint(1, 6)
            preference = {}
            preference['course_id'] = course['id']
            preference['will_to_teach'] = willingness_scores[random.randint(0,3)]
            preference['able_to_teach'] = able_to_teach_scores[random.randint(0,2)]
            course_preferences.append(preference)
    return course_preferences

def get_day_times():
    '''
    returns dict of randomized day times
    '''
    day_times = {}
    day_times['mon'] = {'times':get_randomized_time_ranges(), 'preferredDay':True}
    day_times['tues'] = {'times':get_randomized_time_ranges(), 'preferredDay':True}
    day_times['wed'] = {'times':get_randomized_time_ranges(), 'preferredDay':True}
    day_times['thurs'] = {'times':get_randomized_time_ranges(), 'preferredDay':True}
    day_times['fri'] = {'times':get_randomized_time_ranges(), 'preferredDay':True}
    return day_times

def get_preferred_times():
    '''
    returns randomized dict of preferred times
    '''
    preferred_times = {}
    preferred_times['fall'] = get_day_times()
    preferred_times['spring'] = get_day_times()
    preferred_times['summer'] = get_day_times()
    return preferred_times

def get_preferred_non_teaching_semester():
    '''
    return randomized non teaching semester
    '''
    return non_teaching_semester[random.randint(0, 2)]

def get_preferred_course_day_spread():
    '''
    Returns randomized course day spread
    '''
    return course_day_spread[random.randint(0, 1)]

def sanitize_professors(professors):
    '''
    Returns a list of professor preferences that have been checked to make sure that each course
    is covered by a professor.
    '''
    with open('curr_courses.json', encoding='utf-8') as file_handle:
        all_courses = json.load(file_handle)
    for course in all_courses:
        course_covered = False
        for prof in professors:
            for pref in prof['course_preferences']:
                if pref['course_id'] == course['id'] and \
                    (pref['able_to_teach'] == 'ABLE' or pref['able_to_teach'] == 'WITH_EFFORT') \
                    and \
                    (pref['will_to_teach'] == 'VERY_WILLING' or pref['will_to_teach'] =='WILLING'):
                    course_covered = True

        if not course_covered:
            print(course['course_code'], 'not covered. Fixing.')
            pref = {}
            pref['course_id'] = course['id']
            pref['will_to_teach'] = willingness_scores[0]
            pref['able_to_teach'] = able_to_teach_scores[0]

            lucky_prof_index = random.randint(0, len(professors) - 1)
            professors[lucky_prof_index]['course_preferences'].append(pref)

    return professors

def post_prefs():
    '''
    Posts prefs for all profs in curr_professors.json
    '''
    base_url = 'http://127.0.0.1:5000/professors'
    with open('curr_professors.json', encoding='utf-8') as file_handle:
        professors = json.load(file_handle)

    finished_professors = []
    for prof in professors:
        prefs = {}
        prefs['year'] = 2022
        prefs['num_relief'] = random.randint(0,2)
        prefs['num_summer_courses'] = random.randint(0,2)
        prefs['num_fall_courses'] = random.randint(0,2)
        prefs['num_spring_courses'] = random.randint(0,2)
        prefs['why_relief'] ='temp'
        prefs['preferred_times'] = get_preferred_times()
        prefs['course_preferences'] = get_course_preferences()#(prof['is_peng'])
        if prefs['num_summer_courses'] == 0:
            prefs['semester_off'] = 3
        elif prefs['num_fall_courses'] == 0:
            prefs['semester_off'] = 1
        elif prefs['num_spring_courses'] == 0:
            prefs['semester_off'] = 2
        else:
            prefs['semester_off'] = 0
        finished_professors.append(prefs)

    finished_professors = sanitize_professors(finished_professors)

    for i, prof in enumerate(finished_professors):
        prof_id = professors[i]['id']
        url = f'{base_url}/{prof_id}/preferences'
        res = requests.post(url, json=prof)
        print(res.text)

post_prefs()
