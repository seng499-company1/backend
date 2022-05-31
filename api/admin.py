from flask import Blueprint
admin_bp = Blueprint('admin', __name__)
@admin_bp.route('/hello/')
def hello():
    return "Hello from Admins"