'''
starting point for API
'''
from flask import Flask

from .admin import ADMIN_BP
from .professor import PROFESSOR_BP
from .schedule import SCHEDULE_BP
from .course import COURSE_BP

APP = Flask(__name__)
@APP.route('/')
def index():
    '''
    sanity check endpoint
    '''
    return 'all is good :)'

@APP.after_request
def add_cors_headers(response):
    '''Allows frontend to connect to the backend.'''
    response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:3000')
    return response

APP.register_blueprint(ADMIN_BP, url_prefix='/admins')
APP.register_blueprint(PROFESSOR_BP, url_prefix='/professors')
APP.register_blueprint(SCHEDULE_BP, url_prefix='/schedule')
APP.register_blueprint(COURSE_BP, url_prefix='/courses')
APP.run()
