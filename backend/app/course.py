'''
This file contains the APIs related to the project dashboard and projects
page. It also contains the functions that those APIs used.

'''
import ast
import sys
import os
from datetime import datetime
import threading
import json

from flask import Blueprint, request, jsonify, current_app, Flask, session
from recommendations.recommend_courses import get_recommended_courses
try:
    from webscraping.scrape_single_course import get_single_course_information
except ImportError:
    from ..webscraping.scrape_single_course import get_single_course_information

try:
    from webscraping.pdf_scraping import *
except ImportError:
    from ..webscraping.pdf_scraping import *
from sqlalchemy import desc
from flask_jwt_extended import jwt_required, get_jwt_identity
try:
    from models import db, User, CourseEnrolment, Course, CourseArchive
except ImportError:
    from .models import db, User, CourseEnrolment, Course, CourseArchive

current_directory = os.getcwd()
# Get the parent directory
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

course = Blueprint("course", __name__)


def publicProfileDisplay(zID):
    """
    Retrieve public information for a user based on their zID.

    Args:
    - zID (str): The zID (unique identifier) of the user.

    Returns:
    - A JSON response containing public information about the user, including:
        - "zID": The zID of the user.
        - "firstName": The first name of the user.
        - "lastName": The last name of the user.
        - "headline": The headline or title of the user.
        - "summary": A brief summary or description of the user.
        - "imageURL": The URL of the user's profile image.
        - "private": A boolean indicating whether the user's profile is private 
            (True) or public (False).

    Response Codes:
    - 200 OK: Successful retrieval of public user profile.
    - 400 Bad Request: Invalid user (zID not found).
    """
    user = User.query.filter_by(zID=zID).first()
    if user.privacy == 1:
        privacy = True
    else:
        privacy = False
    if user:
        user_public_info = {
            "zID": user.zID,
            "firstName": user.firstname,
            "lastName": user.lastname,
            "headline": user.headline,
            "summary": user.summary,
            "imageURL": user.imageURL,
            "private": privacy,
        }

        return jsonify(user_public_info), 200
    else:
        return jsonify({"error": "Invalid User"}), 400

def top_ten_items(data):
    """
    Get the top ten items from a dictionary and aggregate the rest into an 'other' category.

    Args:
    - data (dict): A dictionary where keys represent items and values represent their scores.

    Returns:
    - A dictionary containing the top ten items and their scores, with the rest
        aggregated under the 'other' category.
    }
    """
    # Sort the dictionary by values in descending order
    sorted_data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))

    # Get the top N items
    top_n = dict(list(sorted_data.items())[:9])

    # Calculate the 'other' score by summing the rest
    other_score = sum(list(sorted_data.values())[9:])

    # Add the 'other' category to the result
    top_n["other"] = other_score

    return top_n


def get_profile_skills(zid, role):
    """
    Get the top skills for a user based on their zID and role.

    Args:
    - zid (str): The zID (unique identifier) of the user.
    - role (str): The role for which skills are to be retrieved (e.g., "academic", "student").

    Returns:
    - A JSON response containing the top skills for the specified user and role.

    Response Codes:
    - 200 OK: Successful retrieval of user skills.
    - 400 Bad Request: Invalid user (zID not found).
    """
    user = User.query.filter_by(zID=zid).first()
    if user:
        metadata = json.loads(user.metadataJson)
        skills = top_ten_items(metadata["class"][role]["skills"])
        return jsonify({"skills": skills}), 200
    else:
        return jsonify({"error": "Invalid User"}), 400



def get_profile_knowledge(zid, role):
    """
    Get the top knowledge areas for a user based on their zID and role.

    Args:
    - zid (str): The zID (unique identifier) of the user.
    - role (str): The role for which knowledge areas are to be retrieved
    (e.g., "academic", "student").

    Returns:
    - A JSON response containing the top knowledge areas for the specified user and role.

    Response Codes:
    - 200 OK: Successful retrieval of user knowledge areas.
    - 400 Bad Request: Invalid user (zID not found).
    """

    user = User.query.filter_by(zID=zid).first()
    if user:
        metadata = json.loads(user.metadataJson)
        knowledge = top_ten_items(metadata["class"][role]["knowledge"])
        return jsonify({"knowledge": knowledge}), 200
    else:
        return jsonify({"error": "Invalid User"}), 400


def getCourseList(zid, role):
    """
    Get the list of courses enrolled by a user based on their zID and role.

    Args:
    - zid (str): The zID (unique identifier) of the user.
    - role (str): The role for which course enrollment is to be retrieved
    (e.g., "student", "academic").

    Returns:
    - A JSON response containing information about the courses enrolled by the specified user
    and role.

    Response Codes:
    - 200 OK: Successful retrieval of user's course list.
    """
    user_course_list = (
        db.session.query(CourseEnrolment).filter_by(user=zid, courseRole=role).all()
    )

    user_course_list_dict = []
    for course_enrolled in user_course_list:
        course_info = Course.query.filter_by(ID=course_enrolled.course).first()
        course_info_dict = {
            "courseCode": course_info.courseCode,
            "courseName": course_info.courseName,
            "yearDate": course_info.yearDate,
            "term": course_info.term,
            "school": course_info.school,
        }
        user_course_list_dict.append(course_info_dict)
    return json.dumps({"courses": user_course_list_dict})

