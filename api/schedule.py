from flask import Blueprint
schedule_bp = Blueprint('schedule', __name__)
@schedule_bp.route('/hello/')
def hello():
    return "Hello from Schedules"