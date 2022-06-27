'''
starting point for API
'''
import os
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
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

APP.register_blueprint(ADMIN_BP, url_prefix='/admins')
APP.register_blueprint(PROFESSOR_BP, url_prefix='/professors')
APP.register_blueprint(SCHEDULE_BP, url_prefix='/schedules')
APP.register_blueprint(COURSE_BP, url_prefix='/courses')

if __name__ == "__main__":
    port = int(os.environ.get('PORT',5000))
    APP.run(host="0.0.0.0",port=port,debug=True)
