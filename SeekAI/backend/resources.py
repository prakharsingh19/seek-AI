# from flask import jsonify, request, current_app as app
# from flask_restful import Api, Resource, reqparse
# from flask_security import auth_required, current_user
# from flask_security import auth_required, roles_required
# from genAI.chat import chat
# from model import (
#     Users,
#     Instructor,
#     Student,
#     Course,
#     Week,
#     Video,
#     Assignment,
#     InstructorCourse,
#     CourseStudent,
#     Question,
#     UserQuestionAnswer,
#     Submission,
#     QuestionChoice,
#     db,
# )
# from sqlalchemy import func
# from datetime import datetime
# import google.generativeai as genai
# from youtube_transcript_api import YouTubeTranscriptApi
# import re

# # Initialize API with prefix
# api = Api(prefix="/api")
# genai.configure(api_key="AIzaSyCOH6hPYZ3prjUiUO-e0JGct41CMpj2gNQ")


# def extract_video_id(url):
#     """Extracts video ID from a given YouTube URL."""
#     pattern = r"(?:https?:\/\/)?(?:www\.|m\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]{11})"
#     match = re.search(pattern, url)
#     return match.group(1) if match else None

# # ---------- Student Resources ----------


# class StudentsByCourse(Resource):
#     # @auth_required("token")
#     def get(self, course_id):
#         students_in_course = (
#             db.session.query(Student)
#             .join(CourseStudent, Student.student_id == CourseStudent.student_id)
#             .filter(CourseStudent.course_id == course_id)
#             .all()
#         )

#         result = []
#         for student in students_in_course:
#             enrolled_courses = (
#                 db.session.query(CourseStudent.course_id)
#                 .filter(CourseStudent.student_id == student.student_id)
#                 .all()
#             )
#             # Convert list of one-tuples to a plain list of ids.
#             enrolled_courses = [course_id for (course_id,) in enrolled_courses]

#             result.append(
#                 {
#                     "student_id": student.student_id,
#                     "first_name": student.first_name,
#                     "last_name": student.last_name,
#                     "level": student.level,
#                     "total_CGPA": student.total_CGPA,
#                     "weakness": student.weakness,
#                     "contact_info": student.contact_info,
#                     "email": student.email,
#                     # Optionally, include all enrolled course IDs:
#                     #'enrolled_courses': enrolled_courses
#                 }
#             )
#         return result, 200


# class StudentDetail(Resource):
#     # @auth_required("token")
#     def get(self, student_id):
#         student = Student.query.filter_by(student_id=student_id).first()
#         if not student:
#             return {"message": "Student not found"}, 404

#         # Build a list of course_ids the student is enrolled in using CourseStudent.
#         enrolled_courses = (
#             db.session.query(CourseStudent.course_id)
#             .filter(CourseStudent.student_id == student.student_id)
#             .all()
#         )
#         enrolled_courses = [course_id for (course_id,) in enrolled_courses]

#         data = {
#             "student_id": student.student_id,
#             "first_name": student.first_name,
#             "last_name": student.last_name,
#             "level": student.level,
#             "total_CGPA": student.total_CGPA,
#             "weakness": student.weakness,
#             "contact_info": student.contact_info,
#             "email": student.email,
#             "enrolled_courses": enrolled_courses,
#         }
#         return data, 200


# # ---------- Instructor Resources ----------


# class InstructorsList(Resource):
#     # @auth_required("token")
#     def get(self):
#         instructors = Instructor.query.all()
#         result = []
#         for inst in instructors:
#             result.append(
#                 {
#                     "instructor_id": inst.instructor_id,
#                     "name": inst.name,
#                     "experience": inst.experience,
#                     "qualification": inst.qualification,
#                     "contact_info": inst.contact_info,
#                     "email": inst.email,
#                 }
#             )
#         return result, 200


# class InstructorDetail(Resource):
#     # @auth_required("token")
#     def get(self, instructor_id):
#         inst = Instructor.query.filter_by(instructor_id=instructor_id).first()
#         if not inst:
#             return {"message": "Instructor not found"}, 404

#         data = {
#             "instructor_id": inst.instructor_id,
#             "name": inst.name,
#             "experience": inst.experience,
#             "qualification": inst.qualification,
#             "contact_info": inst.contact_info,
#             "email": inst.email,
#         }
#         return data, 200


# # ---------- Courses Resources ----------


# class CoursesList(Resource):
#     # @auth_required("token")
#     def get(self):
#         courses = Course.query.all()
#         result = []
#         for course in courses:
#             # Get associated instructor(s) via InstructorCourse table.
#             instructor_ids = [
#                 inst
#                 for (inst,) in db.session.query(InstructorCourse.instructor_id)
#                 .filter_by(course_id=course.course_id)
#                 .all()
#             ]
#             result.append(
#                 {
#                     "course_id": course.course_id,
#                     "instructor_ids": instructor_ids,
#                     "name": course.name,
#                     "desc": course.desc,
#                     "course_code": course.course_code,
#                     "term_name": course.term_name,
#                     "created_at": course.created_at.strftime("%Y-%m-%d %H:%M:%S")
#                     if course.created_at
#                     else None,
#                 }
#             )
#         return result, 200


# class CoursesByStudent(Resource):
#     # @auth_required("token")
#     def get(self, student_id):
#         student = Student.query.filter_by(student_id=student_id).first()
#         if not student:
#             return {"message": "Student not found"}, 404

#         # Use the CourseStudent mapping table to find courses the student is enrolled in.
#         course_ids = [
#             cid
#             for (cid,) in db.session.query(CourseStudent.course_id)
#             .filter_by(student_id=student.student_id)
#             .all()
#         ]
#         courses = (
#             Course.query.filter(Course.course_id.in_(course_ids)).all()
#             if course_ids
#             else []
#         )
#         result = []
#         for course in courses:
#             instructor_ids = [
#                 inst
#                 for (inst,) in db.session.query(InstructorCourse.instructor_id)
#                 .filter_by(course_id=course.course_id)
#                 .all()
#             ]
#             result.append(
#                 {
#                     "course_id": course.course_id,
#                     "instructor_ids": instructor_ids,
#                     "name": course.name,
#                     "desc": course.desc,
#                     "course_code": course.course_code,
#                     "term_name": course.term_name,
#                     "created_at": course.created_at.strftime("%Y-%m-%d %H:%M:%S")
#                     if course.created_at
#                     else None,
#                 }
#             )
#         return result, 200


# class CoursesByInstructor(Resource):
#     # @auth_required("token")
#     def get(self, instructor_id):
#         # Use the InstructorCourse mapping table to find course IDs linked to the instructor.
#         course_ids = [
#             cid
#             for (cid,) in db.session.query(InstructorCourse.course_id)
#             .filter_by(instructor_id=instructor_id)
#             .all()
#         ]
#         courses = (
#             Course.query.filter(Course.course_id.in_(course_ids)).all()
#             if course_ids
#             else []
#         )
#         result = []
#         for course in courses:
#             instructor_ids = [
#                 inst
#                 for (inst,) in db.session.query(InstructorCourse.instructor_id)
#                 .filter_by(course_id=course.course_id)
#                 .all()
#             ]
#             result.append(
#                 {
#                     "course_id": course.course_id,
#                     "instructor_ids": instructor_ids,
#                     "name": course.name,
#                     "desc": course.desc,
#                     "course_code": course.course_code,
#                     "term_name": course.term_name,
#                     "created_at": course.created_at.strftime("%Y-%m-%d %H:%M:%S")
#                     if course.created_at
#                     else None,
#                 }
#             )
#         return result, 200


# class CourseManagement(Resource):
#     # @auth_required("token")
#     # @roles_required("administrator")
#     def put(self, course_id=None):
#         parser = reqparse.RequestParser()
#         # Although the original endpoint expected instructor_id, title and name,
#         # our Course model has name and desc. We map:
#         #   name -> Course.name
#         #   title -> Course.desc
#         # The instructor mapping is stored in the InstructorCourse table.
#         parser.add_argument(
#             "instructor_id", type=int, required=True, help="Instructor ID is required"
#         )
#         parser.add_argument(
#             "name", type=str, required=True, help="Course name is required"
#         )
#         parser.add_argument(
#             "desc", type=str, required=True, help="Course description is required"
#         )
#         # Optional fields
#         parser.add_argument("course_code", type=str)
#         parser.add_argument("term_name", type=str)
#         data = parser.parse_args()

#         if course_id:
#             course = Course.query.get(course_id)
#             if not course:
#                 return {"message": "Course not found"}, 404
#             course.name = data["name"]
#             course.desc = data["desc"]
#             course.course_code = data.get("course_code")
#             course.term_name = data.get("term_name")
#             # Optionally update created_at; though typically creation time is not updated.
#             course.created_at = datetime.utcnow()
#             message = "Course updated"
#         else:
#             course = Course(
#                 name=data["name"],
#                 desc=data["desc"],
#                 course_code=data.get("course_code"),
#                 term_name=data.get("term_name"),
#                 created_at=datetime.utcnow(),
#             )
#             db.session.add(course)
#             message = "Course created"
#             # Flush to get a course_id assigned.
#             db.session.flush()