def addCourseEnrolment(zid, course_id, role):
    """
    Add a user's enrollment in a course with the specified role.

    Args:
    - zid (str): The zID (unique identifier) of the user.
    - course_id (int): The ID of the course to be enrolled in.
    - role (str): The role in the course for the user (e.g., "student", "academic").

    Returns:
    - None

    Response Codes:
    - No direct response; the function updates the database.
    """

    new_course_enrolment = CourseEnrolment(user=zid, course=course_id, courseRole=role)
    db.session.add(new_course_enrolment)


    user = User.query.filter_by(zID=zid).first()
    enrolling_course = Course.query.filter_by(ID=course_id).first()
    metadata = json.loads(user.metadataJson)

    user_skills = metadata["class"][role]["skills"]
    course_skills = json.loads(enrolling_course.courseSkills)
    for skill, weight in course_skills.items():
        if skill in list(user_skills.keys()):
            user_skills[skill] = user_skills[skill] + weight
        else:
            user_skills[skill] = weight

    user_knowledge = metadata["class"][role]["knowledge"]
    course_knowledge = json.loads(enrolling_course.courseKnowledge)
    for knowledge, weight in course_knowledge.items():
        if knowledge in list(user_knowledge.keys()):
            user_knowledge[knowledge] = user_knowledge[knowledge] + weight
        else:
            user_knowledge[knowledge] = weight

    user.metadataJson = json.dumps(metadata)
    db.session.commit()


def deleteCourseEnrolment(zid, course_id, role):
    """
    Delete a user's enrollment in a course with the specified role.

    Args:
    - zid (str): The zID (unique identifier) of the user.
    - course_id (int): The ID of the course to be unenrolled from.
    - role (str): The role in the course for the user (e.g., "student", "academic").

    Returns:
    - None

    Response Codes:
    - No direct response; the function updates the database.
    """
    CourseEnrolment.query.filter_by(user=zid, course=course_id, courseRole=role).delete()

    remove_course = Course.query.filter_by(ID=course_id).first()
    user = User.query.filter_by(zID=zid).first()
    metadata = json.loads(user.metadataJson)

    user_skills = metadata["class"][role]["skills"]
    course_skills = json.loads(remove_course.courseSkills)
    for skill, weight in course_skills.items():
        if skill in user_skills.keys():
            user_skills[skill] = user_skills[skill] - weight
            if user_skills[skill] <= 0:
                user_skills.pop(skill, None)
        else:
            user_skills[skill] = weight

    user_knowledge = metadata["class"][role]["knowledge"]
    course_knowledge = json.loads(remove_course.courseKnowledge)
    for knowledge, weight in course_knowledge.items():
        if knowledge in user_knowledge.keys():
            user_knowledge[knowledge] = user_knowledge[knowledge] - weight
            if user_knowledge[knowledge] <= 0:
                user_knowledge.pop(knowledge, None)
        else:
            user_knowledge[knowledge] = weight

    user.metadataJson = json.dumps(metadata)
    db.session.commit()



def getRecommendedCourses(zid):
    """
    Get a list of recommended courses for a student based on their completed courses,
    skills, and knowledge.

    Args:
    - zid (str): The zID (unique identifier) of the student.

    Returns:
    - A JSON response containing information about the recommended courses for the specified
    student.

    Response Codes:
    - 200 OK: Successful retrieval of recommended courses.
    - 200 OK (Empty): No recommended courses available.
    """
    completed_course_data = json.loads(getCourseList(zid, "student"))["courses"]
    completed_courses = [course["courseCode"] for course in completed_course_data]
    user = User.query.filter_by(zID=zid).first()
    user_metadata = json.loads(user.metadataJson)
    user_knowledge = user_metadata["class"]["student"]["knowledge"]
    user_skills = user_metadata["class"]["student"]["skills"]
    user_skills_and_knowledge = {
        term: (user_skills.get(term, 0) + user_knowledge.get(term, 0))
        for term in set(user_skills) | set(user_knowledge)
    }

    all_courses = []
    courses = Course.query.all()
    for recc_course in courses:
        course_code = recc_course.courseCode
        course_set = {d["name"] for d in all_courses}
        if course_code in course_set or course_code in completed_courses:
            continue
        courses = (
            Course.query.filter_by(courseCode=course_code)
            .order_by(desc(Course.yearDate), desc(Course.term))
            .all()
        )
        lattest_course = courses[0]
        course_skills = json.loads(lattest_course.courseSkills)
        course_knowledge = json.loads(lattest_course.courseKnowledge)
        all_courses.append(
            {
                "name": course_code,
                "knowledge": course_knowledge,
                "skills": course_skills,
            }
        )
    if len(all_courses) == 0:
        return {"courses": []}, 200
    recommended_courses = get_recommended_courses(
        user_skills_and_knowledge, all_courses
    )

    if len(recommended_courses) == 0:
        return {"courses": []}, 200

    course_code_recommended = [
        item[0] for item in recommended_courses if item[0] not in completed_courses
    ]

    top_recommended_courses = course_code_recommended[:10]

    recommended_courses_info = []

    for recc_course in top_recommended_courses:
        course_all_info = (
            Course.query.filter_by(courseCode=recc_course)
            .order_by(desc(Course.yearDate), desc(Course.term))
            .all()
        )
        course_all_info = course_all_info[0]
        course_required_info = {
            "name": course_all_info.courseName,
            "code": course_all_info.courseCode,
            "school": course_all_info.school,
            "thumbnail": course_all_info.thumbnail,
        }

        recommended_courses_info.append(course_required_info)

    return {"courses": recommended_courses_info}, 200


