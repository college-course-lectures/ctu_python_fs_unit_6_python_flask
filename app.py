#from tarfile import version

from flask import Flask
from flask_restx import Api, Resource, fields
from models import get_db_connection

app = Flask(__name__)
api = Api(app, version='1.0', title='ABC University Admissions API', description='RESTful API for enrolling students with OpenAPI docs.')

#Model for input validation and Swagger docs

student_model = api.model('Student', {
    'firstname': fields.String(required=True, description='First name'),
    'lastname': fields.String(required=True, description='Last name'),
    'address': fields.String(required=True, description='Address'),
    'major_id': fields.Integer(required=True, description='Major ID'),
    'course_id': fields.Integer(required=True, description='Course ID'),

})

@api.route('/majors')
class MajorsList(Resource):
    def get(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM majors")
        majors = cursor.fetchall()
        cursor.close()
        conn.close()
        return majors

@api.route('/courses')
class CoursesList(Resource):
    def get(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()
        cursor.close()
        conn.close()
        return courses


if __name__ == '__main__':
    app.run(port=8000)


