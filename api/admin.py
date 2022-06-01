from flask import Blueprint, jsonify
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/hello/')
def hello():
    return "Hello from Admins", 200

# returns all admins and their URIs
@admin_bp.route('/', methods=['GET'])
def get_all_admins():
    admins = [
        {'vnumber':'V000000', 'uuid': 'd86a6640-d267-42f0-9dcd-8c0d06bf884c' },
        {'vnumber':'V000001', 'uuid': 'ace7c38c-a6dd-467a-b73f-aaaafe9a38b2' },
        {'vnumber':'V000002', 'uuid': 'd016e806-0b2f-405f-be41-2538bdd409a0' }
    ]
    return jsonify(admins), 200
    
# returns a specific professor's account information
@admin_bp.route('/<int:id>', methods=['GET'])
def get_admin(id):
    return jsonify(id), 200

# posts a new professor
@admin_bp.route('/', methods=['POST'])
def post_admin():
    return '',200

# deletes an admin from the admin table
@admin_bp.route('/<int:id>', methods=['DELETE'])
def delete_admin():
    return jsonify(id),200