def add_course_to_db(course_info):
    """
    Create a new Course object and populate it with the provided course information.

    Args:
    - course_info (dict): A dictionary containing information about the course.

    Returns:
    - Course: A new Course object populated with the provided information.
    """
    new_course = Course(
        courseCode=course_info["course"],
        courseName=course_info["course_name"],
        courseDescription=course_info["course_description"],
        courseSkills=json.dumps(course_info["course_skills"]),
        courseKnowledge=json.dumps(course_info["course_knowledge"]),
        topics=json.dumps(course_info["course_topics"]),
        yearDate=course_info["course_year"],
        term=course_info["course_term"],
        revision=course_info["course_scraped"],
        school=course_info["course_school"],
    )

    return new_course


def webscrapeUsingURL(url):
    """
    Perform web scraping to retrieve information about a course from the provided URL.

    Args:
    - url (str): The URL of the webpage containing information about the course.

    Returns:
    - dict: A dictionary containing information about the course obtained through web scraping.
"""
    return get_single_course_information(url)


def getID(zID):
    """
    Retrieve a user's information by their zID.

    Args:
    - zID (str): The zID (unique identifier) of the user.

    Returns:
    - User: The User object corresponding to the provided zID.

    Response Codes:
    - 200 OK: Successful retrieval of user information.
    - 404 Not Found: User not found with the provided zID.
    """
    return User.query.filter_by(zID=zID).first()


@course.route("/courses/academic", methods=["GET"])
@jwt_required()  # decorator verifies the JWT token
def getAcademicCourse():
    """
    Get a list of courses associated with the academic user.

    Returns:
    - A JSON response containing information about the academic user's enrolled courses.

    Response Codes:
    - 200 OK: Successful retrieval of academic user's enrolled courses.
    - 401 Unauthorized: Invalid token.
    - 403 Forbidden: User is not an academic.
    """
    current_user_id = get_jwt_identity()

    # identify user role
    user = getID(current_user_id)
    if not user:
        return jsonify({"error": "Invalid token."}), 401
    metaData = json.loads(user.metadataJson)
    role = list(metaData["class"].keys())
    if "admin" in role:
        role = "admin"
    elif "academic" in role:
        role = "academic"
    else:
        role = "student"
    if role == "student":
        return jsonify({"error": "User is not an academic."}), 403

    # search for courses
    enrolment_course = (
        db.session.query(CourseEnrolment, Course, User)
        .join(Course, Course.ID == CourseEnrolment.course)
        .join(User, User.zID == CourseEnrolment.user)
        .filter(User.zID == current_user_id)
        .all()
    )

    data = []
    for enrolment, course, user in enrolment_course:
        existing_course = list({course["code"] for course in data})

        if not course.courseCode in existing_course:
            data.append(
                {
                    "name": course.courseName,
                    "code": course.courseCode,
                    "school": course.school,
                    "thumbnail": course.thumbnail,
                }
            )

    return jsonify({"courses": data}), 200


@course.route("/courses/<courseCode>", methods=["GET"])
@jwt_required()  # decorator verifies the JWT token
def get_course_code(courseCode):
    """
    Get detailed information about a specific course identified by its courseCode.

    Args:
    - courseCode (str): The code identifying the course.

    Returns:
    - A JSON response containing detailed information about the specified course.

    Response Codes:
    - 200 OK: Successful retrieval of course information.
    - 401 Unauthorized: Invalid token.
    - 404 Not Found: Course not found.
    """
    current_user_id = get_jwt_identity()

    # identify user role
    user = getID(current_user_id)
    if not user:
        return jsonify({"error": "Invalid token."}), 401
    metaData = json.loads(user.metadataJson)
    role = list(metaData["class"].keys())
    if "admin" in role:
        role = "admin"
    elif "academic" in role:
        role = "academic"
    else:
        role = "student"
    course = (
        Course.query.filter_by(courseCode=courseCode)
        .order_by(desc(Course.yearDate), desc(Course.term))
        .first()
    )
    if not course:
        return jsonify({"error": "Course not found."}), 404
    archived = CourseArchive.query.filter_by(courseID=course.ID).all()
    archive_count = len(archived)
    availableYearTerm = [[course.yearDate, course.term]]

    courseAll = Course.query.filter_by(courseCode=courseCode).all()
    for i in range(len(courseAll)):
        if [courseAll[i].yearDate, courseAll[i].term] not in availableYearTerm:
            availableYearTerm.append([courseAll[i].yearDate, courseAll[i].term])

    for i in range(archive_count):
        if [archived[i].yearDate, archived[i].term] not in availableYearTerm:
            availableYearTerm.append([archived[i].yearDate, archived[i].term])

    data = {
        "name": course.courseName,
        "code": course.courseCode,
        "school": course.school,
        "description": course.courseDescription,
        "skills": json.loads(course.courseSkills),
        "knowledge": json.loads(course.courseKnowledge),
        "topics": ast.literal_eval(course.topics),
        "thumbnail": course.thumbnail,
        "currentYear": course.yearDate,
        "currentTerm": course.term,
        "currentVersion": archive_count + 1,
        "availableVersions": [i + 1 for i in range(archive_count + 1)],
        "availableYearTerms": availableYearTerm,
    }

    return jsonify(data), 200