#         # Manage the instructor mapping via InstructorCourse.
#         # Try to get an existing mapping for this course.
#         instructor_mapping = InstructorCourse.query.filter_by(
#             course_id=course.course_id
#         ).first()
#         if instructor_mapping:
#             instructor_mapping.instructor_id = data["instructor_id"]
#         else:
#             new_mapping = InstructorCourse(
#                 instructor_id=data["instructor_id"], course_id=course.course_id
#             )
#             db.session.add(new_mapping)

#         db.session.commit()
#         return {"message": message, "course_id": course.course_id}, 200

#     # @auth_required("token")
#     # @roles_required("administrator")
#     def delete(self, course_id):
#         course = Course.query.get(course_id)
#         if not course:
#             return {"message": "Course not found"}, 404

#         # Remove related InstructorCourse entries first.
#         InstructorCourse.query.filter_by(course_id=course.course_id).delete()
#         # Optionally remove related CourseStudent entries.
#         CourseStudent.query.filter_by(course_id=course.course_id).delete()

#         db.session.delete(course)
#         db.session.commit()
#         return {"message": "Course deleted"}, 200


# # ---------- Video Resources ----------


# class VideosByCourse(Resource):
#     @auth_required("token")
#     def get(self, course_id):
#         # Join Video with Week by matching week_id to filter videos for the given course.
#         videos = (
#             Video.query.join(Week, Video.week_id == Week.week_id)
#             .filter(Week.course_id == course_id)
#             .all()
#         )
#         result = [
#             {
#                 "video_id": video.video_id,
#                 "week_id": video.week_id,
#                 "video_no": video.video_no,
#                 "title": video.title,
#                 "video_url": video.video_url,
#             }
#             for video in videos
#         ]
#         return result, 200


# class AddVideoToCourseWeek(Resource):
#     @auth_required("token")
#     def post(self, course_id, week_number):
#         # Get the data from the request body
#         data = request.get_json()

#         # Validate required fields
#         required_fields = ["video_no", "title", "video_url"]
#         for field in required_fields:
#             if field not in data:
#                 return {"message": f"'{field}' is required"}, 400

#         # Find the week based on course_id and week_number
#         week = Week.query.filter_by(course_id=course_id, week_no=week_number).first()

#         if not week:
#             return {"message": "Week not found"}, 404

#         # Create a new video entry in the database
#         new_video = Video(
#             week_id=week.week_id,
#             video_no=data["video_no"],
#             title=data["title"],
#             video_url=data["video_url"],
#             # Optional: set a timestamp for when the video is added
#             added_on=datetime.utcnow(),
#         )

#         try:
#             # Save the video to the database
#             db.session.add(new_video)
#             db.session.commit()
#             return {
#                 "message": "Video added successfully",
#                 "video_id": new_video.video_id,
#             }, 201
#         except Exception as e:
#             db.session.rollback()
#             return {
#                 "message": f"An error occurred while adding the video: {str(e)}"
#             }, 500


# class VideosByCourseWeek(Resource):
#     # @auth_required("token")
#     def get(self, course_id, week_number):
#         # Adjust filtering as our Week model uses "week_no"
#         week = Week.query.filter_by(course_id=course_id, week_no=week_number).first()
#         if not week:
#             return {"message": "Week not found"}, 404
#         # Query videos that belong to the found week.
#         videos = Video.query.filter_by(week_id=week.week_id).all()
#         result = [
#             {
#                 "video_id": video.video_id,
#                 "week_id": video.week_id,
#                 "video_no": video.video_no,
#                 "title": video.title,
#                 "video_url": video.video_url,
#             }
#             for video in videos
#         ]
#         return result, 200


# class VideoDetail(Resource):
#     @auth_required("token")
#     def get(self, video_id):
#         video = Video.query.filter_by(video_id=video_id).first()
#         if not video:
#             return {"message": "Video not found"}, 404

#         data = {
#             "video_id": video.video_id,
#             "week_id": video.week_id,
#             "video_no": video.video_no,
#             "title": video.title,
#             "video_url": video.video_url,
#             "transcript": video.transcript,
#             "tags": video.tags,
#         }
#         return data, 200


# class VideoManagement(Resource):
#     # @auth_required("token")
#     def post(self):
#         """Create a new video."""
#         data = request.json
#         if not data:
#             return {"message": "No data provided"}, 400

#         required_fields = ["week_id", "video_no", "title", "video_url"]
#         if not all(field in data for field in required_fields):
#             return {"message": "Missing required fields"}, 400

#         video = Video(
#             week_id=data["week_id"],
#             video_no=data["video_no"],
#             title=data["title"],
#             video_url=data["video_url"],
#             transcript=data.get("transcript", ""),
#             tags=data.get("tags", ""),
#         )

#         db.session.add(video)
#         db.session.commit()

#         return {
#             "video_id": video.video_id,
#             "week_id": video.week_id,
#             "video_no": video.video_no,
#             "title": video.title,
#             "video_url": video.video_url,
#             "transcript": video.transcript,
#             "tags": video.tags,
#         }, 201

#     # @auth_required("token")
#     def put(self, video_id):
#         """Update an existing video."""
#         video = Video.query.filter_by(video_id=video_id).first()
#         if not video:
#             return {"message": "Video not found"}, 404

#         data = request.json
#         if not data:
#             return {"message": "No data provided"}, 400

#         video.week_id = data.get("week_id", video.week_id)
#         video.video_no = data.get("video_no", video.video_no)
#         video.title = data.get("title", video.title)
#         video.video_url = data.get("video_url", video.video_url)
#         video.transcript = data.get("transcript", video.transcript)
#         video.tags = data.get("tags", video.tags)

#         db.session.commit()

#         return {
#             "video_id": video.video_id,
#             "week_id": video.week_id,
#             "video_no": video.video_no,
#             "title": video.title,
#             "video_url": video.video_url,
#             "transcript": video.transcript,
#             "tags": video.tags,
#         }, 200

#     # @auth_required("token")
#     def delete(self, video_id):
#         """Delete a video."""
#         video = Video.query.filter_by(video_id=video_id).first()
#         if not video:
#             return {"message": "Video not found"}, 404

#         db.session.delete(video)
#         db.session.commit()

#         return {"message": "Video deleted successfully"}, 200


# # ---------- Assignment Resources ----------


# class AssignmentsByCourse(Resource):
#     # @auth_required("token")
#     def get(self, course_id):
#         # Join Assignment with Week to filter by course using Week.course_id.
#         assignments = (
#             Assignment.query.join(Week, Assignment.week_no == Week.week_no)
#             .filter(Week.course_id == course_id)
#             .all()
#         )
#         result = [
#             {
#                 "assignment_id": assign.assignment_id,
#                 "due_date": assign.due_date.strftime("%Y-%m-%d %H:%M:%S")
#                 if assign.due_date
#                 else None,
#                 "week_no": assign.week_no,
#                 "instructor_id": assign.instructor_id,
#                 "course_id": assign.course_id,
#             }
#             for assign in assignments
#         ]
#         return result, 200


# class AssignmentsByCourseWeek(Resource):
#     # @auth_required("token")
#     def get(self, course_id, week_number):
#         # Filter Week by course_id and week_no.
#         week = Week.query.filter_by(course_id=course_id, week_no=week_number).first()
#         if not week:
#             return {"message": "Week not found"}, 404

#         # Filter assignments by matching week_no and course_id.
#         assignments = Assignment.query.filter_by(
#             week_no=week_number, course_id=course_id
#         ).all()
#         result = [
#             {
#                 "assignment_id": assign.assignment_id,
#                 "due_date": assign.due_date.strftime("%Y-%m-%d %H:%M:%S")
#                 if assign.due_date
#                 else None,
#                 "week_no": assign.week_no,
#                 "instructor_id": assign.instructor_id,
#                 "course_id": assign.course_id,
#             }
#             for assign in assignments
#         ]
#         return result, 200


# class AssignmentManagement(Resource):
#     def post(self):
#         # Same logic as in the put method, for creating new assignments
#         parser = reqparse.RequestParser()
#         parser.add_argument(
#             "week_no", type=int, required=True, help="Week number is required"
#         )
#         parser.add_argument(
#             "course_id", type=int, required=True, help="Course ID is required"
#         )
#         parser.add_argument(
#             "due_date",
#             type=str,
#             required=False,
#             help="Due date in format YYYY-MM-DD HH:MM:SS",
#         )
#         parser.add_argument(
#             "instructor_id", type=int, required=True, help="Instructor ID is required"
#         )
#         data = parser.parse_args()

