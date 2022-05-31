from flask import Blueprint
course_bp = Blueprint('course', __name__)
@course_bp.route('/hello/')
def hello():
    return "Hello from Courses"