@course.route("/courses/<courseCode>/<year>/<term>", methods=["GET"])
@jwt_required()  # decorator verifies the JWT token
def get_course_term(courseCode, year, term):
    """
    Get detailed information about a specific course for a given year and term.

    Args:
    - courseCode (str): The code identifying the course.
    - year (str): The year in which the course is offered.
    - term (str): The term in which the course is offered.

    Returns:
    - A JSON response containing detailed information about the specified
    course for the given year and term.

    Response Codes:
    - 200 OK: Successful retrieval of course information.
    - 401 Unauthorized: Invalid token.
    - 404 Not Found: Course not found.
    """
    current_user_id = get_jwt_identity()

    # idnetify user role
    user = getID(current_user_id)
    if not user:
        return jsonify({"error": "Invalid token."}), 401
    metaData = json.loads(user.metadataJson)
    role = list(metaData["class"].keys())
    if "admin" in role:
        role = "admin"
    elif "academic" in role:
        role = "academic"
    else:
        role = "student"
    course = Course.query.filter_by(
        courseCode=courseCode, yearDate=year, term=term
    ).first()
    if not course:
        return jsonify({"error": "Course not found."}), 404

    # find archive course
    archived = CourseArchive.query.filter_by(courseID=course.ID).all()
    archive_count = len(archived)
    availableYearTerm = [[course.yearDate, course.term]]

    courseAll = Course.query.filter_by(courseCode=courseCode).all()
    for i in range(len(courseAll)):
        if [courseAll[i].yearDate, courseAll[i].term] not in availableYearTerm:
            availableYearTerm.append([courseAll[i].yearDate, courseAll[i].term])

    for i in range(archive_count):
        if [archived[i].yearDate, archived[i].term] not in availableYearTerm:
            availableYearTerm.append([archived[i].yearDate, archived[i].term])

    data = {
        "name": course.courseName,
        "code": course.courseCode,
        "school": course.school,
        "description": course.courseDescription,
        "skills": json.loads(course.courseSkills),
        "knowledge": json.loads(course.courseKnowledge),
        "topics": ast.literal_eval(course.topics),
        "thumbnail": course.thumbnail,
        "currentYear": course.yearDate,
        "currentTerm": course.term,
        "currentVersion": archive_count + 1,
        "availableVersions": [i + 1 for i in range(archive_count + 1)],
        "availableYearTerms": availableYearTerm,
    }

    return jsonify(data), 200


@course.route("/courses/<courseCode>/<year>/<term>/<version>", methods=["GET"])
@jwt_required()  # decorator verifies the JWT token
def get_course_version(courseCode, year, term, version):
    """
    Get detailed information about a specific version of a course for a given year and term.

    Args:
    - courseCode (str): The code identifying the course.
    - year (str): The year in which the course is offered.
    - term (str): The term in which the course is offered.
    - version (int): The version number of the course.

    Returns:
    - A JSON response containing detailed information about the specified
    version of the course for the given year and term.

    Response Codes:
    - 200 OK: Successful retrieval of course version information.
    - 401 Unauthorized: Invalid token.
    - 404 Not Found: Course not found or version not available.
    """
    current_user_id = get_jwt_identity()

    # identify user role
    user = getID(current_user_id)
    if not user:
        return jsonify({"error": "Invalid token."}), 401
    metaData = json.loads(user.metadataJson)
    role = list(metaData["class"].keys())
    if "admin" in role:
        role = "admin"
    elif "academic" in role:
        role = "academic"
    else:
        role = "student"


    version = int(version)
    # get course info archive
    course = Course.query.filter_by(
        courseCode=courseCode, yearDate=year, term=term
    ).first()
    if not course:
        return jsonify({"error": "Course not found."}), 404

    # get achive course info, sorted by the revision asc
    archive = (
        CourseArchive.query.filter_by(courseID=course.ID)
        .order_by(CourseArchive.revision.asc())
        .all()
    )
    archive_count = len(archive)

    availableYearTerm = [[course.yearDate, course.term]]

    courseAll = Course.query.filter_by(courseCode=courseCode).all()
    for i in range(len(courseAll)):
        if [courseAll[i].yearDate, courseAll[i].term] not in availableYearTerm:
            availableYearTerm.append([courseAll[i].yearDate, courseAll[i].term])

    for i in range(archive_count):
        if [archive[i].yearDate, archive[i].term] not in availableYearTerm:
            availableYearTerm.append([archive[i].yearDate, archive[i].term])

    data = None
    if version == archive_count + 1:
        # return current info
        data = {
            "name": course.courseName,
            "code": course.courseCode,
            "school": course.school,
            "description": course.courseDescription,
            "skills": json.loads(course.courseSkills),
            "knowledge": json.loads(course.courseKnowledge),
            "topics": ast.literal_eval(course.topics),
            "thumbnail": course.thumbnail,
            "currentYear": course.yearDate,
            "currentTerm": course.term,
            "currentVersion": archive_count + 1,
            "availableVersions": [i + 1 for i in range(archive_count + 1)],
            "availableYearTerms": availableYearTerm,
        }
    else:
        version = version - 1
        # return archive course
        data = {
            "name": archive[version].courseName,
            "code": archive[version].courseCode,
            "school": archive[version].school,
            "description": archive[version].courseDescription,
            "skills": json.loads(archive[version].courseSkills),
            "knowledge": json.loads(archive[version].courseKnowledge),
            "topics": ast.literal_eval(archive[version].topics),
            "currentYear": archive[version].yearDate,
            "currentTerm": archive[version].term,
            "thumbnail": archive[version].thumbnail,
            "currentVersion": version + 1,
            "availableVersions": [i + 1 for i in range(archive_count + 1)],
            "availableYearTerms": availableYearTerm,
        }

    return jsonify(data), 200


