'''
This file contains all the APIs and functions relating to user profile
and login.
'''

import string
import sys
import os
import hashlib
import random

current_directory = os.getcwd()
# Get the parent directory
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)
import json
from flask_mail import Mail, Message
from flask import Blueprint, request, jsonify, current_app, session
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

try:
    from auth import is_strong_password, is_valid_email
except ImportError:
    from .auth import is_strong_password, is_valid_email
try:
    from models import (
        db,
        User,
        UserCode,
        Course,
        CourseEnrolment,
        Project,
        Group,
        GroupMember,
    )
except ImportError:
    from .models import (
        db,
        User,
        UserCode,
        Course,
        CourseEnrolment,
        Project,
        Group,
        GroupMember,
    )
from recommendations.recommend_students import get_reccomended_students
from recommendations.recommend_courses import get_recommended_courses

try:
    from webscraping.transcript_scrape import scrape_pdf_from_base64
except ImportError:
    from ..webscraping.transcript_scrape import scrape_pdf_from_base64

try:
    from webscraping.scrape_single_course import get_single_course_information
except ImportError:
    from ..webscraping.scrape_single_course import get_single_course_information

try:
    from webscraping.pdf_scraping import *
except ImportError:
    from ..webscraping.pdf_scraping import *

try:
    from recommendations.similar_words import *
except ImportError:
    from ..recommendations.similar_words import *

try:
    from course import addCourseEnrolment
except ImportError:
    from app.course import addCourseEnrolment


user_profile = Blueprint("profile", __name__)
mail = Mail(current_app)



def add_user_to_db(zID, firstname, lastname, email, password):
    """
    Adds a new user to the database.

    Parameters:
    - z_id (str): The zID of the user.
    - first_name (str): The first name of the user.
    - last_name (str): The last name of the user.
    - email (str): The email address of the user.
    - password (str): The user's password.

    Returns:
    User or None: The newly created User object if successful, or None if an error occurs.

    """
    try:
        user_data = {
            "class": {
                "student": {
                    "major": "null",
                    "program": "null",
                    "transcript": "null",
                    "skills": {},
                    "knowledge": {},
                    "jobExperience": {},
                }
            }
        }

        # Serialize the JSON object to a string
        metadata = json.dumps(user_data, indent=2)

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Create a new user and add it to the database
        new_user = User(
            zID=zID,
            firstname=firstname,
            lastname=lastname,
            email=email,
            enPassword=hashed_password,
            metadataJson=metadata,  # Store user_type in metadata column as JSON string
            verified=0,
            privacy=0,
        )
        db.session.add(new_user)
        db.session.commit()

        return new_user

    except Exception as e:
        print(f"Error adding user to the database: {str(e)}")
        db.session.rollback()
        return None


