from flask import Blueprint, jsonify
professor_bp = Blueprint('professor', __name__)
@professor_bp.route('/hello/')
def hello():
    return "Hello from Professors"
professors = [
    {'first_name':'Celina', 'last_name': 'Berg', 'uuid':'0e90ab30-c380-4034-acdb-238856a88df3'},
    {'first_name':'Bill', 'last_name': 'Bird', 'uuid': '8b8829ec-4615-4708-a0cd-5103f080ae56'},
    {'first_name':'Anthony', 'last_name': 'Estey', 'uuid':'6e46c60b-6709-4af5-ab4e-7a1c89c8ae0b'},
]
# returns all professors
@professor_bp.route('/', methods=['GET'])
def get_all_professors():
    return jsonify(professors),200

#returns a professor with an ID
@professor_bp.route('/<int:id>', methods=['GET'])
def get_professor(id):
    return jsonify(professors[id]),200

#returns all of professor's preferences
@professor_bp.route('/<int:id>/preferences', methods=['GET'])
def get_professor_preferences(id):
    return f'preferences of prof with id {id}',200

#returns a professor's preferences for a certain year
@professor_bp.route('/<int:id>/preferences/<int:preference_id>', methods=['GET'])
def get_professor_preference(id, preference_id):
    return f'prof with id {id} and preference id {preference_id}',200

# adds a new professor
@professor_bp.route('/', methods=['POST'])
def post_professor():
    return '',200

# adds a new professor's preferences
@professor_bp.route('/<int:id>/preferences', methods=['POST'])
def post_professor_preferences(id):
    return '',200

# updates a professor's preferences
@professor_bp.route('/<int:id>/preferences/<int:preference_id>', methods=['PUT'])
def update_professor_preferences(id, preference_id):
    return '',200

# deletes a professor
@professor_bp.route('/<int:id>', methods=['DELETE'])
def delete_professor(id):
    return '',200

# deletes a professor's preferences
@professor_bp.route('/<int:id>/preferences/<int:preference_id>', methods=['DELETE'])
def delete_professor_preferences(id, preference_id):
    return '',200