#         due_date_val = None
#         if data.get("due_date"):
#             try:
#                 due_date_val = datetime.strptime(data["due_date"], "%Y-%m-%d %H:%M:%S")
#             except ValueError:
#                 return {
#                     "message": "Invalid due_date format. Use YYYY-MM-DD HH:MM:SS"
#                 }, 400

#         # Create the assignment
#         assignment = Assignment(
#             week_no=data["week_no"],
#             course_id=data["course_id"],
#             instructor_id=data["instructor_id"],
#             due_date=due_date_val,
#         )
#         db.session.add(assignment)
#         db.session.flush()  # Flush to generate assignment_id
#         db.session.commit()

#         return {
#             "message": "Assignment created",
#             "assignment_id": assignment.assignment_id,
#         }, 201  # 201 for resource creation

#     def delete(self, assignment_id):
#         assignment = Assignment.query.get(assignment_id)
#         if not assignment:
#             return {"message": "Assignment not found"}, 404

#         db.session.delete(assignment)
#         db.session.commit()
#         return {"message": "Assignment deleted successfully"}, 200


# class AssignmentById(Resource):
#     def get(self, assignment_id):
#         assignment = Assignment.query.get(assignment_id)
#         if not assignment:
#             return {"message": "Assignment not found"}, 404

#         return {
#             "assignment_id": assignment.assignment_id,
#             "due_date": assignment.due_date.strftime("%Y-%m-%d %H:%M:%S")
#             if assignment.due_date
#             else None,
#             "week_no": assignment.week_no,
#             "course_id": assignment.course_id,
#             "instructor_id": assignment.instructor_id,
#             # Add any other assignment details you need
#         }, 200


# # ---------- Question Resources ----------


# class QuestionsByAssignment(Resource):
#     # @auth_required("token")
#     def get(self, assignment_id):
#         # Query all questions for the given assignment_id.
#         questions = Question.query.filter_by(assignment_id=assignment_id).all()
#         result = [
#             {
#                 "question_id": question.question_id,
#                 "stmt": question.stmt,
#                 "tags": question.tags,
#             }
#             for question in questions
#         ]
#         return result, 200


# class QuestionManagement(Resource):
#     # @auth_required("token")
#     # @roles_required("instructor")
#     def put(self, question_id=None):
#         parser = reqparse.RequestParser()
#         # Adjusted field names to match the models.py definition:
#         # Use 'stmt' for the question statement instead of 'type'
#         # and use 'tags' in place of 'correct_answer' if needed.
#         parser.add_argument(
#             "assignment_id", type=int, required=True, help="Assignment ID is required"
#         )
#         parser.add_argument(
#             "stmt", type=str, required=True, help="Question statement is required"
#         )
#         parser.add_argument(
#             "optionsStmt", type=str, required=True, help="Question options is required"
#         )
#         parser.add_argument("tags", type=str, required=False, help="Tags are optional")
#         data = parser.parse_args()

#         print(data)

#         if question_id:
#             question = Question.query.get(question_id)
#             if not question:
#                 return {"message": "Question not found"}, 404
#             question.assignment_id = data["assignment_id"]
#             question.stmt = data["stmt"]
#             question.tags = data.get("tags")
#             message = "Question updated"
#         else:
#             print(data)
#             question = Question(
#                 assignment_id=data["assignment_id"],
#                 stmt=data["stmt"],
#                 tags=data.get("tags"),
#             )
#             db.session.add(question)
#             message = "Question created"

#         db.session.commit()
#         return {"message": message, "question_id": question.question_id}, 200

#     # @auth_required("token")
#     # @roles_required("instructor")
#     def delete(self, question_id):
#         question = Question.query.get(question_id)
#         if not question:
#             return {"message": "Question not found"}, 404

#         db.session.delete(question)
#         db.session.commit()
#         return {"message": "Question deleted"}, 200

#     def post(self, question_id=None):
#         parser = reqparse.RequestParser()
#         parser.add_argument("assignment_id", type=int, required=True)
#         parser.add_argument("stmt", type=str, required=True)
#         parser.add_argument("optionsStmt", type=str, required=True)
#         parser.add_argument("tags", type=str, required=False)

#         data = parser.parse_args()

#         # Create the Question entry
#         question = Question(
#             assignment_id=data["assignment_id"],
#             stmt=data["stmt"],
#             tags=data.get("tags"),
#         )
#         db.session.add(question)
#         db.session.commit()  # Commit to generate question_id

#         # Split optionsStmt into individual choices
#         option_statements = [opt.strip() for opt in data["optionsStmt"].split(",")]

#         correct_index = int(option_statements.pop()) - 1

#         # Create QuestionChoice entries for each option
#         for index, option_stmt in enumerate(option_statements):
#             choice = QuestionChoice(
#                 question_id=question.question_id,
#                 choice_stmt=option_stmt,
#                 is_right_choice=(
#                     index == correct_index
#                 ),  # Defaulting to False, modify as needed
#             )
#             db.session.add(choice)

#         db.session.commit()  # Commit choices to the database

#         return {"message": "Question created", "question_id": question.question_id}, 201


# # ---------- Submission Resources ----------


# class SubmissionsByCourseWeek(Resource):
#     # @auth_required("token")
#     def get(self, course_id, week_number):
#         # Find the week using course_id and week_no (our Week model uses week_no)
#         week = Week.query.filter_by(course_id=course_id, week_no=week_number).first()
#         if not week:
#             return {"message": "Week not found"}, 404

#         # Get assignments for the specified course and week.
#         assignments = Assignment.query.filter_by(
#             course_id=course_id, week_no=week_number
#         ).all()
#         submissions_list = []
#         for assign in assignments:
#             # For each assignment, get its submissions.
#             submissions = Submission.query.filter_by(
#                 assignment_id=assign.assignment_id
#             ).all()
#             for sub in submissions:
#                 submissions_list.append(
#                     {
#                         "submission_id": sub.submission_id,
#                         "assignment_id": sub.assignment_id,
#                         "student_id": sub.student_id,
#                         "submitted_at": sub.time.strftime("%Y-%m-%d %H:%M:%S")
#                         if sub.time
#                         else None,
#                         "marks_obtained": sub.marks,
#                     }
#                 )
#         return submissions_list, 200


# class SubmissionsByCourse(Resource):
#     # @auth_required("token")
#     def get(self, course_id):
#         # Get all assignments under the given course.
#         assignments = Assignment.query.filter_by(course_id=course_id).all()
#         submissions_list = []
#         for assign in assignments:
#             submissions = Submission.query.filter_by(
#                 assignment_id=assign.assignment_id
#             ).all()
#             for sub in submissions:
#                 submissions_list.append(
#                     {
#                         "submission_id": sub.submission_id,
#                         "assignment_id": sub.assignment_id,
#                         "student_id": sub.student_id,
#                         "submitted_at": sub.time.strftime("%Y-%m-%d %H:%M:%S")
#                         if sub.time
#                         else None,
#                         "marks_obtained": sub.marks,
#                     }
#                 )
#         return submissions_list, 200


# class SubmissionManagement(Resource):
#     # @auth_required("token")
#     # @roles_required("student")
#     def put(self, assignment_id):
#         parser = reqparse.RequestParser()
#         parser.add_argument(
#             "marks_obtained", type=int, required=False, help="Marks obtained (optional)"
#         )
#         data = parser.parse_args()

#         # Get the current student id from the authenticated user.
#         # Assuming that the current_user is an instance of Student.
#         student_id = 7

#         # Check if the assignment exists.
#         assignment = Assignment.query.get(assignment_id)
#         if not assignment:
#             return {"message": "Assignment not found"}, 404

#         # Verify the student exists.
#         student = Users.query.get(student_id)
#         if not student:
#             return {"message": "Student not found"}, 404

#         # Check if a submission already exists for this assignment and student.
#         submission = Submission.query.filter_by(
#             assignment_id=assignment_id, student_id=student_id
#         ).first()
#         if submission:
#             # Update submission if it exists.
#             # Use provided marks_obtained as a placeholder, but then recalc marks.
#             submission.marks = data.get("marks_obtained", submission.marks)
#             submission.time = datetime.utcnow()
#             message = "Submission updated"
#         else:
#             submission = Submission(
#                 assignment_id=assignment_id,
#                 student_id=student_id,
#                 marks=data.get("marks_obtained"),
#             )
#             db.session.add(submission)
#             message = "Submission created"
#             db.session.flush()  # Ensure submission_id is assigned

#         # Calculate marks: (number of correct questions attempted by student) / (total number of questions)
#         total_questions = Question.query.filter_by(assignment_id=assignment_id).count()
#         correct_answers = (
#             UserQuestionAnswer.query.join(
#                 Question, UserQuestionAnswer.question_id == Question.question_id
#             )
#             .filter(
#                 Question.assignment_id == assignment_id,
#                 UserQuestionAnswer.user_id == student_id,
#                 UserQuestionAnswer.is_right is True,
#             )
#             .count()
#         )
#         calculated_marks = (
#             (correct_answers / total_questions) if total_questions > 0 else 0
#         )

