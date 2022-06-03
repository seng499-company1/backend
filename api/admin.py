from flask import Blueprint, jsonify
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/hello/')
def hello():
    '''
    says hello
    '''
    return "Hello from Admins", 200
ADMINS = [
        {'uuid': 'd86a6640-d267-42f0-9dcd-8c0d06bf884c', 'first_name':'Rich', 'last_name':'Little',
         'email':'richlittle@uvic.ca'},
        {'uuid': 'ace7c38c-a6dd-467a-b73f-aaaafe9a38b2', 'first_name':'Dan', 'last_name': 'Mai',
         'email':'danmai@uvic.ca'}
    ]
UUIDS = [admin['uuid'] for admin in ADMINS]

@admin_bp.route('/', methods=['GET'])
def get_all_admins():
    '''
    returns all ADMINS and their URIs
    '''
    return jsonify(ADMINS), 200

@admin_bp.route('/<admin_id>', methods=['GET'])
def get_admin(admin_id):
    '''
    returns a specific professor's account information
    '''
    if admin_id not in UUIDS:
        return 'id not valid', 404
    else:
        return jsonify(ADMINS[UUIDS.index(admin_id)]), 200

@admin_bp.route('/', methods=['POST'])
def post_admin():
    '''
    posts a new admin
    '''
    return 'added user ', 200

@admin_bp.route('/<admin_id>', methods=['DELETE'])
def delete_admin(admin_id):
    '''
    deletes an admin from the admin table
    '''
    return f'deleted user with id {admin_id}', 200
