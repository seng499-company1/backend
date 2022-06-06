from flask import Flask

from .admin import admin_bp
from .professor import professor_bp
from .schedule import schedule_bp
from .course import course_bp

app = Flask(__name__)
@app.route('/')
def index():
    return 'all is good :)'

app.register_blueprint(admin_bp, url_prefix='/admins')
app.register_blueprint(professor_bp, url_prefix='/professors')
app.register_blueprint(schedule_bp, url_prefix='/schedule')
app.register_blueprint(course_bp, url_prefix='/courses')
app.run()