@course.route("/courses/<courseCode>/<year>/<term>", methods=["PUT"])
@jwt_required()  # decorator verifies the JWT token
def courses_create_edit(courseCode, year, term):
    """
    Create or edit a course, and enroll the requesting user as an academic in the course.

    Args:
    - courseCode (str): The code identifying the course.
    - year (str): The year in which the course is offered.
    - term (str): The term in which the course is offered.

    Returns:
    - A JSON response indicating the success or failure of the course creation or update.

    Response Codes:
    - 200 OK: Successful course creation or update.
    - 400 Bad Request: Fields are missing in the request.
    - 401 Unauthorized: Invalid token.
    - 403 Forbidden: User is not an academic.
    """
    current_user_id = get_jwt_identity()
    user = getID(current_user_id)

    # identify user role
    if not user:
        return jsonify({"error": "Invalid token."}), 401
    metaData = json.loads(user.metadataJson)
    role = list(metaData["class"].keys())
    if "admin" in role:
        role = "admin"
    elif "academic" in role:
        role = "academic"
    else:
        role = "student"
    if role == "student":
        return jsonify({"error": "User is not an academic."}), 403

    # create course
    data = request.get_json()
    courseCode = data.get("code")
    year = data.get("year")
    term = data.get("term")
    course = Course.query.filter_by(
        courseCode=courseCode, yearDate=year, term=term
    ).first()
    if not course:
        try:
            course = Course(
                courseCode=data.get("code"),
                courseName=data.get("name"),
                courseDescription=data.get("description"),
                courseSkills=json.dumps(data.get("skills")),
                courseKnowledge=json.dumps(data.get("knowledge")),
                topics=json.dumps(data.get("topics")),
                yearDate=data.get("year"),
                term=data.get("term"),
                school=data.get("school"),
                thumbnail=data.get("thumbnail"),
                revision=datetime.now(),
            )
        except:
            return jsonify({"error": "Fields miss, please check."}), 400

        db.session.add(course)
        db.session.commit()

        new_course = Course.query.filter_by(
            courseCode=data.get("code"),
            yearDate=data.get("year"),
            term=data.get("term"),
        ).first()
        new_course_enrolment = CourseEnrolment(
            user=user.zID, course=new_course.ID, courseRole="academic"
        )
        db.session.add(new_course_enrolment)
        db.session.commit()
        return jsonify({"message": "Course created successfully."}), 200

    # # archive old course info into archive table, set revision as current time
    archive = CourseArchive(
        courseID=course.ID,
        courseCode=course.courseCode,
        courseName=course.courseName,
        courseDescription=course.courseDescription,
        courseSkills=course.courseSkills,
        courseKnowledge=course.courseKnowledge,
        topics=course.topics,
        yearDate=course.yearDate,
        term=course.term,
        school=course.school,
        thumbnail=course.thumbnail,
        revision=course.revision,
    )

    # update course info
    data = request.get_json()
    # print(data.get('courseSkills'))

    course.courseName = data.get("name")
    course.courseCode = data.get("code")
    course.courseDescription = data.get("description")
    course.courseSkills = json.dumps(data.get("skills"))
    course.courseKnowledge = json.dumps(data.get("knowledge"))
    course.topics = json.dumps(data.get("topics"))
    course.yearDate = data.get("year")
    course.term = data.get("term")
    course.school = data.get("school")
    course.thumbnail = data.get("thumbnail")
    course.revision = datetime.now()
    if course.courseName is None:
        db.session.rollback()
        return jsonify({"error": "Fields miss, please check."}), 400
    if course.courseCode is None:
        db.session.rollback()
        return jsonify({"error": "Fields miss, please check."}), 400
    if course.courseDescription is None:
        db.session.rollback()
        return jsonify({"error": "Fields miss, please check."}), 400
    if course.courseSkills is None:
        db.session.rollback()
        return jsonify({"error": "Fields miss, please check."}), 400
    if course.courseKnowledge is None:
        db.session.rollback()
        return jsonify({"error": "Fields miss, please check."}), 400
    if course.topics is None:
        db.session.rollback()
        return jsonify({"error": "Fields miss, please check."}), 400
    if course.yearDate is None:
        db.session.rollback()
        return jsonify({"error": "Fields miss, please check."}), 400
    if course.term is None:
        db.session.rollback()
        return jsonify({"error": "Fields miss, please check."}), 400
    if course.school is None:
        db.session.rollback()
        return jsonify({"error": "Fields miss, please check."}), 400
    if course.thumbnail is None:
        db.session.rollback()
        return jsonify({"error": "Fields miss, please check."}), 400
    if course.revision is None:
        db.session.rollback()
        return jsonify({"error": "Fields miss, please check."}), 400
    db.session.add(archive)
    db.session.commit()

    assigned_academic = CourseEnrolment.query.filter_by(
        course=course.ID, user=user.zID
    ).first()
    if not assigned_academic:
        new_course_enrolment = CourseEnrolment(
            user=user.zID, course=course.ID, courseRole="academic"
        )
        db.session.add(new_course_enrolment)
        db.session.commit()

    return jsonify({"message": "Course updated successfully."}), 200


