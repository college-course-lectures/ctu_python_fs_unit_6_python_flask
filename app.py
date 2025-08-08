#from tarfile import version
from logging import lastResort

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

@api.route('/enroll')
class EnrollStudent(Resource):
    @api.expect(student_model)
    def post(self):
        data = api.payload
        firstname = data['firstname']
        lastname = data['lastname']
        address = data['address']
        major_id = data['major_id']
        course_id = data['course_id']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (firstname, lastname,address,major_id,course_id) VALUES (%s, %s,%s,%s,%s)",
                       (firstname, lastname, address, major_id, course_id))
        conn.commit()
        student_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return {"message":  "Student enrolled successfully", "student_id": student_id}, 201



@api.route('/students')
class StudentList(Resource):
    def get(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT s.id, s.firstname, s.lastname, s.address, m.name AS major, c.name AS course
            FROM students s 
            JOIN majors m ON s.major_id = m.id
             JOIN courses c ON s.course_id = c.id""")
        students = cursor.fetchall()
        cursor.close()
        conn.close()
        return students



if __name__ == '__main__':
    app.run(port=8000)


