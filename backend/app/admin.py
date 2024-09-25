'''
This file contains the functionalities associated to an admin.
'''

import sys
import os

current_directory = os.getcwd()
# Get the parent directory
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

import json

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

try:
    from models import (
        db,
        User,
        CourseEnrolment,
        Course,
        CourseArchive,
        Project,
        Group,
        GroupMember,
    )
except ImportError:
    from .models import (
        db,
        User,
        CourseEnrolment,
        Course,
        CourseArchive,
        Project,
        Group,
        GroupMember,
    )

try:
    from course import deleteCourseEnrolment
except ImportError:
    from .course import deleteCourseEnrolment

admin = Blueprint("admin", __name__)


def return_all_users():
    """
    Fetches and returns information about all users in the database.

    Returns:
    - A JSON response containing a list of dictionaries, where each dictionary represents a
    user's information.
      Each user dictionary includes the following keys:
        - "zID": The user's zID.
        - "firstName": The user's first name.
        - "lastName": The user's last name.
        - "email": The user's email address.
        - "userType": A list of user roles derived from the metadata.

    Example:
    {
        "users": [
            {
                "zID": "z1234567",
                "firstName": "John",
                "lastName": "Doe",
                "email": "john.doe@example.com",
                "userType": ["admin", "student"]
            },
            {
                "zID": "z7654321",
                "firstName": "Jane",
                "lastName": "Smith",
                "email": "jane.smith@example.com",
                "userType": ["student"]
            },
            # ... additional user entries ...
        ]
    }
    """
    user_list = db.session.query(User).all()
    user_list_dict = []
    for user in user_list:
        metadata = json.loads(user.metadataJson)
        roles = list(metadata["class"].keys())

        user_info_dict = {
            "zID": user.zID,
            "firstName": user.firstname,
            "lastName": user.lastname,
            "email": user.email,
            "userType": roles,
        }
        user_list_dict.append(user_info_dict)
    return jsonify({"users": user_list_dict})


def return_all_courses():
    """
    Fetches and returns information about all courses in the database.

    Returns:
    - A JSON response containing a list of dictionaries, where each dictionary represents
    a course's information.
      Each course dictionary includes the following keys:
        - "courseCode": The code identifying the course.
        - "courseName": The name of the course.
        - "yearDate": The year associated with the course.
        - "term": The term (e.g., "T2", "T3") in which the course is offered.
        - "school": The school or department offering the course.

    Example:
    {
        "courses": [
            {
                "courseCode": "COMP1511",
                "courseName": "Programming Fundamentals",
                "yearDate": 2023,
                "term": "T3",
                "school": "School of Computer Science and Engineering"
            },
            {
                "courseCode": "COMP6080",
                "courseName": "Web Front-End Programming",
                "yearDate": 2023,
                "term": "T3",
                "school": "School of Computer Science and Engineering"
            },
            # ... additional course entries ...
        ]
    }
    """
    course_list = db.session.query(Course).all()
    course_list_dict = []
    for course in course_list:
        course_info_dict = {
            "courseCode": course.courseCode,
            "courseName": course.courseName,
            "yearDate": course.yearDate,
            "term": course.term,
            "school": course.school,
        }
        course_list_dict.append(course_info_dict)
    return jsonify({"courses": course_list_dict})


def return_all_projects():
    """
    Fetches and returns information about all projects in the database.

    Returns:
    - A JSON response containing a list of dictionaries, where each dictionary represents a
    project's information.
      Each project dictionary includes the following keys:
        - "id": The unique identifier for the project.
        - "projectName": The name of the project.
        - "client": The client associated with the project.

    Example:
    {
        "projects": [
            {
                "id": 1,
                "projectName": "Website Redesign",
                "client": "ABC Corporation"
            },
            {
                "id": 2,
                "projectName": "Mobile App Development",
                "client": "XYZ Company"
            },
            # ... additional project entries ...
        ]
    }
    """
    project_list = db.session.query(Project).all()
    project_list_dict = []
    for project in project_list:
        project_info_dict = {
            "id": project.ID,
            "projectName": project.projectName,
            "client": project.client,
        }
        project_list_dict.append(project_info_dict)
    return jsonify({"projects": project_list_dict})