@course.route("/student/course", methods=["GET"])
@jwt_required()
def getStudentCourseEnrolment():
    """
    Get the course enrolment details for a student.

    Args:
    - zID (int): The zID of the student.

    Returns:
    - A JSON response containing the course enrolment details for the specified student.

    Response Codes:
    - 200 OK: Successful retrieval of course enrolment details.
    - 400 Bad Request: Invalid user.
    - 401 Unauthorized: Invalid token.
    """
    zID = int(request.args.get("zID"))
    user = User.query.filter_by(zID=zID).first()
    if user:
        return json.loads(getCourseList(zID, "student")), 200
    else:
        return jsonify({"error": "Invalid user"}), 400


@course.route("/student/course/add", methods=["POST"])
@jwt_required()
def addStudentCourseEnrolment():
    """
    Enrol a student in a course.

    Args:
    - zID (str): The zID of the student.
    - courseCode (str): The code of the course.
    - yearDate (str): The year of the course.
    - term (str): The term of the course.

    Returns:
    - An empty JSON response indicating a successful enrolment.

    Response Codes:
    - 200 OK: Successful enrolment.
    - 400 Bad Request: Invalid user or course. Student may be already enrolled.
    - 401 Unauthorized: Invalid token.
    """
    data = request.get_json()
    zID = data["zID"]
    courseCode = data["courseCode"]
    yearDate = data["yearDate"]
    term = data["term"]
    user = User.query.filter_by(zID=zID).first()
    course = Course.query.filter_by(
        courseCode=courseCode, yearDate=yearDate, term=term
    ).first()
    if not (course):
        return jsonify({"error": "Invalid course"}), 400

    enrolledCourse = CourseEnrolment.query.filter_by(
        user=zID, courseRole="student", course=course.ID
    ).first()
    if enrolledCourse:
        return jsonify({"error": "Already enrolled!"}), 400

    if user:
        addCourseEnrolment(zID, course.ID, "student")
        return jsonify({}), 200
    else:
        return jsonify({"error": "Invalid user"}), 400


@course.route("/student/course/delete", methods=["DELETE"])
@jwt_required()
def deleteStudentCourseEnrolment():
    """
    Delete a student's enrolment from a course.

    Args:
    - zID (str): The zID of the student.
    - courseCode (str): The code of the course.
    - yearDate (str): The year of the course.
    - term (str): The term of the course.

    Returns:
    - An empty JSON response indicating a successful deletion.

    Response Codes:
    - 200 OK: Successful deletion.
    - 400 Bad Request: Invalid user, course, or course enrolment.
    - 401 Unauthorized: Invalid token.
    """
    data = request.get_json()
    zID = data["zID"]
    courseCode = data["courseCode"]
    yearDate = data["yearDate"]
    term = data["term"]
    user = User.query.filter_by(zID=zID).first()
    course = Course.query.filter_by(
        courseCode=courseCode, yearDate=yearDate, term=term
    ).first()
    if not (course):
        return jsonify({"error": "Invalid course"}), 400

    if not (user):
        return jsonify({"error": "Invalid user"}), 400
    try:
        deleteCourseEnrolment(user.zID, course.ID, "student")
        return jsonify({}), 200
    except:
        return jsonify({"error": "Invalid course enrolment"}), 400


@course.route("/academic/course", methods=["GET"])
@jwt_required()
def getAcademicCourseEnrolment():
    """
    Retrieve the list of academic courses for a user.

    Args:
    - zID (str): The zID of the academic user.

    Returns:
    - JSON response containing the academic course list.

    Response Codes:
    - 200 OK: Successful retrieval.
    - 400 Bad Request: Invalid user.
    - 401 Unauthorized: Invalid token.
    """
    zID = int(request.args.get("zID"))
    user = User.query.filter_by(zID=zID).first()
    if user:
        return json.loads(getCourseList(zID, "academic")), 200
    else:
        return jsonify({"error": "Invalid user"}), 400


@course.route("/academic/course/add", methods=["POST"])
@jwt_required()
def addAcademicCourseEnrolment():
    """
    Add an academic user to a specific course enrolment.

    Args:
    - zID (str): The zID of the academic user.
    - courseCode (str): The code of the course to be enrolled.
    - yearDate (int): The year of the course.
    - term (str): The term of the course.

    Returns:
    - JSON response indicating the success of the enrolment.

    Response Codes:
    - 200 OK: Successful enrolment.
    - 400 Bad Request: Invalid user or course.
    - 401 Unauthorized: Invalid token.
    - 403 Forbidden: Already enrolled in the course.
    """
    data = request.get_json()
    zID = data["zID"]
    courseCode = data["courseCode"]
    yearDate = data["yearDate"]
    term = data["term"]
    user = User.query.filter_by(zID=zID).first()
    course = Course.query.filter_by(
        courseCode=courseCode, yearDate=yearDate, term=term
    ).first()
    if not (course):
        return jsonify({"error": "Invalid course"}), 400

    enrolledCourse = CourseEnrolment.query.filter_by(
        user=zID, courseRole="academic", course=course.ID
    ).first()
    if enrolledCourse:
        return jsonify({"error": "Already enrolled!"}), 400

    if user:
        addCourseEnrolment(zID, course.ID, "academic")
        return jsonify({}), 200
    else:
        return jsonify({"error": "Invalid user"}), 400


