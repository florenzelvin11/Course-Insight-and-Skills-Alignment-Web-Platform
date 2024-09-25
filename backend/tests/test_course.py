import ast
from datetime import datetime
import sys
import os

current_directory = os.getcwd()
# Get the parent directory
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)
import hashlib
import json
import pytest
from app.app import app
from app.models import db, User, UserCode, Course, CourseArchive, CourseEnrolment


@pytest.fixture
def client():
    # Create and return a test client for the Flask app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def add_dummy_user_to_db(firstname, lastname, zID, email, password, verified):
    """
    Add a dummy user to the database.

    Parameters:
    - firstname (str): The first name of the user.
    - lastname (str): The last name of the user.
    - zID (str): The unique identifier for the user.
    - email (str): The email address of the user.
    - password (str): The password for the user.
    - verified (bool): The verification status of the user.

    Returns:
    - User: The newly created User object.
    """
    user_data = {
        "class": {"student": {"major": "null", "program": "null", "transcript": "null"}}
    }
    metadata = json.dumps(user_data, indent=2)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    new_user = User(
        zID=zID,
        firstname=firstname,
        lastname=lastname,
        email=email,
        enPassword=hashed_password,
        metadataJson=metadata,
        verified=verified,
    )
    db.session.add(new_user)
    db.session.commit()

    return new_user


def add_academic_user_to_db(firstname, lastname, zID, email, password, verified):
    """
    Add a new academic user to the database.

    Args:
    - firstname (str): The first name of the user.
    - lastname (str): The last name of the user.
    - zID (str): The unique identifier for the user.
    - email (str): The email address of the user.
    - password (str): The password for the user (will be hashed before storing).
    - verified (bool): A flag indicating whether the user's account is verified.

    Returns:
    - User: The newly created User object.
    """
    user_data = {
        "class": {
            "academic": {"major": "null", "program": "null", "transcript": "null"}
        }
    }
    metadata = json.dumps(user_data, indent=2)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    new_user = User(
        zID=zID,
        firstname=firstname,
        lastname=lastname,
        email=email,
        enPassword=hashed_password,
        metadataJson=metadata,
        verified=verified,
    )
    db.session.add(new_user)
    db.session.commit()

    return new_user


def delete_user(zID):
    """
    Delete a user from the database.

    Parameters:
    - zID (str): The unique identifier for the user to be deleted.
    """
    # Find the user by their zID
    user = User.query.filter_by(zID=zID).first()
    if user:
        # Delete the user from the database session
        db.session.delete(user)
        # Commit the changes to the database
        db.session.commit()


def delete_usercode(zID):
    """
    Delete a user's verification code from the database.

    Args:
    - zID (str): The unique identifier for the user whose verification code is to be deleted.
    """
    # Find the user by their zID
    usercode = UserCode.query.filter_by(user=zID).first()
    if usercode:
        # Delete the user from the database session
        db.session.delete(usercode)
        # Commit the changes to the database
        db.session.commit()


def delete_course(courseCode):
    """
    Delete a course and its archive from the database.

    Args:
    - courseCode (str): The code of the course to be deleted.
    """
    course = Course.query.filter_by(courseCode=courseCode).first()
    courseArchive = CourseArchive.query.filter_by(courseCode=courseCode).all()

    for result in courseArchive:
        db.session.delete(result)

    # Find the course by their zID
    if course:
        delete_courseEnrolment(course.ID)
        # Delete the course from the database session
        db.session.delete(course)

    # Commit the changes to the database
    db.session.commit()


def add_dummy_course_to_db(courseCode, courseName, school, yearDate="2022", term="T2"):
    """
    Add a dummy course to the database.

    Args:
    - courseCode (str): The code of the course.
    - courseName (str): The name of the course.
    - school (str): The school to which the course belongs.
    - yearDate (str, optional): The year date of the course (default is "2022").
    - term (str, optional): The term of the course (default is "T2").

    Returns:
    - Course: The newly created course object.
    """
    new_course = Course(
        courseCode=courseCode,
        courseName=courseName,
        school=school,
        yearDate=yearDate,
        term=term,
        courseSkills=json.dumps("{ 'c++': 100}"),
        courseKnowledge=json.dumps("{ 'c++': 100}"),
        topics=json.dumps("['topic', 'topic_2']"),
    )
    db.session.add(new_course)
    db.session.commit()

    return new_course


def assign_course_to_academic(courseID, academicZID):
    """
    Assign a course to an academic in the database.

    Args:
    - courseID (int): The ID of the course to be assigned.
    - academicZID (int): The ZID of the academic user.

    Returns:
    - CourseEnrolment: The newly created course enrolment object.
    """
    # find courseCode courseID
    course = Course.query.filter_by(ID=courseID).first()

    new_courseEnrolment = CourseEnrolment(
        course=courseID, user=academicZID, courseRole="teacher"
    )

    db.session.add(new_courseEnrolment)
    db.session.commit()

    return new_courseEnrolment