def add_course_to_db(course_info):
    """
    Creates a new course object and adds it to the database.

    Parameters:
    - course_info (dict): A dictionary containing information about the course.
      It should have the following keys:
        - "course": Course code (str)
        - "course_name": Course name (str)
        - "course_description": Course description (str)
        - "course_skills": List of skills associated with the course (list of str)
        - "course_knowledge": List of knowledge areas associated with the course (list of str)
        - "course_topics": List of topics covered in the course (list of str)
        - "course_year": Year in which the course is offered (int)
        - "course_term": Term in which the course is offered (str)
        - "course_scraped": Revision or scraping information (str)
        - "course_school": School or department offering the course (str)

    Returns:
    Course: The newly created Course object with the provided information.
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


def update_new_role_user(userType, user):
    """
    Updates the role-specific metadata for a user based on the specified user type.

    Parameters:
    - user_type (str): The type of user role to assign ("student", "admin" or 'academic" type).
    - user (User): The User object to update.

    Returns:
    User: The updated User object with role-specific metadata.
    """
    metadata_JSON = user.metadataJson
    json_data = json.loads(metadata_JSON)

    if userType == "student":
        user_data = {
            "student": {
                "major": "NULL",
                "program": "NULL",
                "transcript": "NULL",
                "skills": {},
                "knowledge": {},
                "jobExperience": {},
            }
        }
    elif userType == "admin":
        user_data = {"admin": {}}
    else:
        user_data = {
            "academic": {
                "type": userType,
                "school": "NULL",
                "skills": {},
                "knowledge": {},
            }
        }

    json_data["class"].update(user_data)
    user.metadataJson = json.dumps(json_data)
    db.session.commit()

    return user


def create_unverified_user(zID, userType):
    '''
    Creates a new unverified user with the specified user type.

    Parameters:
    - zID (str): The zID of the user.
    - userType (str): The type of user to create ("student", "admin", or "academic" type).

    The created user is marked as unverified.
    '''
    if userType == "student":
        user_data = {
            "class": {
                "student": {
                    "major": "NULL",
                    "program": "NULL",
                    "transcript": "NULL",
                    "skills": {},
                    "knowledge": {},
                    "jobExperience": {},
                }
            }
        }
    elif userType == "admin":
        user_data = {
            "class": {
                "admin": {},
                "academic": {
                    "type": userType,
                    "school": "NULL",
                    "skills": {},
                    "knowledge": {},
                },
                "student": {
                    "major": "NULL",
                    "program": "NULL",
                    "transcript": "NULL",
                    "skills": {},
                    "knowledge": {},
                    "jobExperience": {},
                },
            }
        }
    else:
        user_data = {
            "class": {
                "academic": {
                    "type": userType,
                    "school": "NULL",
                    "skills": {},
                    "knowledge": {},
                },
                "student": {
                    "major": "NULL",
                    "program": "NULL",
                    "transcript": "NULL",
                    "skills": {},
                    "knowledge": {},
                    "jobExperience": {},
                },
            }
        }

    metadata = json.dumps(user_data)
    new_user = User(
        zID=zID,
        metadataJson=metadata,  # Store user_type in metadata column as JSON string
        verified=0,
    )
    db.session.add(new_user)
    db.session.commit()


def add_remaining_info(z_ID, firstname, lastname, email, password):
    '''
    Adds remaining information (firstname, lastname, email, and password) to an existing user.

    Parameters:
    - z_ID (str): The zID of the existing user.
    - firstname (str): The first name to update for the user.
    - lastname (str): The last name to update for the user.
    - email (str): The email address to update for the user.
    - password (str): The password to update for the user.

    Returns:
    User or None: The updated User object if successful, or None if the user with the
    specified zID is not found.
    '''
    user = User.query.filter_by(zID=z_ID).first()
    user.firstname = firstname
    user.lastname = lastname
    user.email = email
    user.enPassword = hashlib.sha256(password.encode()).hexdigest()
    db.session.commit()
    return user


def get_highest_permissions_email(email):
    '''
        Retrieves the highest-level user role associated with the given email.

        Parameters:
        - email (str): The email address of the user.

        Returns:
        str: The highest-level user role ("admin", "academic", or "student") associated
        with the provided email.
    '''
    user = User.query.filter_by(email=email).first()
    metadata_JSON = user.metadataJson
    json_data = json.loads(metadata_JSON)
    user_roles = list(json_data["class"].keys())

    order = {"admin": 1, "academic": 2, "student": 3}
    sorted_list = sorted(user_roles, key=lambda x: order.get(x, float("inf")))
    return sorted_list[0]


def get_highest_permissions_zID(zID):
    '''
        Retrieves the highest-level user role associated with the given zID.

        Parameters:
        - zID (int): The zID of the user.

        Returns:
        str: The highest-level user role ("admin", "academic", or "student") associated
        with the provided zID.
    '''
    user = User.query.filter_by(zID=zID).first()
    metadata_JSON = user.metadataJson
    json_data = json.loads(metadata_JSON)
    user_roles = list(json_data["class"].keys())

    order = {"admin": 1, "academic": 2, "student": 3}
    sorted_list = sorted(user_roles, key=lambda x: order.get(x, float("inf")))
    return sorted_list[0]


def update_verification(zID):
    """
    Updates the verification status of a user to 'verified'.

    Parameters:
    - zID (str): The zID of the user.

    Returns:
    User: The updated User object with the verification status set to 'verified'.
    """
    user = User.query.filter_by(zID=zID).first()
    user.verified = 1
    db.session.commit()
    return user


def code_generator():
    """
    Generates a random 5-character alphanumeric code.

    Returns:
    str: A randomly generated alphanumeric code.
    """
    return "".join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(5)
    )


def user_code_insertion(zID, code):
    """
    Inserts a user code into the database.

    Parameters:
    - zID (str): The zID of the user.
    - code (str): The code sent to the user's email.

    Note:
    - This function adds a new entry to the UserCode table in the database.
    """
    new_user_code = UserCode(user=zID, code=code)
    db.session.add(new_user_code)
    db.session.commit()


def user_code_deletion(zID, code):
    '''
    Deletes a user code from the database.

    Parameters:
    - zID (str): The zID of the user.
    - code (str): The code to be removed from the user's records.
    '''
    UserCode.query.filter_by(user=zID, code=code).delete()
    db.session.commit()


def publicProfileDisplay(zID):
    """
    Retrieves public information for a user based on their zID.

    Parameters:
    - zID (str): The zID of the user.

    Returns:
    JSON: A JSON response containing public information about the user, including zID,
        first name,last name, headline, summary, image URL, and privacy status.
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


def top_items(data):
    '''
    Normalizes and extracts the top 20 items from a dictionary.

    Parameters:
    - data (dict): A dictionary containing items and their corresponding scores.

    Returns:
    dict: A normalized dictionary containing the top 20 items and an 'other' category.
    '''
    # Sort the dictionary by values in descending order
    sorted_data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))

    # Get the top N items
    top_n = dict(list(sorted_data.items())[:19])

    # Calculate the 'other' score by summing the rest
    other_score = sum(list(sorted_data.values())[19:])

    # Add the 'other' category to the result
    top_n["other"] = other_score

    total = sum(top_n.values())

    if total == 0:
        return data

    # Calculate the scaling factor to normalize to 100
    scaling_factor = 100 / total

    # Normalize the values to be out of 100
    normalized_top_n = {
        key: int(value * scaling_factor) for key, value in top_n.items()
    }
    return normalized_top_n