#         # Here, we update the submission marks with the calculated value.
#         submission.marks = calculated_marks

#         # Optionally, store the calculated marks in a variable.
#         marks_obtained = calculated_marks

#         db.session.commit()
#         return {
#             "message": message,
#             "submission_id": submission.submission_id,
#             "marks_obtained": marks_obtained,
#         }, 200


# # Add to resources.py


# class WeeksByCourse(Resource):
#     # @auth_required("token")
#     def get(self, course_id):
#         weeks = Week.query.filter_by(course_id=course_id).order_by(Week.week_no).all()
#         return [
#             {
#                 "week_id": week.week_id,
#                 # "name": week.name,
#                 "week_no": week.week_no,
#                 "course_id": week.course_id,
#             }
#             for week in weeks
#         ], 200

#     # @auth_required("token")
#     # @roles_required("instructor")
#     def post(self, course_id):
#         parser = reqparse.RequestParser()
#         parser.add_argument("name", type=str, required=True)
#         parser.add_argument("week_no", type=int, required=True)
#         data = parser.parse_args()

#         if Week.query.filter_by(course_id=course_id, week_no=data["week_no"]).first():
#             return {"message": "Week number already exists in this course"}, 400

#         week = Week(course_id=course_id, week_no=data["week_no"])
#         db.session.add(week)
#         db.session.commit()
#         return {"message": "Week added", "week_id": week.week_id}, 201


# class WeekDetail(Resource):
#     # @auth_required("token")
#     # @roles_required("instructor")
#     def put(self, week_id):
#         parser = reqparse.RequestParser()
#         parser.add_argument("name", type=str)
#         parser.add_argument("week_no", type=int)
#         data = parser.parse_args()

#         week = Week.query.get(week_id)
#         if not week:
#             return {"message": "Week not found"}, 404

#         if data.get("week_no"):
#             existing = Week.query.filter_by(
#                 course_id=week.course_id, week_no=data["week_no"]
#             ).first()
#             if existing and existing.week_id != week_id:
#                 return {"message": "Week number already exists in this course"}, 400
#             week.week_no = data["week_no"]

#         if data.get("name"):
#             week.name = data["name"]

#         db.session.commit()
#         return {"message": "Week updated"}, 200

#     # @auth_required("token")
#     # @roles_required("instructor")
#     def delete(self, week_id):
#         week = Week.query.get(week_id)
#         if not week:
#             return {"message": "Week not found"}, 404

#         db.session.delete(week)
#         db.session.commit()
#         return {"message": "Week deleted"}, 200


# class ChoicesByQuestion(Resource):
#     # @auth_required('token')
#     def get(self, question_id):
#         # Query all choices for the given question_id.
#         choices = QuestionChoice.query.filter_by(question_id=question_id).all()

#         if not choices:
#             return {"message": "No choices found for this question"}, 404

#         result = [
#             {
#                 "choice_id": choice.choice_id,
#                 "choice_stmt": choice.choice_stmt,
#                 "is_right_choice": choice.is_right_choice,  # You might want to remove this if it should be hidden
#             }
#             for choice in choices
#         ]

#         return result, 200

# class QuestionHint(Resource):
#     def get(self, question_stmt):
#         try:
#             # Generate a hint using Gemini AI
#             prompt = f"Provide a helpful hint for the following question without revealing the direct answer: {question_stmt}"
#             model = genai.GenerativeModel("gemini-1.5-flash")
#             response = model.generate_content(prompt)
#             hint = response.text.strip()
            
#             return {"hint": hint}, 200
#         except Exception as e:
#             return {"error": str(e)}, 500


# class SummarizeVideo(Resource):
#     def get(self, video_id):
#         try:
#             # Fetch video object from DB using video_id
#             video = Video.query.get(video_id)
#             if not video:
#                 return {"error": "Video not found"}, 404
            
#             # If transcript is available, return it
#             if video.transcript:
#                 return {"summary": video.transcript}, 200
            
#             # If no transcript exists, fetch the transcript from YouTube
#             transcript_data = YouTubeTranscriptApi.get_transcript(video.video_url.split('=')[-1])  # Get video_id from URL
#             transcript = " ".join([t["text"] for t in transcript_data])

#             # Generate summary using Gemini
#             prompt = f"Summarize the following transcript of a YouTube lecture video:\n\n{transcript}"
#             model = genai.GenerativeModel("gemini-1.5-flash")
#             response = model.generate_content(prompt)
#             summary = response.text.strip()

#             # Store the generated summary in the database
#             video.transcript = summary
#             db.session.commit()

#             return {"summary": summary}, 200

#         except Exception as e:
#             return {"error": str(e)}, 500
        


# class ChatResource(Resource):
#     @auth_required('token')
#     def post(self):
#         data = request.get_json()
#         question = data.get("question")
#         answer= chat(question, current_user.user_id)
#         return {"message": answer}, 200

# api.add_resource(ChatResource, "/chat")


# api.add_resource(ChoicesByQuestion, "/questions/<int:question_id>/choices")

# # Add routes
# api.add_resource(WeeksByCourse, "/courses/<int:course_id>/weeks")
# api.add_resource(WeekDetail, "/weeks/<int:week_id>")


# # To add these resources to your API, for example:
# api.add_resource(StudentsByCourse, "/courses/<int:course_id>/students")
# api.add_resource(StudentDetail, "/students/<int:student_id>")
# api.add_resource(InstructorsList, "/instructors")
# api.add_resource(InstructorDetail, "/instructors/<int:instructor_id>")

# api.add_resource(CoursesList, "/courses")
# api.add_resource(CoursesByStudent, "/students/<int:student_id>/courses")
# api.add_resource(CoursesByInstructor, "/instructors/<int:instructor_id>/courses")
# api.add_resource(CourseManagement, "/courses", "/courses/<int:course_id>")

# api.add_resource(VideosByCourse, "/courses/<int:course_id>/videos")
# api.add_resource(
#     VideosByCourseWeek, "/courses/<int:course_id>/weeks/<int:week_number>/videos"
# )
# api.add_resource(VideoDetail, "/videos/<int:video_id>")
# api.add_resource(VideoManagement, "/videos", "/videos/<int:video_id>")

# api.add_resource(AssignmentsByCourse, "/courses/<int:course_id>/assignments")
# api.add_resource(
#     AssignmentsByCourseWeek,
#     "/courses/<int:course_id>/weeks/<int:week_number>/assignments",
# )
# api.add_resource(
#     AssignmentManagement, "/assignments", "/assignments/<int:assignment_id>"
# )
# api.add_resource(AssignmentById, "/api/assignments/<int:assignment_id>")

# api.add_resource(QuestionsByAssignment, "/assignments/<int:assignment_id>/questions")
# api.add_resource(QuestionManagement, "/questions", "/questions/<int:question_id>")

# api.add_resource(
#     SubmissionsByCourseWeek,
#     "/courses/<int:course_id>/weeks/<int:week_number>/submissions",
# )
# api.add_resource(SubmissionsByCourse, "/courses/<int:course_id>/submissions")
# api.add_resource(SubmissionManagement, "/assignments/<int:assignment_id>/submission")

# api.add_resource(QuestionHint, "/question_hint/<string:question_stmt>")
# api.add_resource(SummarizeVideo, "/summarize_video/<int:video_id>") 

from flask import jsonify, request, current_app as app
from flask_login import current_user
from flask_restful import Api, Resource, reqparse
from flask_security import auth_required, roles_required
from model import (
    Users,
    Instructor,
    Student,
    Course,
    Week,
    Video,
    Assignment,
    InstructorCourse,
    CourseStudent,
    Question,
    UserQuestionAnswer,
    Submission,
    Role,
    roles_users,
    QuestionChoice,
    db,
)
from sqlalchemy import func
from datetime import datetime
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import re

# Initialize API with prefix
api = Api(prefix="/api")
genai.configure(api_key="AIzaSyCOH6hPYZ3prjUiUO-e0JGct41CMpj2gNQ")


def extract_video_id(url):
    """Extracts video ID from a given YouTube URL."""
    pattern = r"(?:https?:\/\/)?(?:www\.|m\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def is_admin(user_id):
    role_mapping = db.session.execute(
        db.select(roles_users.c.role_id).where(
            roles_users.c.user_id == 1
        )  # change as user_id = Users.user_id
    ).fetchone()

    if role_mapping:
        role_id = role_mapping[0]
        role = Role.query.filter_by(id=role_id).first()
        return role and role.name == "admin"

    return False


# ---------- Student Resources ----------


