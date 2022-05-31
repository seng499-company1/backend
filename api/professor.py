from flask import Blueprint
professor_bp = Blueprint('professor', __name__)
@professor_bp.route('/hello/')
def hello():
    return "Hello from Professors"