def normalize_skills_knowledge(data):
    '''
    Normalizes a dictionary of skills or knowledge values to be percentages out of 100.

    Parameters:
    - data (dict): A dictionary containing skills or knowledge with their corresponding values.

    Returns:
    dict: A normalized dictionary with values scaled to be percentages out of 100.
    '''
    # Calculate the sum of the original values
    total = sum(data.values())

    if total == 0:
        return data

    # Calculate the scaling factor to normalize to 100
    scaling_factor = 100 / total

    # Normalize the values to be out of 100
    normalized_data = {key: int(value * scaling_factor) for key, value in data.items()}
    return normalized_data


def getProfileSkills(zID, role):
    '''
    Retrieves and returns the skills associated with a user's profile.

    Parameters:
    - zID (str): The zID of the user.
    - role (str): The user's role ("student", "admin", or "academic" type).

    Returns:
    JSON: A JSON response containing the user's profile skills, normalized and sorted.
    '''
    user = User.query.filter_by(zID=zID).first()
    if user:
        metaData = json.loads(user.metadataJson)
        try:
            skills = top_items(
                normalize_skills_knowledge(metaData["class"][role]["skills"])
            )
        except:
            skills = top_items(metaData["class"][role]["skills"])
        return jsonify({"skills": skills}), 200

    else:
        return jsonify({"error": "Invalid User"}), 400
    # get user metadata and converts the json to a dictionary


def getProfileKnowledge(zID, role):
    '''
    Retrieves and returns the knowledge associated with a user's profile.

    Parameters:
    - zID (str): The zID of the user.
    - role (str): The user's role ("student", "admin", or "academic" type).

    Returns:
    JSON: A JSON response containing the user's profile knowledge, normalized and sorted.
    '''
    user = User.query.filter_by(zID=zID).first()
    if user:
        metaData = json.loads(user.metadataJson)
        knowledge = metaData["class"][role]["knowledge"]
        knowledge = normalize_skills_knowledge(knowledge)
        replace_words = get_replaceable_words(knowledge)
        cleaned_knowledge = replace_similar_words_in_dict(knowledge, replace_words)
        try:
            cleaned_knowledge = normalize_skills_knowledge(cleaned_knowledge)
        except:
            pass
        cleaned_knowledge = top_items(cleaned_knowledge)
        return jsonify({"knowledge": cleaned_knowledge}), 200
    else:
        return jsonify({"error": "Invalid User"}), 400


