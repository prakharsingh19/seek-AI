from flask_security import hash_password
from model import db


def seed_initial_data(datastore):
    """
    Function to initialize default roles and users inside the app context.
    """
    # Create roles
    admin_role = datastore.find_or_create_role("admin")
    instructor_role = datastore.find_or_create_role("instructor")
    student_role = datastore.find_or_create_role("student")

    # Create admin user if not exists
    if not datastore.find_user(email="admin@seek.ai"):
        datastore.create_user(
            email="admin@seek.ai",
            fs_uniquifier="admin@seek.ai",
            password=hash_password("pass"),
            roles=[admin_role],
            type="users",
        )

    if not datastore.find_user(email="instructor@seek.ai"):
        datastore.create_user(
            email="instructor@seek.ai",
            fs_uniquifier="instructor@seek.ai",
            password=hash_password("pass"),
            roles=[instructor_role],
            type="instructor",
        )

    if not datastore.find_user(email="student@seek.ai"):
        datastore.create_user(
            email="student@seek.ai",
            fs_uniquifier="student@seek.ai",
            password=hash_password("pass"),
            roles=[student_role],
            type="student",
        )

    db.session.commit()