class StudentsByCourse(Resource):
    # @auth_required("token")
    def get(self, course_id):
        students_in_course = (
            db.session.query(Student)
            .join(CourseStudent, Student.student_id == CourseStudent.student_id)
            .filter(CourseStudent.course_id == course_id)
            .all()
        )

        result = []
        for student in students_in_course:
            enrolled_courses = (
                db.session.query(CourseStudent.course_id)
                .filter(CourseStudent.student_id == student.student_id)
                .all()
            )
            # Convert list of one-tuples to a plain list of ids.
            enrolled_courses = [course_id for (course_id,) in enrolled_courses]

            result.append(
                {
                    "student_id": student.student_id,
                    "first_name": student.first_name,
                    "last_name": student.last_name,
                    "level": student.level,
                    "total_CGPA": student.total_CGPA,
                    "weakness": student.weakness,
                    "contact_info": student.contact_info,
                    "email": student.email,
                    # Optionally, include all enrolled course IDs:
                    #'enrolled_courses': enrolled_courses
                }
            )
        return result, 200


class StudentDetail(Resource):
    # @auth_required("token")
    def get(self, student_id):
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            return {"message": "Student not found"}, 404

        # Build a list of course_ids the student is enrolled in using CourseStudent.
        enrolled_courses = (
            db.session.query(CourseStudent.course_id)
            .filter(CourseStudent.student_id == student.student_id)
            .all()
        )
        enrolled_courses = [course_id for (course_id,) in enrolled_courses]

        data = {
            "student_id": student.student_id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "level": student.level,
            "total_CGPA": student.total_CGPA,
            "weakness": student.weakness,
            "contact_info": student.contact_info,
            "email": student.email,
            "enrolled_courses": enrolled_courses,
        }
        return data, 200


# ---------- Instructor Resources ----------


class InstructorsList(Resource):
    # @auth_required("token")
    def get(self):
        instructors = Instructor.query.all()
        result = []
        for inst in instructors:
            result.append(
                {
                    "instructor_id": inst.instructor_id,
                    "name": inst.name,
                    "experience": inst.experience,
                    "qualification": inst.qualification,
                    "contact_info": inst.contact_info,
                    "email": inst.email,
                }
            )
        return result, 200


class InstructorDetail(Resource):
    # @auth_required("token")
    def get(self, instructor_id):
        inst = Instructor.query.filter_by(instructor_id=instructor_id).first()
        if not inst:
            return {"message": "Instructor not found"}, 404

        data = {
            "instructor_id": inst.instructor_id,
            "name": inst.name,
            "experience": inst.experience,
            "qualification": inst.qualification,
            "contact_info": inst.contact_info,
            "email": inst.email,
        }
        return data, 200


# ---------- Courses Resources ----------


class CoursesList(Resource):
    # @auth_required("token")
    def get(self, course_id=None):  # Add course_id parameter
        if course_id:
            # Handle single course request
            course = Course.query.get(course_id)
            if not course:
                return {"message": "Course not found"}, 404

            # Get instructors for single course
            instructor_ids = [
                inst[0]
                for inst in db.session.query(InstructorCourse.instructor_id)
                .filter_by(course_id=course_id)
                .all()
            ]

            return {
                "course_id": course.course_id,
                "instructor_ids": instructor_ids,
                "name": course.name,
                "desc": course.desc,
                "course_code": course.course_code,
                "term_name": course.term_name,
                "created_at": (
                    course.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    if course.created_at
                    else None
                ),
            }, 200
        else:
            # Handle all courses request
            courses = Course.query.all()
            results = []

            for course in courses:
                # Get instructors for each course
                instructor_ids = [
                    inst[0]
                    for inst in db.session.query(InstructorCourse.instructor_id)
                    .filter_by(course_id=course.course_id)
                    .all()
                ]

                results.append(
                    {
                        "course_id": course.course_id,
                        "instructor_ids": instructor_ids,
                        "name": course.name,
                        "desc": course.desc,
                        "course_code": course.course_code,
                        "term_name": course.term_name,
                        "created_at": (
                            course.created_at.strftime("%Y-%m-%d %H:%M:%S")
                            if course.created_at
                            else None
                        ),
                    }
                )

            return results, 200


class CoursesByStudent(Resource):
    # @auth_required("token")
    def get(self, student_id):
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            return {"message": "Student not found"}, 404

        # Use the CourseStudent mapping table to find courses the student is enrolled in.
        course_ids = [
            cid
            for (cid,) in db.session.query(CourseStudent.course_id)
            .filter_by(student_id=student.student_id)
            .all()
        ]
        courses = (
            Course.query.filter(Course.course_id.in_(course_ids)).all()
            if course_ids
            else []
        )
        result = []
        for course in courses:
            instructor_ids = [
                inst
                for (inst,) in db.session.query(InstructorCourse.instructor_id)
                .filter_by(course_id=course.course_id)
                .all()
            ]
            result.append(
                {
                    "course_id": course.course_id,
                    "instructor_ids": instructor_ids,
                    "name": course.name,
                    "desc": course.desc,
                    "course_code": course.course_code,
                    "term_name": course.term_name,
                    "created_at": (
                        course.created_at.strftime("%Y-%m-%d %H:%M:%S")
                        if course.created_at
                        else None
                    ),
                }
            )
        return result, 200


class CoursesByInstructor(Resource):
    # @auth_required("token")
    def get(self, instructor_id):
        # Use the InstructorCourse mapping table to find course IDs linked to the instructor.
        course_ids = [
            cid
            for (cid,) in db.session.query(InstructorCourse.course_id)
            .filter_by(instructor_id=instructor_id)
            .all()
        ]
        courses = (
            Course.query.filter(Course.course_id.in_(course_ids)).all()
            if course_ids
            else []
        )
        result = []
        for course in courses:
            instructor_ids = [
                inst
                for (inst,) in db.session.query(InstructorCourse.instructor_id)
                .filter_by(course_id=course.course_id)
                .all()
            ]
            result.append(
                {
                    "course_id": course.course_id,
                    "instructor_ids": instructor_ids,
                    "name": course.name,
                    "desc": course.desc,
                    "course_code": course.course_code,
                    "term_name": course.term_name,
                    "created_at": (
                        course.created_at.strftime("%Y-%m-%d %H:%M:%S")
                        if course.created_at
                        else None
                    ),
                }
            )
        return result, 200


class CourseManagement(Resource):
    def put(self, course_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "name", type=str, required=True, help="Course name is required"
        )
        parser.add_argument(
            "desc", type=str, required=True, help="Course description is required"
        )
        parser.add_argument("course_code", type=str)
        parser.add_argument("term_name", type=str)
        parser.add_argument("instructor_id", type=int)  # Optional for creation

        data = parser.parse_args()

        if course_id:  # Update existing course
            course = Course.query.get(course_id)
            if not course:
                return {"message": "Course not found"}, 404

            # Update course fields
            course.name = data["name"]
            course.desc = data["desc"]
            course.course_code = data.get("course_code")
            course.term_name = data.get("term_name")
            message = "Course updated successfully"

            # Handle instructor mapping (update only)
            if data.get("instructor_id"):
                mapping = InstructorCourse.query.filter_by(course_id=course_id).first()
                if mapping:
                    mapping.instructor_id = data["instructor_id"]
                else:
                    db.session.add(
                        InstructorCourse(
                            instructor_id=data["instructor_id"], course_id=course_id
                        )
                    )

        else:  # Create new course
            course = Course(
                name=data["name"],
                desc=data["desc"],
                course_code=data.get("course_code"),
                term_name=data.get("term_name"),
            )
            db.session.add(course)
            db.session.flush()  # Get course ID before commit
            message = "Course created successfully"

        db.session.commit()
        return {
            "message": message,
            "course_id": course.course_id,
            "details": {
                "name": course.name,
                "description": course.desc,
                "code": course.course_code,
                "term": course.term_name,
            },
        }, (200 if course_id else 201)


# ---------- Video Resources ----------


class VideosByCourse(Resource):
    @auth_required("token")
    def get(self, course_id):
        # Join Video with Week by matching week_id to filter videos for the given course.
        videos = (
            Video.query.join(Week, Video.week_id == Week.week_id)
            .filter(Week.course_id == course_id)
            .all()
        )
        result = [
            {
                "video_id": video.video_id,
                "week_id": video.week_id,
                "video_no": video.video_no,
                "title": video.title,
                "video_url": video.video_url,
            }
            for video in videos
        ]
        return result, 200