@course.route("/academic/course/delete", methods=["DELETE"])
@jwt_required()
def deleteAcademicCourseEnrolment():
    """
    Delete an academic user from a specific course enrolment.

    Args:
    - zID (str): The zID of the academic user.
    - courseCode (str): The code of the course from which to be unenrolled.
    - yearDate (int): The year of the course.
    - term (str): The term of the course.

    Returns:
    - JSON response indicating the success of the unenrolment.

    Response Codes:
    - 200 OK: Successful unenrolment.
    - 400 Bad Request: Invalid user or course.
    - 401 Unauthorized: Invalid token.
    """
    data = request.get_json()
    zID = data["zID"]
    courseCode = data["courseCode"]
    yearDate = data["yearDate"]
    term = data["term"]
    user = User.query.filter_by(zID=zID).first()
    course = Course.query.filter_by(
        courseCode=courseCode, yearDate=yearDate, term=term
    ).first()
    if not (course):
        return jsonify({"error": "Invalid course"}), 400

    if not (user):
        return jsonify({"error": "Invalid user"}), 400
    deleteCourseEnrolment(user.zID, course.ID, "academic")
    return jsonify({}), 200


@course.route("/courses/student", methods=["GET"])
@jwt_required()
def recommendedCourses():
    """
    Get a list of recommended courses for the current user.

    Returns:
    - JSON response containing a list of recommended courses.

    Response Codes:
    - 200 OK: Successful retrieval of recommended courses.
    - 401 Unauthorized: Invalid token.
    - 404 Not Found: User not found.

    Response JSON:
    {
      "courses": [
        {
          "name": "Introduction to Python",
          "code": "COMP101",
          "school": "Computer Science",
          "thumbnail": "https://example.com/thumbnail.jpg"
        },
        // Additional recommended courses...
      ]
    }
    """
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(zID=current_user_id).first()
    # identify user role
    if not user:
        return jsonify({"error": "Invalid token."}), 401

    response = getRecommendedCourses(user.zID)
    return response


@course.route("/courses/url", methods=["PUT"])
@jwt_required()
def updateCourseInformationURL():
    """
    Initiate the update of course information using a provided UNSW course outline URL.

    Args:
    - None (Arguments are extracted from the JSON payload in the request).

    Returns:
    - JSON response indicating that the course web scraping is in progress.

    Response Codes:
    - 200 OK: Course web scraping initiated successfully.
    - 400 Bad Request: Invalid UNSW course outline URL.
    - 401 Unauthorized: Invalid token.

    Response JSON:
    {
      "message": "Course web scraping in progress."
    }
    """
    current_user_id = get_jwt_identity()
    user = getID(current_user_id)

    # identify user role
    if not user:
        return jsonify({"error": "Invalid token."}), 401
    metaData = json.loads(user.metadataJson)
    role = list(metaData["class"].keys())
    if "admin" in role:
        role = "admin"
    elif "academic" in role:
        role = "academic"
    else:
        role = "student"
    if role == "student":
        return jsonify({"error": "User is not an academic."}), 403

    # create course
    data = request.get_json()
    url = data["url"]
    if "unsw.edu.au/course-outlines/course-outline#" not in url:
        return jsonify({"error": "Invalid UNSW course outline url"}), 400

    # Use threading to perform URL scraping concurrently
    scraping_thread = threading.Thread(
        target=process_course_update_url,
        args=(
            current_app._get_current_object(),
            user,
            url,
        ),
    )
    scraping_thread.start()

    # Respond to the client immediately with a 200 status code
    return jsonify({"message": "Course web scraping in progress."}), 200


def process_course_update_url(app, user, url):
    """
    Process the update of course information using a provided UNSW course outline URL.

    Args:
    - app (Flask app): The Flask application context.
    - user (User): The User object representing the academic initiating the update.
    - url (str): The UNSW course outline URL.

    Returns:
    - None
    """
    with app.app_context():
        course_info = webscrapeUsingURL(url)
        existing_course = Course.query.filter_by(
            courseCode=course_info["course"],
            yearDate=course_info["course_year"],
            term=course_info["course_term"],
        ).first()
        if not existing_course:
            new_course = add_course_to_db(course_info)
            db.session.add(new_course)
            db.session.commit()

            course = Course.query.filter_by(
                courseCode=course_info["course"],
                yearDate=course_info["course_year"],
                term=course_info["course_term"],
            ).first()
            new_course_enrolment = CourseEnrolment(
                user=user.zID, course=course.ID, courseRole="academic"
            )
            db.session.add(new_course_enrolment)
            db.session.commit()

            return

        # # archive old course info into archive table
        assinged_academic = CourseEnrolment.query.filter_by(
            course=course_info["course"], user=user.zID
        ).first()
        if not assinged_academic:
            new_course_enrolment = CourseEnrolment(
                user=user.zID, course=existing_course.ID, courseRole="academic"
            )
            db.session.add(new_course_enrolment)
            db.session.commit()

        archive = CourseArchive(
            courseID=existing_course.ID,
            courseCode=existing_course.courseCode,
            courseName=existing_course.courseName,
            courseDescription=existing_course.courseDescription,
            courseSkills=existing_course.courseSkills,
            courseKnowledge=existing_course.courseKnowledge,
            topics=existing_course.topics,
            yearDate=existing_course.yearDate,
            term=existing_course.term,
            school=existing_course.school,
            thumbnail=existing_course.thumbnail,
            revision=existing_course.revision,
        )

        existing_course.courseName = course_info["course_name"]
        existing_course.courseDescription = course_info["course_description"]
        existing_course.courseSkills = json.dumps(course_info["course_skills"])
        existing_course.courseKnowledge = json.dumps(course_info["course_knowledge"])
        existing_course.topics = json.dumps(course_info["course_topics"])
        existing_course.yearDate = course_info["course_year"]
        existing_course.term = course_info["course_term"]
        existing_course.school = course_info["course_school"]
        existing_course.revision = course_info["course_scraped"]
        existing_course.thumbnail = existing_course.thumbnail

        db.session.add(archive)
        db.session.commit()


