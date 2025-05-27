from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime

db = SQLAlchemy()

# Association table for many-to-many relationship between users and roles
roles_users = db.Table(
    'roles_users',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)

class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    desc = db.Column(db.Text)

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Integer, default=1)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=True)
    login_attempts = db.Column(db.Integer, default=0)

    roles = db.relationship('Role', secondary=roles_users, backref=backref('all_users', lazy='dynamic'))

    # Polymorphic inheritance (Student and Instructor inherit from Users)
    type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'users',
        'polymorphic_on': type
    }

class Student(Users):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=True)
    level = db.Column(db.String(20), nullable=True)
    weakness = db.Column(db.Text)
    total_CGPA = db.Column(db.Float)
    contact_info = db.Column(db.String(100))
    __mapper_args__ = {'polymorphic_identity': 'student'}

class Instructor(Users):
    __tablename__ = 'instructors'
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.String(50))
    qualification = db.Column(db.String(100))
    contact_info = db.Column(db.String(100))
    __mapper_args__ = {'polymorphic_identity': 'instructor'}

class Course(db.Model):
    __tablename__ = 'courses'
    course_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.Text)
    course_code= db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    term_name = db.Column(db.String(50))

class CourseStudent(db.Model):
    __tablename__ = 'course_students'
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), primary_key=True)
    total_mark = db.Column(db.Float)

class InstructorCourse(db.Model):
    __tablename__ = 'instructor_courses'
    instcourse_id = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.instructor_id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'))

class Assignment(db.Model):
    __tablename__ = 'assignments'
    assignment_id = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.instructor_id'))
    due_date = db.Column(db.DateTime)
    week_no = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'))

class Question(db.Model):
    __tablename__ = 'questions'
    question_id = db.Column(db.Integer, primary_key=True)
    stmt = db.Column(db.Text, nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.assignment_id'))
    tags = db.Column(db.String(100))

class QuestionChoice(db.Model):
    __tablename__ = 'question_choices'
    choice_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    is_right_choice = db.Column(db.Boolean, default=False)
    choice_stmt = db.Column(db.Text)

class UserQuestionAnswer(db.Model):
    __tablename__ = 'user_question_answers'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'), primary_key=True)
    choice_id = db.Column(db.Integer, db.ForeignKey('question_choices.choice_id'))
    is_right = db.Column(db.Boolean, default=False)

class Week(db.Model):
    __tablename__ = 'weeks'
    week_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'))
    week_no = db.Column(db.Integer)

class Video(db.Model):
    __tablename__ = 'videos'
    video_id = db.Column(db.Integer, primary_key=True)
    week_id = db.Column(db.Integer, db.ForeignKey('weeks.week_id'))
    video_no = db.Column(db.Integer)
    title = db.Column(db.String(255))
    video_url = db.Column(db.String(255))
    transcript = db.Column(db.Text)
    tags = db.Column(db.String(255))

class Submission(db.Model):
    __tablename__ = 'submissions'
    submission_id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.assignment_id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    marks = db.Column(db.Float)
    time = db.Column(db.DateTime, default=datetime)