def getRecommendedStudents(zID):
    '''
    Retrieves and returns a list of recommended students based on skills and knowledge matching.

    Parameters:
    - zID (str): The zID of the user.

    Returns:
    JSON: A JSON response containing information about recommended students, including zID,
          first name, last name, headline, skills, knowledge, and image URL.
    '''
    all_students = {}
    users = User.query.all()
    for user in users:
        metaData = json.loads(user.metadataJson)
        if "student" in list(metaData["class"].keys()):
            user_knowledge = metaData["class"]["student"]["knowledge"]
            user_skills = metaData["class"]["student"]["skills"]
            user_skills_and_knowledge = {
                term: (user_skills.get(term, 0) + user_knowledge.get(term, 0))
                for term in set(user_skills) | set(user_knowledge)
            }
            all_students[user.zID] = user_skills_and_knowledge
    recommended_students = get_reccomended_students(all_students, zID)

    recommended_students_info = []

    for student in recommended_students:
        user = User.query.filter_by(zID=student).first()
        metaData = json.loads(user.metadataJson)
        user_knowledge = metaData["class"]["student"]["knowledge"]
        user_knowledge_list = list(user_knowledge.keys())
        user_skills = metaData["class"]["student"]["skills"]
        user_skills_list = list(user_skills.keys())

        user_info = {
            "zID": user.zID,
            "firstName": user.firstname,
            "lastName": user.lastname,
            "headline": user.headline,
            "skills": user_skills_list,
            "knowledge": user_knowledge_list,
            "imageURL": user.imageURL,
        }

        recommended_students_info.append(user_info)

    return {"students": recommended_students_info}, 200


def updateCourseTranscriptPDF(zID, transcript):
    '''
    Updates a user's course enrolment based on information extracted from a transcript PDF.

    Parameters:
    - zID (str): The zID of the user.
    - transcript (str): The transcript PDF encoded in base64 format.

    Returns:
    JSON: An empty JSON response indicating the success of the course enrolment update.
    '''
    course_list = scrape_pdf_from_base64(transcript)
    for course in course_list:
        try:
            courseCode = course[0]
            yearDate = course[1]
            term = course[2][0] + course[2][-1]
            courseInfo = Course.query.filter_by(
                courseCode=courseCode, yearDate=yearDate, term=term
            ).first()
            addCourseEnrolment(zID, courseInfo.ID, "student")
        except:
            pass
    return jsonify({}), 200