def delete_courseEnrolment(courseId):
    # find courseCode courseID
    course = CourseEnrolment.query.filter_by(course=courseId).all()

    for record in course:
        db.session.delete(record)

    db.session.commit()


#####################
#       Tests       #
#####################
def test_successful_course_create(client):
    """
    Test creating a new course successfully by an academic user.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        delete_user(zID="1234569")
        delete_course("COMP9900")
        # Add user to DB
        add_academic_user_to_db(
            "Yanzhi", "Li", "1234569", "z1234569@ad.unsw.edu.au", "Lyz1234569", 1
        )

        # Define user login data
        login_data = {"email": "z1234569@ad.unsw.edu.au", "password": "Lyz1234569"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        course = add_dummy_course_to_db(
            "COMP9900", "Capstone Project", "School of Computer Science and Engineering"
        )
        # course data
        courses = {
            "name": "cs",
            "code": "COMP8900",
            "year": "2022",
            "term": "T2",
            "description": "cs",
            "skills": "python",
            "topics": "123",
            "knowledge": "c",
            "thumbnail": "null",
        }

        # Add the course to DB using set preference
        response = client.put(
            f"/courses/{course.courseCode}/{course.yearDate}/{course.term}",
            headers=headers,
            json=courses,
        )

        # Check if the registration is unsuccessful
        assert response.status_code == 200
        assert "Course created successfully." in response.get_json()["message"]

        delete_course("COMP8900")
        delete_user(zID="1234569")


def test_not_academic_course_create(client):
    """
    Test creating a new course successfully by an academic user.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        delete_user(zID="1234569")
        delete_course("COMP9900")
        # Add user to DB
        add_dummy_user_to_db(
            "Yanzhi", "Li", "1234569", "z1234569@ad.unsw.edu.au", "Lyz1234569", 1
        )

        # Define user login data
        login_data = {"email": "z1234569@ad.unsw.edu.au", "password": "Lyz1234569"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        role = responseData.get("userType")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        course = add_dummy_course_to_db(
            "COMP9900", "Capstone Project", "School of Computer Science and Engineering"
        )
        # course data
        courses = {
            "name": "cs",
            "code": "COMP8900",
            "year": "2022",
            "term": "T2",
            "description": "cs",
            "skills": "python",
            "topics": "123",
            "knowledge": "c",
        }
        response = client.put(
            f"/courses/{course.courseCode}/{course.yearDate}/{course.term}",
            headers=headers,
            json=courses,
        )
        assert response.status_code == 403
        assert "User is not an academic." in response.get_json()["error"]

        delete_course("COMP8900")
        delete_user(zID="1234569")


def test_successful_course_get(client):
    """
    Test creating a new course successfully by an academic user.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        delete_course("COMP9900")
        delete_user(zID="1234567")
        # Add user to DB
        add_academic_user_to_db(
            "Evan", "Li", "1234567", "z1234567@ad.unsw.edu.au", "Lyz1234567", 1
        )

        # Define user login data
        login_data = {"email": "z1234567@ad.unsw.edu.au", "password": "Lyz1234567"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        course = add_dummy_course_to_db(
            "COMP9900", "Capstone Project", "School of Computer Science and Engineering"
        )
        # courses= {
        #     "courseCode": "COMP9900",
        #     "yearDate": "2022",
        #     "term": "T2",
        #     "thumbnail": "null"
        # }

        response = client.get(f"/courses/COMP9900", headers=headers)
        assert response.status_code == 200
        assert response.get_json()["code"] == "COMP9900"

        delete_course("COMP9900")
        delete_user(zID="1234567")


def test_successful_courseTerm_get(client):
    """
    Test successfully retrieving information about a specific course for a given term.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        delete_course("COMP9900")
        delete_user(zID="1234567")
        # Add user to DB
        add_academic_user_to_db(
            "Evan", "Li", "1234567", "z1234567@ad.unsw.edu.au", "Lyz1234567", 1
        )

        # Define user login data
        login_data = {"email": "z1234567@ad.unsw.edu.au", "password": "Lyz1234567"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        course = add_dummy_course_to_db(
            "COMP9900", "Capstone Project", "School of Computer Science and Engineering"
        )
        # courses= {
        #     "courseCode": "COMP9900",
        #     "yearDate": "2022",
        #     "term": "T2"
        # }

        response = client.get(f"/courses/COMP9900/2022/T2", headers=headers)

        assert response.status_code == 200
        assert response.get_json()["code"] == "COMP9900"

        delete_course("COMP9900")
        delete_user(zID="1234567")


def test_course_code_not_found_courseTerm_get(client):
    with app.app_context():
        delete_course("COMP9900")
        delete_user(zID="1234567")
        # Add user to DB
        add_academic_user_to_db(
            "Evan", "Li", "1234567", "z1234567@ad.unsw.edu.au", "Lyz1234567", 1
        )

        # Define user login data
        login_data = {"email": "z1234567@ad.unsw.edu.au", "password": "Lyz1234567"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        course = add_dummy_course_to_db(
            "COMP9900", "Capstone Project", "School of Computer Science and Engineering"
        )

        response = client.get(f"/courses/COMP900/2022/T2", headers=headers)

        assert response.status_code == 404
        assert response.get_json()["error"] == "Course not found."

        delete_course("COMP9900")
        delete_user(zID="1234567")


def test_course_yearDate_not_found_courseTerm_get(client):
    """
    Test handling the case where the specified course code is not found when retrieving course 
    information for a given term.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        delete_course("COMP9900")
        delete_user(zID="1234567")
        # Add user to DB
        add_academic_user_to_db(
            "Evan", "Li", "1234567", "z1234567@ad.unsw.edu.au", "Lyz1234567", 1
        )

        # Define user login data
        login_data = {"email": "z1234567@ad.unsw.edu.au", "password": "Lyz1234567"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        course = add_dummy_course_to_db(
            "COMP9900", "Capstone Project", "School of Computer Science and Engineering"
        )

        response = client.get(f"/courses/COMP9900/2021/T2", headers=headers)

        assert response.status_code == 404
        assert response.get_json()["error"] == "Course not found."

        delete_course("COMP9900")
        delete_user(zID="1234567")


def test_course_term_not_found_courseTerm_get(client):
    """
    Test handling the case where the specified course term is not found 
    when retrieving course information.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        delete_course("COMP9900")
        delete_user(zID="1234567")
        # Add user to DB
        add_academic_user_to_db(
            "Evan", "Li", "1234567", "z1234567@ad.unsw.edu.au", "Lyz1234567", 1
        )

        # Define user login data
        login_data = {"email": "z1234567@ad.unsw.edu.au", "password": "Lyz1234567"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        course = add_dummy_course_to_db(
            "COMP9900", "Capstone Project", "School of Computer Science and Engineering"
        )

        response = client.get(f"/courses/COMP9900/2022/T1", headers=headers)

        assert response.status_code == 404
        assert response.get_json()["error"] == "Course not found."

        delete_course("COMP9900")
        delete_user(zID="1234567")


def test_successful_courseVersion_get(client):
    """
    Test successfully retrieving information about a specific version of a course.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        delete_course("COMP9900")
        delete_user(zID="1234567")
        # Add user to DB
        add_academic_user_to_db(
            "Evan", "Li", "1234567", "z1234567@ad.unsw.edu.au", "Lyz1234567", 1
        )

        # Define user login data
        login_data = {"email": "z1234567@ad.unsw.edu.au", "password": "Lyz1234567"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        course = add_dummy_course_to_db(
            "COMP9900", "Capstone Project", "School of Computer Science and Engineering"
        )

        response = client.get(f"/courses/COMP9900/2022/T2/1", headers=headers)
        assert response.status_code == 200
        assert response.get_json()["code"] == "COMP9900"

        delete_course("COMP9900")
        delete_user(zID="1234567")


def test_course_code_not_found_courseVersion_get(client):
    """
    Test handling the case where the specified course code is not found when 
    retrieving a specific version of a course.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        delete_course("COMP9900")
        delete_user(zID="1234567")
        # Add user to DB
        add_academic_user_to_db(
            "Evan", "Li", "1234567", "z1234567@ad.unsw.edu.au", "Lyz1234567", 1
        )

        # Define user login data
        login_data = {"email": "z1234567@ad.unsw.edu.au", "password": "Lyz1234567"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        course = add_dummy_course_to_db(
            "COMP9900", "Capstone Project", "School of Computer Science and Engineering"
        )

        response = client.get(f"/courses/COMP900/2022/T2/1", headers=headers)

        assert response.status_code == 404
        assert response.get_json()["error"] == "Course not found."

        delete_course("COMP9900")
        delete_user(zID="1234567")


def test_course_yearDate_not_found_courseVersion_get(client):
    """
    Test handling the case where the specified year and term (yearDate) are
    not found when retrieving a specific version of a course.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        delete_course("COMP9900")
        delete_user(zID="1234567")
        # Add user to DB
        add_academic_user_to_db(
            "Evan", "Li", "1234567", "z1234567@ad.unsw.edu.au", "Lyz1234567", 1
        )

        # Define user login data
        login_data = {"email": "z1234567@ad.unsw.edu.au", "password": "Lyz1234567"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        course = add_dummy_course_to_db(
            "COMP9900", "Capstone Project", "School of Computer Science and Engineering"
        )

        response = client.get(f"/courses/COMP9900/2021/T2/1", headers=headers)

        assert response.status_code == 404
        assert response.get_json()["error"] == "Course not found."

        delete_course("COMP9900")
        delete_user(zID="1234567")


def test_course_term_not_found_courseVersion_get(client):
    """
    Test handling the case where the specified term (in a specific year) is not 
    found when retrieving a specific version of a course.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        delete_course("COMP9900")
        delete_user(zID="1234567")
        # Add user to DB
        add_academic_user_to_db(
            "Evan", "Li", "1234567", "z1234567@ad.unsw.edu.au", "Lyz1234567", 1
        )

        # Define user login data
        login_data = {"email": "z1234567@ad.unsw.edu.au", "password": "Lyz1234567"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        course = add_dummy_course_to_db(
            "COMP9900", "Capstone Project", "School of Computer Science and Engineering"
        )

        response = client.get(f"/courses/COMP9900/2022/T1/1", headers=headers)

        assert response.status_code == 404
        assert response.get_json()["error"] == "Course not found."

        delete_course("COMP9900")
        delete_user(zID="1234567")


def test_update_course_info(client):
    """
    Test handling the case where the specified term (in a specific year) is not found when 
    retrieving a specific version of a course.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        delete_course("COMP9900")
        delete_user(zID="1234567")
        # Add user to DB
        add_academic_user_to_db(
            "Evan", "Li", "1234567", "z1234567@ad.unsw.edu.au", "Lyz1234567", 1
        )

        # Define user login data
        login_data = {"email": "z1234567@ad.unsw.edu.au", "password": "Lyz1234567"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        course = add_dummy_course_to_db(
            "COMP9900", "Capstone Project", "School of Computer Science and Engineering"
        )

        newInfo = {
            "name": "cs",
            "code": "COMP9900",
            "year": "2022",
            "term": "T2",
            "description": "cse",
            "skills": "c",
            "topics": "12345",
            "knowledge": "java",
            "thumbnail": "null",
            "revision": datetime.now(),
            "school": "School of Computer Science and Engineering",
        }

        response = client.put(
            f"/courses/{course.courseCode}/{course.yearDate}/{course.term}",
            headers=headers,
            json=newInfo,
        )

        assert response.status_code == 200

        delete_course("COMP9900")
        delete_user(zID="1234567")


def test_not_academic_update_course_info(client):
    """
    Test updating information for a specific version of a course.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        delete_course("COMP9900")
        delete_user(zID="1234567")
        # Add user to DB
        add_dummy_user_to_db(
            "Evan", "Li", "1234567", "z1234567@ad.unsw.edu.au", "Lyz1234567", 1
        )

        # Define user login data
        login_data = {"email": "z1234567@ad.unsw.edu.au", "password": "Lyz1234567"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        course = add_dummy_course_to_db(
            "COMP9900", "Capstone Project", "School of Computer Science and Engineering"
        )

        newInfo = {
            "name": "cs",
            "code": "COMP9900",
            "year": "2022",
            "term": "T2",
            "description": "cse",
            "skills": "c",
            "topics": "12345",
            "knowledge": "java",
        }

        response = client.put(
            f"/courses/{course.courseCode}/{course.yearDate}/{course.term}",
            headers=headers,
            json=newInfo,
        )

        assert response.status_code == 403
        assert response.get_json()["error"] == "User is not an academic."

        delete_course("COMP9900")
        delete_user(zID="1234567")


def test_missing_fields_update_course_info(client):
    """
    Test updating information for a specific version of a course.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        delete_course("COMP9900")
        delete_user(zID="1234567")
        # Add user to DB
        add_academic_user_to_db(
            "Evan", "Li", "1234567", "z1234567@ad.unsw.edu.au", "Lyz1234567", 1
        )

        # Define user login data
        login_data = {"email": "z1234567@ad.unsw.edu.au", "password": "Lyz1234567"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        course = add_dummy_course_to_db(
            "COMP9900", "Capstone Project", "School of Computer Science and Engineering"
        )

        # bind academic and course
        assign_course_to_academic(course.ID, "1234567")
        newInfo = {
            "name": "cs",
            "code": "COMP9900",
            "year": "2022",
            "term": "T2",
            "description": "cse",
            "skills": "c",
            "topics": "12345",
        }
        # get course of academic
        response = client.put(
            f"/courses/{course.courseCode}/{course.yearDate}/{course.term}",
            headers=headers,
            json=newInfo,
        )

        assert response.status_code == 400
        assert response.get_json()["error"] == "Fields miss, please check."

        # clean up
        delete_courseEnrolment(course.ID)
        delete_course("COMP9900")
        delete_user(zID="1234567")
