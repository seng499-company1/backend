from flask import Flask

from admin import ADMIN_BP
from professor import PROFESSOR_BP
from schedule import SCHEDULE_BP
from course import COURSE_BP

app = Flask(__name__)
@app.route('/')
def index():
    return 'all is good :)'

app.register_blueprint(ADMIN_BP, url_prefix='/admins')
app.register_blueprint(PROFESSOR_BP, url_prefix='/professors')
app.register_blueprint(SCHEDULE_BP, url_prefix='/schedule')
app.register_blueprint(COURSE_BP, url_prefix='/courses')
app.run()