@user_profile.route("/register", methods=["POST"])
def register():
    '''
    Registers a new user with the provided information.

    Request:
    - Method: POST
    - Endpoint: /register
    - JSON Body: {"zId": "1234567", "firstName": "John", "lastName": "Doe",
                  "email": "john.doe@example.com", "password": "Securepasswor12d"}

    Response:
    - Success: {"message": "User registration successful"}
    - Error: {"error": "User registration failed."}
    '''
    # Get user data from the request JSON body
    data = request.get_json()

    # Ensure all required fields are present
    required_fields = ["zId", "firstName", "lastName", "email", "password"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Please provide all required fields"}), 400

    z_id = data["zId"][1:]
    firstname = data["firstName"]
    lastname = data["lastName"]
    email = data["email"]
    password = data["password"]

    # Check if the zID is already registered
    existing_user_id = User.query.filter_by(zID=z_id, verified=1).first()
    if existing_user_id:
        return (
            jsonify(
                {
                    "error": "User already exists. Please use a different zID or login to your existing account."
                }
            ),
            400,
        )

    # Check if the email is already registered
    existing_user = User.query.filter_by(email=email, verified=1).first()
    if existing_user:
        return (
            jsonify({"error": "Email already exists. Please use a different email."}),
            400,
        )

    # Check if they're an admin or academic type that is pre-signed up
    pre_determined = User.query.filter_by(zID=z_id).first()

    if pre_determined:
        new_user = add_remaining_info(z_id, firstname, lastname, email, password)
    else:
        # Add the user (including student details) to the database
        new_user = add_user_to_db(z_id, firstname, lastname, email, password)

    if new_user:
        # Sends email with code verification
        code = code_generator()

        # msg = Message('Hello', sender = 'PROJECT15UNSW@outlook.com', recipients = [f'z{z_id}@ad.unsw.edu.au'])
        # msg.html = f'<i>Thanks for signing up!</i>. Please click this link to eneter your account <a href= "http://localhost:3000/verify-account/{data["zId"]}/{code}" >Click here!</a>'
        # mail.send(msg)

        user_code_insertion(z_id, code)
        return jsonify({}), 200
    else:
        return jsonify({"error": "User registration failed."}), 400


@user_profile.route("/verifyCode", methods=["POST"])
def verifyCode():
    '''
    Verifies a user's registration code and generates an access token upon successful verification.

    Request:
    - Method: POST
    - Endpoint: /verify_code
    - JSON Body: {"zId": "1234567", "code": "verification_code"}

    Response:
    - Success: {"token": "access_token", "userType": "student"}
    - Error: {"error": "There was some error."}
    '''
    data = request.get_json()
    zID = data["zId"][1:]
    code = data["code"]

    # Find user-code pair
    user_code_pair = UserCode.query.filter_by(user=zID, code=code).first()

    # Create a JWT token for the new user
    access_token = create_access_token(identity=zID)

    # Get the highest permissions of the user
    user_role = get_highest_permissions_zID(zID)

    if user_code_pair:
        update_verification(zID)
        user_code_deletion(zID, code)
        return jsonify({"token": access_token, "userType": user_role}), 200

    return jsonify({"error": "There was some error"}), 400


@user_profile.route("/login", methods=["POST"])
def login():
    '''
    Logs in a user by validating the provided email and password.

    Request:
    - Method: POST
    - Endpoint: /login
    - JSON Body: {"email": "user@example.com", "password": "securepassword"}

    Response:
    - Success: {"token": "access_token", "userType": "student"}
    - Error: {"error": "Invalid email or password"} or
             {"error": "User unverified, please sign up again with the same details"}
    '''
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    # Find the user by email
    user = User.query.filter_by(email=email).first()

    hash_password = hashlib.sha256(password.encode()).hexdigest()

    if user:
        if user.verified == 0:
            return (
                jsonify(
                    {
                        "error": "User unverified, please sign up again with the same details"
                    }
                ),
                401,
            )
        if user.enPassword == hash_password:
            # Generate a JWT token
            access_token = create_access_token(identity=user.zID)

            # Get the highest permissions of the user
            user_role = get_highest_permissions_email(email)
            # Return the token along with a success message
            return jsonify({"token": access_token, "userType": user_role}), 200
        # If authentication fails, return an error response
    return jsonify({"error": "Invalid email or password"}), 401


@user_profile.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    '''
    Logs out the authenticated user, clearing the session data.

    Request:
    - Method: POST
    - Endpoint: /logout

    Response:
    - Success: {"message": "Logout successful"}
    '''
    # Clear the user's session data
    session.clear()
    return jsonify({"message": "Logout successful"}), 200


@user_profile.route("/admin/user/edit/usertype", methods=["PUT"])
@jwt_required()
def giveUserRole():
    '''
    Assigns or updates the user role for a specified user.

    Request:
    - Method: PUT
    - Endpoint: /admin/user/edit/usertype
    - JSON Body: {"zId": "1234567", "userType": "admin"}

    Response:
    - Success: {"message": "Role assigned"}
    - Error: {"error": "Invalid input"} (if the specified role already exists for the user)
    '''
    data = request.get_json()
    zID = data["zId"][1:]
    userType = data["userType"]
    # Find the user by email
    user = User.query.filter_by(zID=zID).first()

    if user:
        metadata_JSON = user.metadataJson
        json_data = json.loads(metadata_JSON)
        user_roles = list(json_data["class"].keys())
        if userType in user_roles:
            return jsonify({"error": "Invalid input"}), 400
        else:
            update_new_role_user(userType, user)
    else:
        create_unverified_user(zID, userType)

    return jsonify({"message": "Role assigned"}), 200


@user_profile.route("/user/profile", methods=["GET"])
@jwt_required()  # decorator verifies the JWT token
def getProfile():
    '''
    Retrieves the profile information of a user.

    GET /user/profile

    Parameters:
    - Requires a valid JWT token.
    - URL Parameter: zID (optional; if not provided, uses the identity from the token)

    Response:
    - JSON containing user profile information, including zID, name, email, headline,
      summary, imageURL, privacy status, and user type.
    '''
    current_user_id = request.args.get("zID")
    if current_user_id == None:
        current_user_id = get_jwt_identity()

    # Find the user
    user = User.query.filter_by(zID=int(current_user_id)).first()

    if not user:
        return jsonify({"error": "User not found."}), 404

    # get user metadata and converts the json to a dictionary
    metaData = json.loads(user.metadataJson)
    # get user role
    role = list(metaData["class"].keys())

    if "admin" in role:
        role = "admin"
    elif "academic" in role:
        role = "academic"
    else:
        role = "student"

    if user.privacy == 1:
        privacy = True
    else:
        privacy = False

    data = {
        "zID": user.zID,
        "firstName": user.firstname,
        "lastName": user.lastname,
        "email": user.email,
        "headline": user.headline,
        "summary": user.summary,
        "imageURL": user.imageURL,
        "private": privacy,
        "userType": role,
    }

    return jsonify(data), 200


@user_profile.route("/user/profile/setaccountpreference", methods=["PUT"])
@jwt_required()  # decorator verifies the JWT token
def setPreference():
    '''
    Retrieves the profile information of the authenticated user or a specified user.

    Request:
    - Method: GET
    - Endpoint: /user/profile
    - Query Parameter (Optional): ?zID=1234567 (to specify a user by zID)

    Response:
    - Success: JSON containing user profile information, including zID, first name, last name,
        email, headline, summary, image URL, privacy status, and user type.
    - Error: {"error": "User not found."} (if the specified or authenticated user is not found)

    '''
    # get data from request body
    data = request.get_json()
    # print(data)
    zID = get_jwt_identity()
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    headline = data.get("headline")
    summary = data.get("summary")
    imageURL = data.get("imageURL")

    # Find the user
    user = User.query.filter_by(zID=zID).first()

    if not user:
        return jsonify({"error": "User not found."}), 404

    # first name (1, 50) length, last name (1, 50) length, Headline (3, 20) length and all alpha, summary (1, 500) length
    # if not (1 <= len(firstName) <= 50) or not (1 <= len(lastName) <= 50) or not (3 <= len(headline) <= 20) or not (1 <= len(summary) <= 50):
    #     return jsonify({
    #         "error": "Invalid Input"
    #     }), 400

    if not (1 <= len(firstName) <= 50) or not (1 <= len(lastName) <= 50):
        return jsonify({"error": "Invalid Input- First Name or Last Name"}), 400

    if not (len(headline) <= 40):
        return jsonify({"error": "Invalid Input - Headline too long!"}), 400

    if not (len(summary) <= 100):
        return jsonify({"error": "Invalid Input - Summary too long!"}), 400

    # change name
    user.firstname = firstName
    user.lastname = lastName
    user.headline = headline
    user.summary = summary
    user.imageURL = imageURL

    # commit changes
    db.session.commit()

    return jsonify({"message": "Edit successful"})


@user_profile.route("/user/profile/edit-intro", methods=["PUT"])
@jwt_required()  # decorator verifies the JWT token
def editIntro():
    '''
    Edits the user's profile introduction.

    Request:
    - Requires a valid JWT token.
    - Updates the user's first name, last name, headline, summary, and image URL.

    Response:
    - {"message": "Edit successful"} on success.
    - {"error": "User not found."} if the specified user is not found.
    - {"error": "Invalid Input- First Name or Last Name"} if input constraints are not met.
    - {"error": "Invalid Input - Headline too long!"} if the headline length exceeds 40 characters.
    - {"error": "Invalid Input - Summary too long!"} if the summary length exceeds 100 characters.
    '''
    # get data from request body
    data = request.get_json()
    # print(data)
    zID = data.get("zID")
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    headline = data.get("headline")
    summary = data.get("summary")
    imageURL = data.get("imageURL")

    # Find the user
    user = User.query.filter_by(zID=zID).first()

    if not user:
        return jsonify({"error": "User not found."}), 404

    # first name (1, 50) length, last name (1, 50) length, Headline (3, 20) length and all alpha, summary (1, 500) length
    # if not (1 <= len(firstName) <= 50) or not (1 <= len(lastName) <= 50) or not (3 <= len(headline) <= 20) or not (1 <= len(summary) <= 50):
    #     return jsonify({
    #         "error": "Invalid Input"
    #     }), 400

    if not (1 <= len(firstName) <= 50) or not (1 <= len(lastName) <= 50):
        return jsonify({"error": "Invalid Input- First Name or Last Name"}), 400

    if not (len(headline) <= 40):
        return jsonify({"error": "Invalid Input - Headline too long!"}), 400

    if not (len(summary) <= 100):
        return jsonify({"error": "Invalid Input - Summary too long!"}), 400

    # change name
    user.firstname = firstName
    user.lastname = lastName
    user.headline = headline
    user.summary = summary
    user.imageURL = imageURL

    # commit changes
    db.session.commit()

    return jsonify({"message": "Edit successful"})


@user_profile.route("/profile/edit/privacy", methods=["PUT"])
@jwt_required()  # decorator verifies the JWT token
def setPrivacy():
    '''
    Sets the privacy status of the current user.

    PUT /profile/edit/privacy

    Parameters:
    - Requires a valid JWT token.
    - JSON Body:
        - zID: The zID of the user whose privacy is being edited.
        - private: Boolean indicating the desired privacy status.

    Response:
    - JSON indicating the success of the privacy status update.
    '''
    current_user_id = get_jwt_identity()

    # Find the user
    user = User.query.filter_by(zID=current_user_id).first()
    # print(user)

    if not user:
        return jsonify({"error": "User not found."}), 404

    # get data from request body
    data = request.get_json()
    zID = data["zID"]
    privacy = data["private"]
    user = User.query.filter_by(zID=zID).first()

    if privacy:
        user.privacy = 1
    else:
        user.privacy = 0

    # commit changes
    db.session.commit()

    return jsonify({"message": "Edit successful"})


@user_profile.route("/auth/setemail", methods=["PUT"])
@jwt_required()  # decorator verifies the JWT token
def setEmail():
    '''
    Sets the email of the current user.

    PUT /auth/setemail

    Parameters:
    - Requires a valid JWT token.
    - JSON Body:
        - email: The new email address to set.

    Response:
    - JSON indicating the success of the email update.
    '''
    # get token from request header
    current_user_id = get_jwt_identity()

    # Find the user
    user = User.query.filter_by(zID=current_user_id).first()

    # get data from request body
    data = request.get_json()
    targetEmail = data.get("email")

    # validate input length
    if not (1 <= len(targetEmail) <= 255) or not is_valid_email(targetEmail):
        return jsonify({"error": "Invalid Input"}), 400

    # check if email is already in use
    if User.query.filter_by(email=targetEmail).first():
        return jsonify({"error": "Invalid Input"}), 400

    # update user
    user.email = targetEmail
    # commit changes
    db.session.commit()

    # regen token
    # token = jwt.encode({"email": targetEmail}, current_app.secret_key, algorithm="HS256")
    # token = "123"
    return jsonify({"message": "Set successful"})


@user_profile.route("/auth/passwordreset", methods=["PUT"])
@jwt_required()  # decorator verifies the JWT token
def passwordReset():
    '''
    Resets the password for the authenticated user.

    Request:
    - Requires a valid JWT token.
    - JSON Body: {"currentPassword": "old_password", "newPassword": "new_secure_password"}

    Response:
    - {"message": "Reset successful"} on success.
    - {"error": "Invalid Input"} if the current password is incorrect or the new password is weak.
    '''
    # get token from request header
    current_user_id = get_jwt_identity()

    # find user
    user = User.query.filter_by(zID=current_user_id).first()

    data = request.get_json()
    currentPassword = data.get("currentPassword")
    newPassword = data.get("newPassword")
    hashed_password_current = hashlib.sha256(currentPassword.encode()).hexdigest()
    hashed_password_new = hashlib.sha256(newPassword.encode()).hexdigest()
    # validate password
    if hashed_password_current != user.enPassword:
        return jsonify({"error": "Invalid Input"}), 400

    # validate password
    if not is_strong_password(newPassword):
        return jsonify({"error": "Invalid Input"}), 400

    # update user
    user.enPassword = hashed_password_new

    # commit changes
    db.session.commit()

    return jsonify({"message": "Reset successful"})


@user_profile.route("/admin/auth/passwordreset", methods=["PUT"])
@jwt_required()  # decorator verifies the JWT token
def adminPasswordReset():
    '''
    Resets the password for a user by an administrator.

    Request:
    - Requires a valid JWT token with administrator privileges.
    - JSON Body: {"zID": "1234567", "newPassword": "new_secure_password"}

    Response:
    - {"message": "Reset successful"} on success.
    - {"error": "User not found."} if the specified user is not found.
    '''
    data = request.get_json()

    # find user
    zID = data.get("zID")
    user = User.query.filter_by(zID=zID).first()

    newPassword = data.get("newPassword")
    hashed_password_new = hashlib.sha256(newPassword.encode()).hexdigest()

    # update user
    user.enPassword = hashed_password_new

    # commit changes
    db.session.commit()

    return jsonify({"message": "Reset successful"})


def getStudentProjects(zID):
    '''
    Retrieves a list of projects associated with a student.

    Parameters:
    - zID: Student's identification number (zID).

    Response:
    - JSON containing a list of projects with project ID, name, client, and thumbnail.
    '''
    studentProjectsList = (
        Project.query.join(Group).join(GroupMember).filter_by(student=zID)
    )
    projectListDict = []
    for project in studentProjectsList:
        ProjectInfoDict = {
            "id": project.ID,
            "projectName": project.projectName,
            "client": project.client,
            "thumbnail": project.thumbnail,
        }
        projectListDict.append(ProjectInfoDict)
    return jsonify({"projects": projectListDict})


@user_profile.route("/user/profile/student", methods=["GET"])
@jwt_required()
def getUserStudentPublicProfile():
    '''
    Retrieves the public profile of a student.

    Parameters:
    - Requires a valid JWT token.
    - URL Parameter: zID

    Response:
    - Public profile information in JSON format.
    '''
    zID = int(request.args.get("zID"))
    return publicProfileDisplay(zID)


@user_profile.route("/user/profile/academic", methods=["GET"])
@jwt_required()
def getUserAcademicPublicProfile():
    '''
    Retrieves the public profile of an academic user.

    Parameters:
    - Requires a valid JWT token.
    - URL Parameter: zID (academic user's identification number)

    Response:
    - Public profile information in JSON format.
    '''
    zID = int(request.args.get("zID"))
    return publicProfileDisplay(zID)


@user_profile.route("/student/profile/skills", methods=["GET"])
@jwt_required()
def getStudentSkills():
    '''
    Retrieves the skills of a student.

    Parameters:
    - Requires a valid JWT token.
    - URL Parameter: zID

    Response:
    - JSON containing the student's skills.
    '''
    zID = int(request.args.get("zID"))
    return getProfileSkills(zID, "student")


@user_profile.route("/student/profile/knowledge", methods=["GET"])
@jwt_required()
def getStudentKnowledge():
    '''
    Retrieves the knowledge of a student.

    Parameters:
    - Requires a valid JWT token.
    - URL Parameter: zID

    Response:
    - JSON containing the student's knowledge.
    '''
    zID = int(request.args.get("zID"))
    return getProfileKnowledge(zID, "student")


@user_profile.route("/academic/profile/skills", methods=["GET"])
@jwt_required()
def getAcademicSkills():
    '''
    Retrieves the skills of an academic user.

    Parameters:
    - Requires a valid JWT token.
    - URL Parameter: zID (academic user's identification number)

    Response:
    - JSON containing the academic user's skills.
    '''
    zID = int(request.args.get("zID"))
    return getProfileSkills(zID, "academic")


@user_profile.route("/academic/profile/knowledge", methods=["GET"])
@jwt_required()
def getAcademicKnowledge():
    '''
    Retrieves the knowledge of an academic user.

    Parameters:
    - Requires a valid JWT token.
    - URL Parameter: zID (academic user's identification number)

    Response:
    - JSON containing the academic user's knowledge.
    '''
    zID = int(request.args.get("zID"))
    return getProfileKnowledge(zID, "academic")


@user_profile.route("/user/profile/student/transcript", methods=["POST"])
@jwt_required()
def extractTranscriptPDF():
    '''
    Extracts and updates the transcript for a student.

    Parameters:
    - Requires a valid JWT token.
    - JSON Body: {"zID": "1234567", "transcript": "base64_encoded_pdf_content"}

    Response:
    - JSON indicating the success or failure of the transcript extraction.
    '''
    data = request.get_json()
    print(data)
    transcript = data["transcript"]
    zID = data["zID"]
    response = updateCourseTranscriptPDF(zID, transcript)
    return response


@user_profile.route("/user/recommended-users", methods=["GET"])
@jwt_required()
def recommendedUsers():
    '''
    Retrieves a list of recommended users for a student.

    Parameters:
    - Requires a valid JWT token.
    - URL Parameter: zID

    Response:
    - JSON containing information about recommended users.
    '''
    zID = int(request.args.get("zID"))
    response = getRecommendedStudents(zID)
    return response


@user_profile.route("/student/projects", methods=["GET"])
@jwt_required()
def studentProjects():
    '''
    Retrieves a list of projects associated with a student.

    Parameters:
    - Requires a valid JWT token.
    - URL Parameter: zID

    Response:
    - JSON containing a list of projects with project ID, name, client, and thumbnail.
    '''
    zID = int(request.args.get("zID"))

    # Find the user
    response = getStudentProjects(zID)
    return response, 200
