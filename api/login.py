'''
Contains the /login endpoint.

This can really be thought of as a throw away file which was implemented purely for demo purposes.
In reality if/when this system is used by UVic they will use the netlink system for login, which
will render this file obsolete. So, all this file aims to do is provide an easy way for our app to
provide netlink-like login services at the surface level, without any of the accompanying security.
'''
from flask import Blueprint, request, jsonify
from .dbconn import DB_CONN

LOGIN_BP = Blueprint('login', __name__)

def get_user_id(table, user):
    '''
    Gets a user's id from a specific table.
    '''
    sql = f"SELECT BIN_TO_UUID(id) as id FROM {table} WHERE email LIKE \"{user}@%\" LIMIT 1;"
    u_id = DB_CONN.select_one(sql)
    return None if not u_id else u_id.get_json()['id']

@LOGIN_BP.route('/', methods=['POST'])
def login():
    '''
    Authenticates a user.
    '''
    data = request.json

    if data['password'] != 'password':
        return 'authentication failed', 401

    u_id = get_user_id('Admin', data['username'])
    if u_id:
        return jsonify({"id": u_id, "permissions": "admin"}), 200

    u_id = get_user_id('Professor', data['username'])
    if u_id:
        return jsonify({"id": u_id, "permissions": "professor"}), 200

    return 'authentication failed', 401
