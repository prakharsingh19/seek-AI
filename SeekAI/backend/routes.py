from flask import (
    jsonify,
    request,
    Flask,
    render_template,
    send_file,
    send_from_directory,
)
from flask_security import *
from model import *
import os

app = Flask(__name__)

user_datastore = SQLAlchemyUserDatastore(db, Users, Role)
security = Security(app, user_datastore)


def init_app(app):
    @app.route("/")
    def home():
        return send_from_directory("../frontend", "index.html")

    @app.route("/login", methods=["POST"])
    def login():
        try:
            data = request.get_json()
            email = data.get("email")
            password = data.get("password")

            # Validation
            if not email or not password:
                return jsonify({"message": "Invalid inputs"}), 400

            # Find the user
            user = Users.query.filter_by(email=email).first()
            if not user:
                return jsonify({"message": "Invalid email"}), 404

            # Verify password
            if not verify_password(password, user.password):
                return jsonify({"message": "Invalid password"}), 401

            # Check if user is active
            if not user.active:
                return jsonify({"message": "You're Blocked by Admin"}), 403

            # Get user's role_id from roles_users table
            role_mapping = db.session.execute(
                db.select(roles_users.c.role_id).where(
                    roles_users.c.user_id == user.user_id
                )
            ).fetchone()

            if not role_mapping:
                return jsonify({"message": "Role not assigned"}), 403

            role_id = role_mapping[0]

            # Get role name from roles table
            role = Role.query.filter_by(id=role_id).first()
            role_name = role.name if role else "User"
            print(role_name)
            # Determine name based on role
            name = "User"
            if role_name == "student":
                name = (
                    Student.query.filter_by(user_id=user.user_id).first()
                ).first_name
                # name = student.first_name if student else "Student"
            elif role_name == "instructor":
                name = (Instructor.query.filter_by(user_id=user.user_id).first()).name
            elif role_name == "admin":
                name = "Admin"

            token = user.get_auth_token()

            return jsonify(
                {
                    "message": "Login successful",
                    "token": token,
                    "role": role_name,
                    "name": name,
                }
            ), 200

        except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500

    @app.route("/register", methods=["POST"])
    def register():
        try:
            data = request.json
            email = data.get("email")
            password = data.get("password")
            role = data.get("role")  # 'student' or 'instructor'

            # Ensure request is from curl (not from frontend)
            if "application/json" not in request.content_type:
                return jsonify({"message": "Invalid request source!"}), 400

            # Prevent admin registration
            if role == "admin":
                return jsonify(
                    {"message": "Method not allowed! Register as Student or Instructor"}
                ), 400

            # Check if required fields are provided
            if not email or not password or not role:
                return jsonify(
                    {
                        "message": "Invalid request format! Required fields(email/password/role) are missing "
                    }
                ), 400

            # Check if the user already exists
            if Users.query.filter_by(email=email).first():
                return jsonify({"message": "User already exists!"}), 400

            # Hash password
            hashed_password = hash_password(password)

            # Validate required fields based on role
            if role == "student":
                if not data.get("first_name"):
                    return jsonify(
                        {
                            "message": "Invalid request format! 'first_name' is required for students"
                        }
                    ), 400

                last_name = data.get("last_name") if data.get("last_name") else None
                contact_info = (
                    data.get("contact_info") if data.get("contact_info") else None
                )

                user = Student(
                    email=email,
                    password=hashed_password,
                    first_name=data.get("first_name"),
                    fs_uniquifier=email,
                    last_name=last_name,
                    contact_info=contact_info,
                )

            elif role == "instructor":
                if not data.get("name"):
                    return jsonify(
                        {
                            "message": "Invalid request format! 'name' is required for instructors"
                        }
                    ), 400

                contact_info = (
                    data.get("contact_info") if data.get("contact_info") else None
                )
                experience = data.get("experience") if data.get("experience") else "0"
                qualification = (
                    data.get("qualification")
                    if data.get("qualification")
                    else "No data"
                )

                user = Instructor(
                    email=email,
                    password=hashed_password,
                    name=data.get("name"),
                    contact_info=contact_info,
                    fs_uniquifier=email,
                    experience=experience,
                    qualification=qualification,
                )

            else:
                return jsonify({"message": "Invalid role!"}), 400

            # Add user to database
            db.session.add(user)
            db.session.commit()

            # Fetch role ID from roles table
            role_entry = Role.query.filter_by(name=role).first()
            if not role_entry:
                return jsonify({"message": "Role does not exist!"}), 400

            # Insert into roles_users table
            db.session.execute(
                roles_users.insert().values(user_id=user.user_id, role_id=role_entry.id)
            )
            db.session.commit()

            return jsonify({"message": "User registered successfully!"}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500