class AddVideoToCourseWeek(Resource):
    @auth_required("token")
    def post(self, course_id, week_number):
        # Get the data from the request body
        data = request.get_json()

        # Validate required fields
        required_fields = ["video_no", "title", "video_url"]
        for field in required_fields:
            if field not in data:
                return {"message": f"'{field}' is required"}, 400

        # Find the week based on course_id and week_number
        week = Week.query.filter_by(course_id=course_id, week_no=week_number).first()

        if not week:
            return {"message": "Week not found"}, 404

        # Create a new video entry in the database
        new_video = Video(
            week_id=week.week_id,
            video_no=data["video_no"],
            title=data["title"],
            video_url=data["video_url"],
            # Optional: set a timestamp for when the video is added
            added_on=datetime.utcnow(),
        )

        try:
            # Save the video to the database
            db.session.add(new_video)
            db.session.commit()
            return {
                "message": "Video added successfully",
                "video_id": new_video.video_id,
            }, 201
        except Exception as e:
            db.session.rollback()
            return {
                "message": f"An error occurred while adding the video: {str(e)}"
            }, 500


class VideosByCourseWeek(Resource):
    # @auth_required("token")
    def get(self, course_id, week_number):
        # Adjust filtering as our Week model uses "week_no"
        week = Week.query.filter_by(course_id=course_id, week_no=week_number).first()
        if not week:
            return {"message": "Week not found"}, 404
        # Query videos that belong to the found week.
        videos = Video.query.filter_by(week_id=week.week_id).all()
        result = [
            {
                "video_id": video.video_id,
                "week_id": video.week_id,
                "video_no": video.video_no,
                "title": video.title,
                "video_url": video.video_url,
            }
            for video in videos
        ]
        return result, 200


class VideoDetail(Resource):
    @auth_required("token")
    def get(self, video_id):
        video = Video.query.filter_by(video_id=video_id).first()
        if not video:
            return {"message": "Video not found"}, 404

        data = {
            "video_id": video.video_id,
            "week_id": video.week_id,
            "video_no": video.video_no,
            "title": video.title,
            "video_url": video.video_url,
            "transcript": video.transcript,
            "tags": video.tags,
        }
        return data, 200


class VideoManagement(Resource):
    # @auth_required("token")
    def post(self):
        """Create a new video."""
        data = request.json
        if not data:
            return {"message": "No data provided"}, 400

        required_fields = ["week_id", "video_no", "title", "video_url"]
        if not all(field in data for field in required_fields):
            return {"message": "Missing required fields"}, 400

        video = Video(
            week_id=data["week_id"],
            video_no=data["video_no"],
            title=data["title"],
            video_url=data["video_url"],
            transcript=data.get("transcript", ""),
            tags=data.get("tags", ""),
        )

        db.session.add(video)
        db.session.commit()

        return {
            "video_id": video.video_id,
            "week_id": video.week_id,
            "video_no": video.video_no,
            "title": video.title,
            "video_url": video.video_url,
            "transcript": video.transcript,
            "tags": video.tags,
        }, 201

    # @auth_required("token")
    def put(self, video_id):
        """Update an existing video."""
        video = Video.query.filter_by(video_id=video_id).first()
        if not video:
            return {"message": "Video not found"}, 404

        data = request.json
        if not data:
            return {"message": "No data provided"}, 400

        video.week_id = data.get("week_id", video.week_id)
        video.video_no = data.get("video_no", video.video_no)
        video.title = data.get("title", video.title)
        video.video_url = data.get("video_url", video.video_url)
        video.transcript = data.get("transcript", video.transcript)
        video.tags = data.get("tags", video.tags)

        db.session.commit()

        return {
            "video_id": video.video_id,
            "week_id": video.week_id,
            "video_no": video.video_no,
            "title": video.title,
            "video_url": video.video_url,
            "transcript": video.transcript,
            "tags": video.tags,
        }, 200

    # @auth_required("token")
    def delete(self, video_id):
        """Delete a video."""
        video = Video.query.filter_by(video_id=video_id).first()
        if not video:
            return {"message": "Video not found"}, 404

        db.session.delete(video)
        db.session.commit()

        return {"message": "Video deleted successfully"}, 200


# ---------- Assignment Resources ----------


class AssignmentsByCourse(Resource):
    # @auth_required("token")
    def get(self, course_id):
        # Join Assignment with Week to filter by course using Week.course_id.
        assignments = (
            Assignment.query.join(Week, Assignment.week_no == Week.week_no)
            .filter(Week.course_id == course_id)
            .all()
        )
        result = [
            {
                "assignment_id": assign.assignment_id,
                "due_date": (
                    assign.due_date.strftime("%Y-%m-%d %H:%M:%S")
                    if assign.due_date
                    else None
                ),
                "week_no": assign.week_no,
                "instructor_id": assign.instructor_id,
                "course_id": assign.course_id,
            }
            for assign in assignments
        ]
        return result, 200


class AssignmentsByCourseWeek(Resource):
    # @auth_required("token")
    def get(self, course_id, week_number):
        # Filter Week by course_id and week_no.
        week = Week.query.filter_by(course_id=course_id, week_no=week_number).first()
        if not week:
            return {"message": "Week not found"}, 404

        # Filter assignments by matching week_no and course_id.
        assignments = Assignment.query.filter_by(
            week_no=week_number, course_id=course_id
        ).all()
        result = [
            {
                "assignment_id": assign.assignment_id,
                "due_date": (
                    assign.due_date.strftime("%Y-%m-%d %H:%M:%S")
                    if assign.due_date
                    else None
                ),
                "week_no": assign.week_no,
                "instructor_id": assign.instructor_id,
                "course_id": assign.course_id,
            }
            for assign in assignments
        ]
        return result, 200


