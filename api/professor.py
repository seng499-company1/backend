from flask import Blueprint, jsonify
professor_bp = Blueprint('professor', __name__)
@professor_bp.route('/hello/')
def hello():
    return "Hello from Professors"
professors = [
    {'first_name':'Celina', 'last_name': 'Berg', 'uuid':'0e90ab30-c380-4034-acdb-238856a88df3', 'department':'CSC', 'is_teaching':True,'email':'email@uvic.ca' },
    {'first_name':'Bill', 'last_name': 'Bird', 'uuid': '8b8829ec-4615-4708-a0cd-5103f080ae56','department':'CSC', 'is_teaching':True,'email':'email@uvic.ca' },
    {'first_name':'Anthony', 'last_name': 'Estey', 'uuid':'6e46c60b-6709-4af5-ab4e-7a1c89c8ae0b','department':'CSC', 'is_teaching':True,'email':'email@uvic.ca' },
]
reliefs = [
    {'prof_id':'0e90ab30-c380-4034-acdb-238856a88df3', 'id':1, 'year':2022, 'num_relief': 2, 'num_summer_courses':1, 'num_fall_courses':1, 'num_spring_courses':2},
    {'prof_id':'8b8829ec-4615-4708-a0cd-5103f080ae56', 'id':2, 'year':2022, 'num_relief': 2, 'num_summer_courses':1, 'num_fall_courses':1, 'num_spring_courses':2},
    {'prof_id':'6e46c60b-6709-4af5-ab4e-7a1c89c8ae0b', 'id':3, 'year':2022, 'num_relief': 2, 'num_summer_courses':1, 'num_fall_courses':1, 'num_spring_courses':2},
]
uuids = [prof['uuid'] for prof in professors]
# returns all professors
@professor_bp.route('/', methods=['GET'])
def get_all_professors():
    return jsonify(professors),200

#returns a professor with an ID
@professor_bp.route('/<id>', methods=['GET'])
def get_professor(id):
    return jsonify(professors[uuids.index(id)]),200

#returns all of professor's preferences
@professor_bp.route('/<id>/preferences', methods=['GET'])
def get_professor_preferences(id):
    return jsonify(reliefs[uuids.index(id)]),200

#returns a professor's preferences for a certain year
@professor_bp.route('/<id>/preferences/<preference_id>', methods=['GET'])
def get_professor_preference(id, preference_id):
    if reliefs[uuids.index(id)]['id'] != int(preference_id):
        return 'couldn\'t find that preference id', 404
    else:
        return jsonify(reliefs[uuids.index(id)]),200

# adds a new professor
@professor_bp.route('/', methods=['POST'])
def post_professor():
    return 'posted a professor',200

# adds a new professor's preferences
@professor_bp.route('/<id>/preferences', methods=['POST'])
def post_professor_preferences(id):
    return f'updates a prof with id {id}',200

# updates a professor's preferences
@professor_bp.route('/<id>/preferences/<preference_id>', methods=['PUT'])
def update_professor_preferences(id, preference_id):
    return f'updates the preferences with id {preference_id} for professor with id {id}',200

# deletes a professor
@professor_bp.route('/<id>', methods=['DELETE'])
def delete_professor(id):
    return f'deleted prof with id {id}',200

# deletes a professor's preferences
@professor_bp.route('/<id>/preferences/<preference_id>', methods=['DELETE'])
def delete_professor_preferences(id, preference_id):
    return f'deleted preference with id {preference_id} for professor with id {id}',200