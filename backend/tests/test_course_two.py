import ast
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
import base64


@pytest.fixture
def client():
    # Create and return a test client for the Flask app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def add_dummy_user_to_db(
    firstname, lastname, zID, email, password, verified, user_data
):
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


def add_dummy_course_to_db(courseCode, courseName, school, yearDate="2023", term="T3"):
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
        course=courseID, user=academicZID, courseRole="academic"
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
def test_course_url_upload_wrong_url(client):
    """
    Test uploading a course outline URL with an invalid format.

    Args:
    - client: Flask test client.

    """
    with app.app_context():  # Create an application context
        delete_user(zID="5255998")
        delete_user(zID="1234569")

        user_data = {"class": {"academic": {}}}
        # Add a dummy user to the database
        add_dummy_user_to_db(
            firstname="Sammi",
            lastname="AuYeung",
            zID="5255998",
            email="z5255998@ad.unsw.edu.au",
            password="1amSammi*",
            verified=1,
            user_data=user_data,
        )

        # Define user login data
        login_data = {"email": "z5255998@ad.unsw.edu.au", "password": "1amSammi*"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        url = "https://www.youtube.com/"

        response = client.put(f"/courses/url", headers=headers, json={"url": url})

        assert response.status_code == 400
        assert "Invalid UNSW course outline url" in response.get_json()["error"]

        delete_user(zID="5255998")
        delete_user(zID="1234569")


def test_recommended_courses(client):
    """
    Test retrieving recommended courses for a student based on their skills and knowledge.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        delete_user(zID="5255998")
        delete_user(zID="1234569")

        user_data = {
            "class": {
                "student": {
                    "major": "null",
                    "program": "null",
                    "transcript": "null",
                    "skills": {"essay writing": 70, "public speaking": 30},
                    "knowledge": {"c++": 50, "python": 25, "graphs": 25},
                    "jobExperience": {},
                }
            }
        }
        # Add a dummy user to the database
        add_dummy_user_to_db(
            firstname="Sammi",
            lastname="AuYeung",
            zID="5255998",
            email="z5255998@ad.unsw.edu.au",
            password="1amSammi*",
            verified=1,
            user_data=user_data,
        )

        # Define user login data
        login_data = {"email": "z5255998@ad.unsw.edu.au", "password": "1amSammi*"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        response = client.get(f"/courses/student", headers=headers)
        assert response.status_code == 200
        assert response.get_json()["courses"] == []

        delete_user(zID="5255998")
        delete_user(zID="1234569")


def test_recommended_courses_multiple(client):
    """
    Test retrieving recommended courses for a student with multiple preferences.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        delete_user(zID="5255998")
        delete_user(zID="1234569")

        user_data = {
            "class": {
                "student": {
                    "major": "null",
                    "program": "null",
                    "transcript": "null",
                    "skills": {"essay writing": 70, "public speaking": 30},
                    "knowledge": {"c++": 50, "python": 25, "graphs": 25},
                    "jobExperience": {},
                }
            }
        }
        # Add a dummy user to the database
        add_dummy_user_to_db(
            firstname="Sammi",
            lastname="AuYeung",
            zID="5255998",
            email="z5255998@ad.unsw.edu.au",
            password="1amSammi*",
            verified=1,
            user_data=user_data,
        )

        # Define user login data
        login_data = {"email": "z5255998@ad.unsw.edu.au", "password": "1amSammi*"}

        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        acamdeic_data = {"class": {"academic": {}}}
        # Add a dummy user to the database
        add_dummy_user_to_db(
            firstname="Someone",
            lastname="Random",
            zID="5255999",
            email="z5255999@ad.unsw.edu.au",
            password="1amSammi*",
            verified=1,
            user_data=acamdeic_data,
        )

        # Define user login data
        login_data_two = {"email": "z5255999@ad.unsw.edu.au", "password": "1amSammi*"}

        # Add the same user to DB using register
        response_academic = client.post("/login", json=login_data_two)

        # Get headers
        responseData_academic = response_academic.get_json()
        access_token_academic = responseData_academic.get("token")
        headers_academic = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token_academic}",
        }

        course_one = {
            "name": "Programming Fundamentals",
            "code": "COMP1511",
            "year": "2023",
            "term": "T3",
            "description": "None",
            "skills": {"essay writing": 100},
            "topics": ["Test Topics"],
            "knowledge": {"python": 100},
            "thumbnail": "None",
        }

        # Add the course to DB using set preference
        response = client.put(
            f"/courses/COMP1511/2023/3", headers=headers_academic, json=course_one
        )

        assert response.status_code == 200
        assert "Course created successfully." in response.get_json()["message"]

        course_two = {
            "name": "Random Course",
            "code": "COMP2511",
            "year": "2023",
            "term": "T3",
            "description": "None",
            "skills": {"building sandcastles": 100},
            "topics": ["Test Topics"],
            "knowledge": {"gaming": 100},
            "thumbnail": "None",
        }

        # Add the course to DB using set preference
        response = client.put(
            f"/courses/COMP1511/2023/3", headers=headers_academic, json=course_two
        )

        assert response.status_code == 200
        assert "Course created successfully." in response.get_json()["message"]

        response = client.get(f"/courses/student", headers=headers)
        assert response.status_code == 200
        courses = response.get_json()["courses"]

        assert len(courses) == 2

        assert courses[0]["name"] == "Programming Fundamentals"
        assert courses[1]["name"] == "Random Course"

        delete_course("COMP1511")
        delete_course("COMP2511")
        delete_user(zID="5255998")
        delete_user(zID="1234569")
