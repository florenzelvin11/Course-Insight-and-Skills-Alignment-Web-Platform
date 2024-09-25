import os
import sys

current_directory = os.getcwd()
# Get the parent directory
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

import hashlib
import json
import pytest
from app.app import app
from app.models import db, User, Project, Group, GroupMember


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


#####################
#       Tests       #
#####################


def test_returns_correct_recommended_students_single_student(client):
    """
    Test the retrieval of recommended single student for a single student based on their profile.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        delete_user(zID="5255998")
        delete_user(zID="1234569")

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

        response = client.get(f"/user/recommended-users?zID=5255998", headers=headers)

        assert response.status_code == 200

        content = response.get_json()["students"]

        count = 0

        for student in content:
            if student["zID"] == 5319978 or student["zID"] == 5255997:
                continue
            count += 1
        assert count == 0

        delete_user(zID="5255998")
        delete_user(zID="1234569")


def test_returns_correct_recommended_students_multiple_students(client):
    """
    Test the retrieval of recommended multiple students for a single student based on their profile.
    
    Args:
    - client: Flask test client.
    """
    with app.app_context():
        delete_user(zID="5255998")
        delete_user(zID="5255999")
        delete_user(zID="5255910")
        delete_user(zID="1234569")

        user_data = {
            "class": {
                "student": {
                    "major": "null",
                    "program": "null",
                    "transcript": "null",
                    "skills": {
                        "public speaking": 40,
                        "essay writing": 30,
                        "reciting": 30,
                    },
                    "knowledge": {"c++": 20, "python": 70, "graphs": 10},
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

        user_data_two = {
            "class": {
                "student": {
                    "major": "null",
                    "program": "null",
                    "transcript": "null",
                    "skills": {"speaking": 40, "writing": 30, "coding": 30},
                    "knowledge": {"c++": 20, "python": 70, "graphs": 10},
                    "jobExperience": {},
                }
            }
        }
        # Add a dummy user to the database
        add_dummy_user_to_db(
            firstname="Jane",
            lastname="Doe",
            zID="5255999",
            email="z5255999@ad.unsw.edu.au",
            password="1amJane*",
            verified=1,
            user_data=user_data_two,
        )

        user_data_three = {
            "class": {
                "student": {
                    "major": "null",
                    "program": "null",
                    "transcript": "null",
                    "skills": {"typing": 40, "communication": 30, "coding": 30},
                    "knowledge": {"SQL": 20, "javascript": 70, "R": 10},
                    "jobExperience": {},
                }
            }
        }
        # Add a dummy user to the database
        add_dummy_user_to_db(
            firstname="John",
            lastname="Doe",
            zID="5255910",
            email="z5255910@ad.unsw.edu.au",
            password="1amJohn*",
            verified=1,
            user_data=user_data_three,
        )

        response = client.get(f"/user/recommended-users?zID=5255998", headers=headers)

        assert response.status_code == 200

        content = response.get_json()["students"]

        count = 0
        other_students = []
        for student in content:
            if student["zID"] == 5319978 or student["zID"] == 5255997:
                continue
            count += 1
            other_students.append(student)

        assert count == 2

        assert other_students[0]["zID"] == 5255999
        assert other_students[1]["zID"] == 5255910

        delete_user(zID="5255998")
        delete_user(zID="5255999")
        delete_user(zID="5255910")
        delete_user(zID="1234569")