def user_type_count():
    """
    Counts the number of users in different roles and returns a dictionary with the count
    for each user type.

    Returns:
    - A dictionary containing the count of users for each user type:
        - "student": Number of student users.
        - "casualAcademic": Number of casual academic users.
        - "academic": Number of academic users.
        - "courseAdmin": Number of course admin users.
        - "admin": Number of admin users.

    Example:
    {
        "student": 150,
        "casualAcademic": 20,
        "academic": 50,
        "courseAdmin": 10,
        "admin": 5
    }
    """
    user_list = db.session.query(User).all()
    student_count = 0
    casual_academic_count = 0
    academic_count = 0
    course_admin_count = 0
    admin_count = 0
    for user in user_list:
        metadata = json.loads(user.metadataJson)
        roles = list(metadata["class"].keys())

        if "student" in roles:
            student_count += 1
        if "academic" in roles:
            if metadata["class"]["academic"]["type"] == "academic":
                academic_count += 1
            elif metadata["class"]["academic"]["type"] == "casual academic":
                casual_academic_count += 1
            else:
                course_admin_count += 1
        if "admin" in roles:
            admin_count += 1

    return {
        "student": student_count,
        "casualAcademic": casual_academic_count,
        "academic": academic_count,
        "courseAdmin": course_admin_count,
        "admin": admin_count,
    }


def get_project_count():
    """
    Retrieves the total count of projects in the database.

    Returns:
    - An integer representing the total number of projects.

    Example:
    25  # Total number of projects in the database
    """
    project_count = Project.query.count()
    return project_count


def get_course_count():
    """
    Retrieves the total count of courses in the database.

    Returns:
    - An integer representing the total number of courses.

    Example:
    15  # Total number of courses in the database
    """
    course_count = Course.query.count()
    return course_count


def delete_course_cascade(course_code, year_date, term):
    """
    Deletes a course and its related data in a cascading manner from the database.

    Args:
    - course_code (str): The code identifying the course to be deleted.
    - year_date (int): The year associated with the course to be deleted.
    - term (str): The term (e.g., "Spring", "Fall") in which the course is offered to be
      deleted.

    Returns:
    - A JSON response with a success message if the course is successfully deleted.
      If the course is not found, a JSON response with an error message and a 404 status
      code is returned.

    Example:
    Successfully deleted course
    """
    course = Course.query.filter_by(
        courseCode=course_code, yearDate=year_date, term=term
    ).first()
    if not (course):
        return jsonify({"error": "Course not found."}), 404
    course_id = course.ID
    course_enrolment_in_course = CourseEnrolment.query.filter_by(course=course_id).all()
    for course_enrolment in course_enrolment_in_course:
        zid = course_enrolment.user
        role = course_enrolment.courseRole
        deleteCourseEnrolment(zid, course_id, role)
    CourseArchive.query.filter_by(courseID=course_id).delete()
    Course.query.filter_by(ID=course_id).delete()

    db.session.commit()

    return jsonify({"message": "Successfully deleted course"}), 200


def delete_group_cascade(group_id):
    """
    Deletes a group and its related data in a cascading manner from the database.

    Args:
    - group_id (int): The unique identifier of the group to be deleted.

    Returns:
    - A JSON response with a success message if the group is successfully deleted.
      If the group is not found, a JSON response with an error message and a 404 status
      code is returned.

    Example:
    Successfully deleted group
    """
    group = Group.query.filter_by(ID=group_id).first()
    if not (group):
        return jsonify({"error": "Group not found."}), 404
    GroupMember.query.filter_by(groupID=group_id).delete()
    Group.query.filter_by(ID=group_id).delete()
    db.session.commit()

    return jsonify({"message": "Successfully deleted group"}), 200