class AssignmentManagement(Resource):
    def post(self):
        # Same logic as in the put method, for creating new assignments
        parser = reqparse.RequestParser()
        parser.add_argument(
            "week_no", type=int, required=True, help="Week number is required"
        )
        parser.add_argument(
            "course_id", type=int, required=True, help="Course ID is required"
        )
        parser.add_argument(
            "due_date",
            type=str,
            required=False,
            help="Due date in format YYYY-MM-DD HH:MM:SS",
        )
        parser.add_argument(
            "instructor_id", type=int, required=True, help="Instructor ID is required"
        )
        data = parser.parse_args()

        due_date_val = None
        if data.get("due_date"):
            try:
                due_date_val = datetime.strptime(data["due_date"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return {
                    "message": "Invalid due_date format. Use YYYY-MM-DD HH:MM:SS"
                }, 400

        # Create the assignment
        assignment = Assignment(
            week_no=data["week_no"],
            course_id=data["course_id"],
            instructor_id=data["instructor_id"],
            due_date=due_date_val,
        )
        db.session.add(assignment)
        db.session.flush()  # Flush to generate assignment_id
        db.session.commit()

        return {
            "message": "Assignment created",
            "assignment_id": assignment.assignment_id,
        }, 201  # 201 for resource creation

    def delete(self, assignment_id):
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return {"message": "Assignment not found"}, 404

        db.session.delete(assignment)
        db.session.commit()
        return {"message": "Assignment deleted successfully"}, 200


class AssignmentById(Resource):
    def get(self, assignment_id):
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return {"message": "Assignment not found"}, 404

        return {
            "assignment_id": assignment.assignment_id,
            "due_date": (
                assignment.due_date.strftime("%Y-%m-%d %H:%M:%S")
                if assignment.due_date
                else None
            ),
            "week_no": assignment.week_no,
            "course_id": assignment.course_id,
            "instructor_id": assignment.instructor_id,
            # Add any other assignment details you need
        }, 200


# ---------- Question Resources ----------


class QuestionsByAssignment(Resource):
    # @auth_required("token")
    def get(self, assignment_id):
        # Query all questions for the given assignment_id.
        questions = Question.query.filter_by(assignment_id=assignment_id).all()
        result = [
            {
                "question_id": question.question_id,
                "stmt": question.stmt,
                "tags": question.tags,
            }
            for question in questions
        ]
        return result, 200


class QuestionManagement(Resource):
    # @auth_required("token")
    # @roles_required("instructor")
    def put(self, question_id=None):
        parser = reqparse.RequestParser()
        # Adjusted field names to match the models.py definition:
        # Use 'stmt' for the question statement instead of 'type'
        # and use 'tags' in place of 'correct_answer' if needed.
        parser.add_argument(
            "assignment_id", type=int, required=True, help="Assignment ID is required"
        )
        parser.add_argument(
            "stmt", type=str, required=True, help="Question statement is required"
        )
        parser.add_argument(
            "optionsStmt", type=str, required=True, help="Question options is required"
        )
        parser.add_argument("tags", type=str, required=False, help="Tags are optional")
        data = parser.parse_args()

        print(data)

        if question_id:
            question = Question.query.get(question_id)
            if not question:
                return {"message": "Question not found"}, 404
            question.assignment_id = data["assignment_id"]
            question.stmt = data["stmt"]
            question.tags = data.get("tags")
            message = "Question updated"
        else:
            print(data)
            question = Question(
                assignment_id=data["assignment_id"],
                stmt=data["stmt"],
                tags=data.get("tags"),
            )
            db.session.add(question)
            message = "Question created"

        db.session.commit()
        return {"message": message, "question_id": question.question_id}, 200

    # @auth_required("token")
    # @roles_required("instructor")
    def delete(self, question_id):
        question = Question.query.get(question_id)
        if not question:
            return {"message": "Question not found"}, 404

        db.session.delete(question)
        db.session.commit()
        return {"message": "Question deleted"}, 200

    def post(self, question_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument("assignment_id", type=int, required=True)
        parser.add_argument("stmt", type=str, required=True)
        parser.add_argument("optionsStmt", type=str, required=True)
        parser.add_argument("tags", type=str, required=False)

        data = parser.parse_args()

        # Create the Question entry
        question = Question(
            assignment_id=data["assignment_id"],
            stmt=data["stmt"],
            tags=data.get("tags"),
        )
        db.session.add(question)
        db.session.commit()  # Commit to generate question_id

        # Split optionsStmt into individual choices
        option_statements = [opt.strip() for opt in data["optionsStmt"].split(",")]

        correct_index = int(option_statements.pop()) - 1

        # Create QuestionChoice entries for each option
        for index, option_stmt in enumerate(option_statements):
            choice = QuestionChoice(
                question_id=question.question_id,
                choice_stmt=option_stmt,
                is_right_choice=(
                    index == correct_index
                ),  # Defaulting to False, modify as needed
            )
            db.session.add(choice)

        db.session.commit()  # Commit choices to the database

        return {"message": "Question created", "question_id": question.question_id}, 201


# ---------- Submission Resources ----------


class SubmissionsByCourseWeek(Resource):
    # @auth_required("token")
    def get(self, course_id, week_number):
        # Find the week using course_id and week_no (our Week model uses week_no)
        week = Week.query.filter_by(course_id=course_id, week_no=week_number).first()
        if not week:
            return {"message": "Week not found"}, 404

        # Get assignments for the specified course and week.
        assignments = Assignment.query.filter_by(
            course_id=course_id, week_no=week_number
        ).all()
        submissions_list = []
        for assign in assignments:
            # For each assignment, get its submissions.
            submissions = Submission.query.filter_by(
                assignment_id=assign.assignment_id
            ).all()
            for sub in submissions:
                submissions_list.append(
                    {
                        "submission_id": sub.submission_id,
                        "assignment_id": sub.assignment_id,
                        "student_id": sub.student_id,
                        "submitted_at": (
                            sub.time.strftime("%Y-%m-%d %H:%M:%S") if sub.time else None
                        ),
                        "marks_obtained": sub.marks,
                    }
                )
        return submissions_list, 200


class SubmissionsByCourse(Resource):
    # @auth_required("token")
    def get(self, course_id):
        # Get all assignments under the given course.
        assignments = Assignment.query.filter_by(course_id=course_id).all()
        submissions_list = []
        for assign in assignments:
            submissions = Submission.query.filter_by(
                assignment_id=assign.assignment_id
            ).all()
            for sub in submissions:
                submissions_list.append(
                    {
                        "submission_id": sub.submission_id,
                        "assignment_id": sub.assignment_id,
                        "student_id": sub.student_id,
                        "submitted_at": (
                            sub.time.strftime("%Y-%m-%d %H:%M:%S") if sub.time else None
                        ),
                        "marks_obtained": sub.marks,
                    }
                )
        return submissions_list, 200


class SubmissionManagement(Resource):
    # @auth_required("token") # Make sure authentication is active
    # Inside SubmissionManagement class, put method
    def put(self, assignment_id):
        # 1. Get Request Data
        data = request.get_json()
        if not data or "selectedChoices" not in data:
            return {"message": "Missing 'selectedChoices' in request body"}, 400
        selected_choices_dict = data["selectedChoices"]

        # *** Hardcode student_id for testing ***
        student_id = 1  # Or any valid student ID from your database
        print(f"WARNING: Using hardcoded student_id: {student_id}")  # Add a warning!

        # ... (rest of the logic uses student_id = 1) ...

        # 2. Get Request Data
        data = request.get_json()
        if not data or "selectedChoices" not in data:
            return {"message": "Missing 'selectedChoices' in request body"}, 400
        # selectedChoices is expected to be: { "question_id_str": choice_id, ... }
        selected_choices_dict = data["selectedChoices"]

        # 3. Validate Assignment
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return {"message": "Assignment not found"}, 404

        # 4. Get all questions for this assignment
        questions = Question.query.filter_by(assignment_id=assignment_id).all()
        if not questions:
            return {"message": "No questions found for this assignment"}, 404

        total_questions = len(questions)
        correct_count = 0
        results_detail = (
            {}
        )  # To store feedback for each question {question_id: {is_correct: bool, correct_choice_id: int}}

        # Optional: Clear previous answers for this user/assignment in UserQuestionAnswer if needed
        # UserQuestionAnswer.query.filter_by(user_id=student_id, question_id.in_([q.question_id for q in questions])).delete()

        # 5. Process Each Question
        for question in questions:
            question_id_str = str(question.question_id)  # Keys in JSON are strings
            selected_choice_id = selected_choices_dict.get(question_id_str)

            # Find the correct choice for this question
            correct_choice = QuestionChoice.query.filter_by(
                question_id=question.question_id, is_right_choice=True
            ).first()

            # Handle cases where correct choice isn't set (data issue)
            if not correct_choice:
                print(
                    f"Warning: No correct choice found for question ID {question.question_id}"
                )
                # Decide how to handle this: skip, mark as incorrect, etc.
                # Let's skip scoring it for now, but record it was attempted if selected
                if selected_choice_id is not None:
                    results_detail[question.question_id] = {
                        "selected_choice_id": (
                            int(selected_choice_id) if selected_choice_id else None
                        ),
                        "is_correct": False,  # Cannot determine correctness
                        "correct_choice_id": None,  # No correct choice defined
                    }
                continue  # Move to the next question

            is_correct = False
            if selected_choice_id is not None:
                try:
                    # Ensure comparison is between integers
                    is_correct = int(selected_choice_id) == correct_choice.choice_id
                    if is_correct:
                        correct_count += 1

                    # Store detailed result
                    results_detail[question.question_id] = {
                        "selected_choice_id": int(selected_choice_id),
                        "is_correct": is_correct,
                        "correct_choice_id": correct_choice.choice_id,
                    }

                    # Optional: Save the attempt to UserQuestionAnswer
                    # existing_answer = UserQuestionAnswer.query.filter_by(user_id=student_id, question_id=question.question_id).first()
                    # if existing_answer:
                    #     existing_answer.selected_choice_id = int(selected_choice_id)
                    #     existing_answer.is_right = is_correct
                    #     existing_answer.answered_on = datetime.utcnow()
                    # else:
                    #     new_answer = UserQuestionAnswer(
                    #         user_id=student_id,
                    #         question_id=question.question_id,
                    #         selected_choice_id=int(selected_choice_id),
                    #         is_right=is_correct,
                    #         answered_on=datetime.utcnow()
                    #     )
                    #     db.session.add(new_answer)

                except ValueError:
                    # Handle case where selected_choice_id is not a valid integer string
                    print(
                        f"Warning: Invalid format for selected_choice_id '{selected_choice_id}' for question {question.question_id}"
                    )
                    results_detail[question.question_id] = {
                        "selected_choice_id": None,  # Or keep the invalid string?
                        "is_correct": False,
                        "correct_choice_id": correct_choice.choice_id,
                    }
            else:
                # Question was not answered
                results_detail[question.question_id] = {
                    "selected_choice_id": None,
                    "is_correct": False,  # Mark unanswered as incorrect for scoring? Or handle separately?
                    "correct_choice_id": correct_choice.choice_id,
                }

        # 6. Calculate Final Score (e.g., as a percentage)
        marks_obtained = (
            (correct_count / total_questions) * 100 if total_questions > 0 else 0
        )

        # 7. Create or Update Submission Record
        submission = Submission.query.filter_by(
            assignment_id=assignment_id, student_id=student_id
        ).first()

        if submission:
            submission.marks = marks_obtained
            submission.time = datetime.utcnow()
            message = "Submission updated"
        else:
            submission = Submission(
                assignment_id=assignment_id,
                student_id=student_id,
                marks=marks_obtained,
                time=datetime.utcnow(),  # Use current time for submission time
            )
            db.session.add(submission)
            message = "Submission created"

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Database error during submission: {e}")
            return {"message": f"Database error: {e}"}, 500

        # 8. Return Detailed Response
        return {
            "message": message,
            "submission_id": submission.submission_id,
            "marks_obtained": marks_obtained,
            "correct_count": correct_count,
            "total_questions": total_questions,
            "results_detail": results_detail,  # Send back the per-question feedback
        }, 200


# Add to resources.py


class WeeksByCourse(Resource):
    # @auth_required("token")
    def get(self, course_id):
        weeks = Week.query.filter_by(course_id=course_id).order_by(Week.week_no).all()
        return [
            {
                "week_id": week.week_id,
                # "name": week.name,
                "week_no": week.week_no,
                "course_id": week.course_id,
            }
            for week in weeks
        ], 200

    # @auth_required("token")
    # @roles_required("instructor")
    def post(self, course_id):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("week_no", type=int, required=True)
        data = parser.parse_args()

        if Week.query.filter_by(course_id=course_id, week_no=data["week_no"]).first():
            return {"message": "Week number already exists in this course"}, 400

        week = Week(course_id=course_id, week_no=data["week_no"])
        db.session.add(week)
        db.session.commit()
        return {"message": "Week added", "week_id": week.week_id}, 201


class WeekDetail(Resource):
    # @auth_required("token")
    # @roles_required("instructor")
    def put(self, week_id):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("week_no", type=int)
        data = parser.parse_args()

        week = Week.query.get(week_id)
        if not week:
            return {"message": "Week not found"}, 404

        if data.get("week_no"):
            existing = Week.query.filter_by(
                course_id=week.course_id, week_no=data["week_no"]
            ).first()
            if existing and existing.week_id != week_id:
                return {"message": "Week number already exists in this course"}, 400
            week.week_no = data["week_no"]

        if data.get("name"):
            week.name = data["name"]

        db.session.commit()
        return {"message": "Week updated"}, 200

    # @auth_required("token")
    # @roles_required("instructor")
    def delete(self, week_id):
        week = Week.query.get(week_id)
        if not week:
            return {"message": "Week not found"}, 404

        db.session.delete(week)
        db.session.commit()
        return {"message": "Week deleted"}, 200


class ChoicesByQuestion(Resource):
    # @auth_required('token')
    def get(self, question_id):
        # Query all choices for the given question_id.
        choices = QuestionChoice.query.filter_by(question_id=question_id).all()

        if not choices:
            return {"message": "No choices found for this question"}, 404

        result = [
            {
                "choice_id": choice.choice_id,
                "choice_stmt": choice.choice_stmt,
                "is_right_choice": choice.is_right_choice,  # You might want to remove this if it should be hidden
            }
            for choice in choices
        ]

        return result, 200


class QuestionHint(Resource):
    def get(self, question_stmt):
        try:
            # Generate a hint using Gemini AI
            prompt = f"Provide a helpful hint for the following question without revealing the direct answer: {question_stmt}"
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            hint = response.text.strip()

            return {"hint": hint}, 200
        except Exception as e:
            return {"error": str(e)}, 500


class SummarizeVideo(Resource):
    def get(self, video_id):
        try:
            # Fetch video object from DB using video_id
            video = Video.query.get(video_id)
            if not video:
                return {"error": "Video not found"}, 404

            # If transcript is available, return it
            if video.transcript:
                return {"summary": video.transcript}, 200

            # If no transcript exists, fetch the transcript from YouTube
            transcript_data = YouTubeTranscriptApi.get_transcript(
                video.video_url.split("=")[-1]
            )  # Get video_id from URL
            transcript = " ".join([t["text"] for t in transcript_data])

            # Generate summary using Gemini
            prompt = f"Summarize the following transcript of a YouTube lecture video:\n\n{transcript}"
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            summary = response.text.strip()

            # Store the generated summary in the database
            video.transcript = summary
            db.session.commit()

            return {"summary": summary}, 200

        except Exception as e:
            return {"error": str(e)}, 500


class CourseResource(Resource):
    # @auth_required('token')
    # @login_required
    # @roles_accepted('admin')
    def post(self):
        if not is_admin(current_user):
            return {"message": "You are not an admin and not allowed to do that."}, 403

        try:
            # if Role=='admin':
            data = request.get_json()
            name = data.get("name")
            desc = data.get("desc")
            term_name = data.get("term_name")
            course_code = data.get("course_code")
            print(data)
            if not name or not term_name or not course_code:
                return {"message": "Invalid data."}, 400

            if Course.query.filter_by(
                course_code=course_code, term_name=term_name
            ).first():
                return {"message": "Course already exists."}, 409

            new_course = Course(
                name=name, desc=desc, term_name=term_name, course_code=course_code
            )
            print(new_course)  # sinha work
            db.session.add(new_course)
            db.session.commit()

            return {"message": "Course added.", "course_id": new_course.course_id}, 201

        except:
            db.session.rollback()
            return {"message": "Something went wrong."}, 500

    # @auth_required('token')
    def delete(self, course_id):
        if not is_admin(current_user):
            return {"message": "You are not an admin and not allowed to do that."}, 403

        course = Course.query.get(course_id)
        print(course)
        if not course:
            return {"message": "Course not found."}, 404

        db.session.delete(course)
        db.session.commit()

        return {"message": "Course deleted."}, 200

    # @auth_required('token')
    def put(self, course_id):
        if not is_admin(current_user):
            return {"message": "You are not an admin and not allowed to do that."}, 403

        course = Course.query.get(course_id)
        if not course:
            return {"message": "Course not found."}, 404

        data = request.get_json()
        course.name = data.get("name", course.name)
        course.desc = data.get("desc", course.desc)
        course.term_name = data.get("term_name", course.term_name)
        course.course_code = data.get("course_code", course.course_code)

        db.session.commit()

        return {"message": "Course updated."}, 200

    def get(self, course_id=None):
        if course_id is None:  # this part is added by abhi sinha
            courses = Course.query.all()
            result = []
            for course in courses:
                result.append(
                    {
                        "course_id": course.course_id,
                        "name": course.name,
                        "desc": course.desc,
                        "course_code": course.course_code,
                        "term_name": course.term_name,
                        "created_at": (
                            course.created_at.strftime("%Y-%m-%d %H:%M:%S")
                            if course.created_at
                            else None
                        ),
                    }
                )
                print(result)
            return result, 200
        else:
            course = Course.query.get(course_id)
            if not course:
                return {"message": "Course not found."}, 404

            return {
                "course_id": course.course_id,
                "name": course.name,
                "desc": course.desc,
                "term_name": course.term_name,
                "course_code": course.course_code,
            }, 200


from genAI.chat import chat


class ChatResource(Resource):
    @auth_required('token')
    def post(self):
        data = request.get_json()
        question = data.get("question")
        answer= chat(question, current_user.user_id)
        return {"message": answer}, 200

api.add_resource(ChatResource, "/chat")

# Add resource to API
api.add_resource(CourseResource, "/course", "/course/<int:course_id>")

api.add_resource(ChoicesByQuestion, "/questions/<int:question_id>/choices")
# Add routes
api.add_resource(WeeksByCourse, "/courses/<int:course_id>/weeks")
api.add_resource(WeekDetail, "/weeks/<int:week_id>")
# To add these resources to your API, for example:
api.add_resource(StudentsByCourse, "/courses/<int:course_id>/students")
api.add_resource(StudentDetail, "/students/<int:student_id>")
api.add_resource(InstructorsList, "/instructors")
api.add_resource(InstructorDetail, "/instructors/<int:instructor_id>")

api.add_resource(CoursesList, "/courses", "/courses/<int:course_id>")
api.add_resource(CoursesByStudent, "/students/<int:student_id>/courses")
api.add_resource(CoursesByInstructor, "/instructors/<int:instructor_id>/courses")
api.add_resource(CourseManagement, "/courses", "/courses/<int:course_id>")

api.add_resource(VideosByCourse, "/courses/<int:course_id>/videos")
api.add_resource(
    VideosByCourseWeek, "/courses/<int:course_id>/weeks/<int:week_number>/videos"
)
api.add_resource(VideoDetail, "/videos/<int:video_id>")
api.add_resource(VideoManagement, "/videos", "/videos/<int:video_id>")

api.add_resource(AssignmentsByCourse, "/courses/<int:course_id>/assignments")
api.add_resource(
    AssignmentsByCourseWeek,
    "/courses/<int:course_id>/weeks/<int:week_number>/assignments",
)
api.add_resource(
    AssignmentManagement, "/assignments", "/assignments/<int:assignment_id>"
)
api.add_resource(AssignmentById, "/api/assignments/<int:assignment_id>")

api.add_resource(QuestionsByAssignment, "/assignments/<int:assignment_id>/questions")
api.add_resource(QuestionManagement, "/questions", "/questions/<int:question_id>")

api.add_resource(
    SubmissionsByCourseWeek,
    "/courses/<int:course_id>/weeks/<int:week_number>/submissions",
)
api.add_resource(SubmissionsByCourse, "/courses/<int:course_id>/submissions")
api.add_resource(SubmissionManagement, "/assignments/<int:assignment_id>/submission")

api.add_resource(QuestionHint, "/question_hint/<string:question_stmt>")
api.add_resource(SummarizeVideo, "/summarize_video/<int:video_id>")
