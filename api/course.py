from flask import Blueprint, request, jsonify
course_bp = Blueprint('course', __name__)
@course_bp.route('/hello/')
def hello():
    '''
    blah
    '''
    return 'Hello from Courses'
COURSES = [
    {
        'course_code': 'CSC111',
        'course_name': 'Fundamentals of C Programming',
        'uuid': '1e90ab30-c380-4034-acdb-238856a88df3',
        'min_offering': '3',
        'spring_required': True,
        'summer_required': False, 
        'fall_required': False,
        'spring_peng_req': False,
        'summer_peng_req': False,
        'fall_peng_req': False,
    },
    {
        'course_code': 'SENG275',
        'course_name': 'Zastre\'s favourite course',
        'uuid': '2e90ab30-c380-4034-acdb-238856a88df3',
        'min_offering': '2',
        'spring_required': True,
        'summer_required': True,
        'fall_required': False,
        'spring_peng_req': True,
        'summer_peng_req': True,
        'fall_peng_req': False,
    },
    {
        'course_code': 'CSC230',
        'course_name': 'Assembly ARM programming',
        'uuid': '3e90ab30-c380-4034-acdb-238856a88df3',
        'min_offering': '2',
        'spring_required': True,
        'summer_required': True,
        'fall_required': True,
        'spring_peng_req': False,
        'summer_peng_req': False,
        'fall_peng_req': False,
    },
]
UUIDS = [course['uuid'] for course in COURSES]

@course_bp.route('/', methods=['GET'])
def get_all_courses():
    # Return JSON object containing a list of courses and their course ids
    return jsonify(COURSES), 200

@course_bp.route('/<course_id>', methods=['GET'])
def get_course(course_id):
    # Return JSON object containing that course’s information
    if(course_id not in UUIDS):
        return 'couldn\'t find that course', 404
    
    return jsonify(COURSES[UUIDS.index(course_id)]), 200

@course_bp.route('/', methods=['POST'])
def add_course():
    # Request contains JSON object containing information about the course being posted
    # Add a new course to the table of courses
    # Returns new course’s id
    return f'course id of new entry\n\nJSON object:\n{request.data}\n\n', 200

@course_bp.route('/<course_id>', methods=['DELETE'])
def delete_course(course_id):
    # Deletes a course from the course table
    return f'deleted course {course_id}', 200