def delete_project_cascade(id):
    """
    Deletes a project and its related data in a cascading manner from the database.

    Args:
    - id (int): The unique identifier of the project to be deleted.

    Returns:
    - A JSON response with a success message if the project is successfully deleted.
      If the project is not found, a JSON response with an error message and a 404 status
      code is returned.

    Example:
    Successfully deleted project
    """
    project = Project.query.filter_by(ID=id).first()
    if not (project):
        return jsonify({"error": "Project not found."}), 404
    project_groups = Group.query.filter_by(project=id).all()
    for group in project_groups:
        group_id = group.ID
        delete_group_cascade(group_id)

    Project.query.filter_by(ID=id).delete()

    db.session.commit()
    return jsonify({"message": "Successfully deleted project"}), 200


def delete_user_cascade(zid):
    """
    Deletes a user and its related data in a cascading manner from the database.

    Args:
    - zid (str): The unique identifier (zID) of the user to be deleted.

    Returns:
    - A JSON response with a success message if the user is successfully deleted.
      If the user is not found, a JSON response with an error message and a 404 status
      code is returned.

    Example:
    Successfully deleted user
    """

    user = User.query.filter_by(zID=zid).first()
    if not (user):
        return jsonify({"error": "User not found."}), 404
    GroupMember.query.filter_by(student=zid).delete()
    CourseEnrolment.query.filter_by(user=zid).delete()
    User.query.filter_by(zID=zid).delete()

    db.session.commit()
    return jsonify({"message": "Successfully deleted user"}), 200


@admin.route("/admin/all-users", methods=["GET"])
@jwt_required()
def get_user_list():
    """
    Retrieve a list of all users in the system.

    Requires a valid JWT token for authentication.

    Endpoint:
    GET /admin/all-users

    Returns:
    - A JSON response containing information about all users, including their zID,
    first name, last name,
      email, and user roles.

    Example:
    {
        "users": [
            {
                "zID": "z1234567",
                "firstName": "John",
                "lastName": "Doe",
                "email": "john.doe@example.com",
                "userType": ["admin", "student"]
            },
            {
                "zID": "z7654321",
                "firstName": "Jane",
                "lastName": "Smith",
                "email": "jane.smith@example.com",
                "userType": ["student"]
            },
            # ... additional user entries ...
        ]
    }

    Response Codes:
    - 200 OK: Successful retrieval of user list.
    """
    return return_all_users(), 200


@admin.route("/admin/all-courses", methods=["GET"])
@jwt_required()
def get_course_list():
    """
    Retrieve a list of all courses in the system.

    Requires a valid JWT token for authentication.

    Endpoint:
    GET /admin/all-courses

    Returns:
    - A JSON response containing information about all courses, including their
    course code, course name,
      year, term, and school.

    Example:
    {
            "courses": [
                {
                    "courseCode": "COMP1511",
                    "courseName": "Programming Fundamentals",
                    "yearDate": 2023,
                    "term": "T3",
                    "school": "School of Computer Science and Engineering"
                },
                {
                    "courseCode": "COMP6080",
                    "courseName": "Web Front-End Programming",
                    "yearDate": 2023,
                    "term": "T3",
                    "school": "School of Computer Science and Engineering"
                },
                # ... additional course entries ...
            ]
        }

    Response Codes:
    - 200 OK: Successful retrieval of course list.
    """
    return return_all_courses(), 200


@admin.route("/admin/all-projects", methods=["GET"])
@jwt_required()
def get_project_list():
    """
    Retrieve a list of all projects in the system.

    Requires a valid JWT token for authentication.

    Endpoint:
    GET /admin/all-projects

    Returns:
    - A JSON response containing information about all projects, including their
    project ID, project name,
      and client.

    Example:
    {
        "projects": [
            {
                "id": 1,
                "projectName": "Website Redesign",
                "client": "ABC Corporation"
            },
            {
                "id": 2,
                "projectName": "Mobile App Development",
                "client": "XYZ Company"
            },
            # ... additional project entries ...
        ]
    }

    Response Codes:
    - 200 OK: Successful retrieval of project list.
    """
    return return_all_projects(), 200


