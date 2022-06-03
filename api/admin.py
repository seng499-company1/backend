from flask import Blueprint, jsonify
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/hello/')
def hello():
<<<<<<< HEAD
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
=======
    return "Hello from Admins", 200
admins = [
        {'uuid': 'd86a6640-d267-42f0-9dcd-8c0d06bf884c', 'first_name':'Rich', 'last_name':'Little', 'email':'richlittle@uvic.ca'},
        {'uuid': 'ace7c38c-a6dd-467a-b73f-aaaafe9a38b2', 'first_name':'Dan', 'last_name': 'Mai', 'email':'danmai@uvic.ca'}
    ]
uuids = [admin['uuid'] for admin in admins]
# returns all admins and their URIs
@admin_bp.route('/', methods=['GET'])
def get_all_admins():
    return jsonify(admins), 200
    
# returns a specific professor's account information
@admin_bp.route('/<id>', methods=['GET'])
def get_admin(id):
    print(id)
    if id not in uuids:
        return 'id not valid', 404
    else:
        return jsonify(admins[uuids.index(id)]), 200

# posts a new professor
@admin_bp.route('/', methods=['POST'])
def post_admin():
    return 'added user ',200

# deletes an admin from the admin table
@admin_bp.route('/<id>', methods=['DELETE'])
def delete_admin(id):
    return f'deleted user with id {id}',200
>>>>>>> 4777b19ab4e3aba98baa4efa4581741cebf6b7c4