@course.route("/courses/pdf", methods=["PUT"])
@jwt_required()
def updateCourseInformationPDF():
    """
    Initiate the update of course information from a PDF.

    This function is typically called by an academic user to update course details from a provided PDF file.

    Args:
    - None

    Returns:
    - Flask JSON response: Indicates the initiation of the update process.

    Side Effects:
    - Initiates a background thread to process the PDF and update the course information.
    - Verifies the user's role and authentication.
    - Responds to the client immediately with a 200 status code.

    Example Usage:
      updateCourseInformationPDF()

    Explanation:
    - Retrieves the current user's identity and role.
    - Validates the user as an academic.
    - Extracts information from the provided PDF.
    - Starts a background thread to update the course information.
    - Immediately responds to the client, indicating the initiation of the update process.
    """

    current_user_id = get_jwt_identity()
    user = getID(current_user_id)

    # identify user role
    if not user:
        return jsonify({"error": "Invalid token."}), 401
    metaData = json.loads(user.metadataJson)
    role = list(metaData["class"].keys())
    if "admin" in role:
        role = "admin"
    elif "academic" in role:
        role = "academic"
    else:
        role = "student"
    if role == "student":
        return jsonify({"error": "User is not an academic."}), 403

    # create course
    data = request.get_json()
    pdf = data["pdf"]
    course_information = scrape_pdf(pdf)
    if "UNSW Course Outline" not in course_information[0]:
        return jsonify({"error": "Invalid UNSW course outline pdf"}), 400
    scraping_thread = threading.Thread(
        target=process_course_update_pdf,
        args=(
            current_app._get_current_object(),
            user,
            course_information,
        ),
    )
    scraping_thread.start()

    # Respond to the client immediately with a 200 status code
    return jsonify({"message": "Course pdf scrape update in progress."}), 200


def process_course_update_pdf(app, user, course_information):
    """
    Process and update course information from a PDF.

    Args:
    - app (Flask App): The Flask application context.
    - user (User): The academic user initiating the update.
    - course_information (list): Information extracted from the PDF.

    Returns:
    - None
    """
    with app.app_context():
        course_info = get_single_course_information_from_pdf(course_information)
        existing_course = Course.query.filter_by(
            courseCode=course_info["course"].strip(),
            yearDate=int(course_info["course_year"]),
            term=course_info["course_term"],
        ).first()
        if not existing_course:
            new_course = add_course_to_db(course_info)
            db.session.add(new_course)
            db.session.commit()

            course = Course.query.filter_by(
                courseCode=course_info["course"],
                yearDate=course_info["course_year"],
                term=course_info["course_term"],
            ).first()
            new_course_enrolment = CourseEnrolment(
                user=user.zID, course=course.ID, courseRole="academic"
            )
            db.session.add(new_course_enrolment)
            db.session.commit()
            return

        # # archive old course info into archive table
        assinged_academic = CourseEnrolment.query.filter_by(
            course=course_info["course"], user=user.zID
        ).first()
        if not assinged_academic:
            new_course_enrolment = CourseEnrolment(
                user=user.zID, course=existing_course.ID, courseRole="academic"
            )
            db.session.add(new_course_enrolment)
            db.session.commit()

        archive = CourseArchive(
            courseID=existing_course.ID,
            courseCode=existing_course.courseCode,
            courseName=existing_course.courseName,
            courseDescription=existing_course.courseDescription,
            courseSkills=existing_course.courseSkills,
            courseKnowledge=existing_course.courseKnowledge,
            topics=existing_course.topics,
            yearDate=existing_course.yearDate,
            term=existing_course.term,
            school=existing_course.school,
            thumbnail=existing_course.thumbnail,
            revision=existing_course.revision,
        )

        existing_course.courseName = course_info["course_name"]
        existing_course.courseDescription = course_info["course_description"]
        existing_course.courseSkills = json.dumps(course_info["course_skills"])
        existing_course.courseKnowledge = json.dumps(course_info["course_knowledge"])
        existing_course.topics = json.dumps(course_info["course_topics"])
        existing_course.yearDate = course_info["course_year"]
        existing_course.term = course_info["course_term"]
        existing_course.school = course_info["course_school"]
        existing_course.revision = course_info["course_scraped"]
        existing_course.thumbnail = existing_course.thumbnail

        db.session.add(archive)
        # db.session.add(existing_course)
        db.session.commit()