@admin.route("/admin/dashboard", methods=["GET"])
@jwt_required()
def admin_stats():
    """
    Retrieve statistics for the admin dashboard.

    Requires a valid JWT token for authentication.

    Endpoint:
    GET /admin/dashboard

    Returns:
    - A JSON response containing statistics for the admin dashboard, including:
        - "userCount": The count of users categorized by type (student, academic,
        course admin, admin).
        - "courseCount": The total count of courses in the system.
        - "projectCount": The total count of projects in the system.

    Example:
    {
        "dashboard": {
            "userCount": {
                "student": 150,
                "casualAcademic": 20,
                "academic": 50,
                "courseAdmin": 10,
                "admin": 5
            },
            "courseCount": 15,
            "projectCount": 25
        }
    }

    Response Codes:
    - 200 OK: Successful retrieval of admin dashboard statistics.
    """
    user_count_stat = user_type_count()
    course_count = get_course_count()
    project_count = get_project_count()

    return (
        jsonify(
            {
                "dashboard": {
                    "userCount": user_count_stat,
                    "courseCount": course_count,
                    "projectCount": project_count,
                }
            }
        ),
        200,
    )


@admin.route("/admin/course/delete", methods=["DELETE"])
@jwt_required()
def delete_course():
    """
    Delete a course and its related data from the system.

    Requires a valid JWT token for authentication.

    Endpoint:
    DELETE /admin/course/delete

    Request JSON Payload:
    {
        "courseCode": "COMP1511",
        "yearDate": 2023,
        "term": "T3"
    }

    Returns:
    - A JSON response with a success message if the course is successfully deleted.
      If the course is not found, a JSON response with an error message and a 404
      status code is returned.

    Example:
    Successfully deleted course

    Response Codes:
    - 200 OK: Successful deletion of the course.
    - 404 Not Found: Course not found.
    """
    data = request.get_json()
    course_code = data["courseCode"]
    year_date = data["yearDate"]
    term = data["term"]
    return delete_course_cascade(course_code, year_date, term)


@admin.route("/admin/group/delete", methods=["DELETE"])
@jwt_required()
def delete_group():
    """
    Delete a group and its related data from the system.

    Requires a valid JWT token for authentication.

    Endpoint:
    DELETE /admin/group/delete

    Request JSON Payload:
    {
        "groupID": 1
    }

    Returns:
    - A JSON response with a success message if the group is successfully deleted.
      If the group is not found, a JSON response with an error message and a
      404 status code is returned.

    Example:
    Successfully deleted group

    Response Codes:
    - 200 OK: Successful deletion of the group.
    - 404 Not Found: Group not found.
    """
    data = request.get_json()
    group_id = data["groupID"]
    return delete_group_cascade(group_id)


@admin.route("/admin/project/delete", methods=["DELETE"])
@jwt_required()
def delete_project():
    """
    Delete a project and its related data from the system.

    Requires a valid JWT token for authentication.

    Endpoint:
    DELETE /admin/project/delete

    Request JSON Payload:
    {
        "ID": 1
    }

    Returns:
    - A JSON response with a success message if the project is successfully deleted.
      If the project is not found, a JSON response with an error message and a 404
      status code is returned.

    Example:
    Successfully deleted project

    Response Codes:
    - 200 OK: Successful deletion of the project.
    - 404 Not Found: Project not found.
    """
    data = request.get_json()
    project_id = data["ID"]
    return delete_project_cascade(project_id)


@admin.route("/admin/user/delete", methods=["DELETE"])
@jwt_required()
def delete_user():
    """
    Delete a user and its related data from the system.

    Requires a valid JWT token for authentication.

    Endpoint:
    DELETE /admin/user/delete

    Request JSON Payload:
    {
        "zID": "z1234567"
    }

    Returns:
    - A JSON response with a success message if the user is successfully deleted.
      If the user is not found, a JSON response with an error message and a 404
      status code is returned.

    Example:
    Successfully deleted user

    Response Codes:
    - 200 OK: Successful deletion of the user.
    - 404 Not Found: User not found.
    """
    data = request.get_json()
    zid = data["zID"]
    return delete_user_cascade(zid)
