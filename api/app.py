'''
starting point for API
'''
import os
from flask import Flask
from flask_cors import CORS

from .admin import ADMIN_BP
from .professor import PROFESSOR_BP
from .schedule import SCHEDULE_BP
from .course import COURSE_BP
from .login import LOGIN_BP

APP = Flask(__name__)
CORS(APP)
@APP.route('/')
def index():
    '''
    sanity check endpoint
    '''
    return 'all is good :)'

APP.register_blueprint(ADMIN_BP, url_prefix='/admins')
APP.register_blueprint(PROFESSOR_BP, url_prefix='/professors')
APP.register_blueprint(SCHEDULE_BP, url_prefix='/schedules')
APP.register_blueprint(COURSE_BP, url_prefix='/courses')
APP.register_blueprint(LOGIN_BP, url_prefix='/login')

if __name__ == "__main__":
    port = int(os.environ.get('PORT',5000))
    APP.run(host="0.0.0.0",port=port,debug=True)
