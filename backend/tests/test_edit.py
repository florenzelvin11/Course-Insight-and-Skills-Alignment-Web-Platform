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
from app.models import db, User, UserCode


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


def get_usercode(zID):
    """
    Add a dummy project to the database.

    Parameters:
    - name (str): The name of the project.
    - client (str): The client associated with the project.
    - skills (str): Skills required for the project.
    - thumbnail (str): URL or path to the project's thumbnail.
    - scope (str): The scope or description of the project.
    - topics (str): Topics related to the project.
    - zid (str): The zID of the creator/owner of the project.

    Returns:
    - Project: The newly added project object.
    """
    # Find the user by their zID
    usercode = UserCode.query.filter_by(user=zID).first()
    if usercode:
        return usercode.code


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


#####################
#       Tests       #
#####################


def test_invalid_first_name(client):
    """
    Test updating user profile with an invalid first name.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        # Delete if user exist
        delete_user(zID="5338660")

        # Add user to DB
        add_dummy_user_to_db(
            "Evan", "Li", "5338660", "z5338660@ad.unsw.edu.au", "Lyz1234567", 1
        )

        # Define user login data
        login_data = {"email": "z5338660@ad.unsw.edu.au", "password": "Lyz1234567"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        # edit profile data
        edits = {
            "firstName": "",
            "lastName": "Li",
            "academicPosition": "student",
            "summary": "123",
        }

        # Add the same user to DB using set preference
        response = client.put(
            "/user/profile/setaccountpreference", headers=headers, json=edits
        )

        # Check if the registration is unsuccessful
        assert response.status_code == 400
        assert "Invalid Input- First Name or Last Name" in response.get_json()["error"]

        delete_user(zID="5338660")


def test_invalid_last_name(client):
    """
    Test updating user profile with an invalid last name.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        # Delete if user exist
        delete_user(zID="5338660")

        # Add user to DB
        add_dummy_user_to_db(
            "Evan", "Li", "5338660", "z5338660@ad.unsw.edu.au", "Lyz1234567", 1
        )

        # Define user login data
        login_data = {"email": "z5338660@ad.unsw.edu.au", "password": "Lyz1234567"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        # edit profile data
        edits = {
            "firstName": "Evan",
            "lastName": "",
            "academicPosition": "student",
            "summary": "123",
        }

        # Add the same user to DB using set preference
        response = client.put(
            "/user/profile/setaccountpreference", headers=headers, json=edits
        )

        # Check if the registration is unsuccessful
        assert response.status_code == 400
        assert "Invalid Input" in response.get_json()["error"]

        delete_user(zID="5338660")


def test_invalid_headline(client):
    """
    Test updating user profile with an invalid headline.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        # Delete if user exist
        delete_user(zID="5338660")

        # Add user to DB
        add_dummy_user_to_db(
            "Evan", "Li", "5338660", "z5338660@ad.unsw.edu.au", "Lyz1234567", 1
        )

        # Define user login data
        login_data = {"email": "z5338660@ad.unsw.edu.au", "password": "Lyz1234567"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        # edit profile data
        edits = {
            "firstName": "Evan",
            "lastName": "Li",
            "headline": "*" * 51,
            "summary": "123",
        }

        # Add the same user to DB using set preference
        response = client.put(
            "/user/profile/setaccountpreference", headers=headers, json=edits
        )

        # Check if the registration is unsuccessful
        assert response.status_code == 400
        assert "Invalid Input" in response.get_json()["error"]

        delete_user(zID="5338660")


def test_invalid_summary(client):
    """
    Test updating user profile with an invalid summary.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        # Delete if user exist
        delete_user(zID="5338660")

        # Add user to DB
        add_dummy_user_to_db(
            "Evan", "Li", "5338660", "z5338660@ad.unsw.edu.au", "Lyz1234567", 1
        )

        # Define user login data
        login_data = {"email": "z5338660@ad.unsw.edu.au", "password": "Lyz1234567"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        # edit profile data
        edits = {
            "firstName": "Evan",
            "lastName": "Li",
            "headline": "Computer Science Student",
            "summary": "*" * 1001,
        }

        # Add the same user to DB using set preference
        response = client.put(
            "/user/profile/setaccountpreference", headers=headers, json=edits
        )

        # Check if the registration is unsuccessful
        assert response.status_code == 400
        assert "Invalid Input" in response.get_json()["error"]

        delete_user(zID="5338660")


def test_successful_edit_profile(client):
    """
    Test successfully editing user profile.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        # Delete if user exist
        delete_user(zID="5338660")

        # Add user to DB
        add_dummy_user_to_db(
            "Evan", "Li", "5338660", "z5338660@ad.unsw.edu.au", "Lyz1234567", 1
        )

        # Define user login data
        login_data = {"email": "z5338660@ad.unsw.edu.au", "password": "Lyz1234567"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        # edit profile data
        edits = {
            "firstName": "Yanzhi",
            "lastName": "Lii",
            "headline": "Computer Science Student",
            "summary": "123abc",
        }

        # Add the same user to DB using set preference
        response = client.put(
            "/user/profile/setaccountpreference", headers=headers, json=edits
        )

        # Check if the registration is unsuccessful
        assert response.status_code == 200
        assert "Edit successful" in response.get_json()["message"]

        delete_user(zID="5338660")


def test_invalid_email(client):
    """
    Test invalid email input when updating user email.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        # Delete if user exist
        delete_user(zID="5338660")

        # Add user to DB
        add_dummy_user_to_db(
            "Evan", "Li", "5338660", "z5338660@ad.unsw.edu.au", "Lyz1234567", 1
        )

        # Define user login data
        login_data = {"email": "z5338660@ad.unsw.edu.au", "password": "Lyz1234567"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        # edit profile data
        email = {"email": "123"}

        # Add the same user to DB using set preference
        response = client.put("/auth/setemail", headers=headers, json=email)

        # Check if the registration is unsuccessful
        assert response.status_code == 400
        assert "Invalid Input" in response.get_json()["error"]

        delete_user(zID="5338660")


def test_existed_email(client):
    """
    Test updating user email to an already existing email.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        # Delete if user exist
        delete_user(zID="5338660")

        # Add user to DB
        add_dummy_user_to_db(
            "Evan", "Li", "5338660", "z5338660@ad.unsw.edu.au", "Lyz1234567", 1
        )

        # Define user login data
        login_data = {"email": "z5338660@ad.unsw.edu.au", "password": "Lyz1234567"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        # edit profile data
        email = {"email": "z5338660@ad.unsw.edu.au"}

        # Add the same user to DB using set preference
        response = client.put("/auth/setemail", headers=headers, json=email)

        # Check if the registration is unsuccessful
        assert response.status_code == 400
        assert "Invalid Input" in response.get_json()["error"]

        delete_user(zID="5338660")


def test_successful_email_set(client):
    """
    Test successfully setting a new email for a user.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        # Delete if user exist
        delete_user(zID="5338660")

        # Add user to DB
        add_dummy_user_to_db(
            "Evan", "Li", "5338660", "z5338660@ad.unsw.edu.au", "Lyz1234567", 1
        )

        # Define user login data
        login_data = {"email": "z5338660@ad.unsw.edu.au", "password": "Lyz1234567"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        # edit profile data
        email = {"email": "z5338661@ad.unsw.edu.au"}

        # Add the same user to DB using set preference
        response = client.put("/auth/setemail", headers=headers, json=email)

        # Check if the registration is unsuccessful
        assert response.status_code == 200
        assert "Set successful" in response.get_json()["message"]

        delete_user(zID="5338660")


def test_wrong_password(client):
    """
    Test updating the user's password with an incorrect current password.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        # Delete if user exist
        delete_user(zID="5338660")

        # Add user to DB
        add_dummy_user_to_db(
            "Evan", "Li", "5338660", "z5338660@ad.unsw.edu.au", "Lyz1234567", 1
        )

        # Define user login data
        login_data = {"email": "z5338660@ad.unsw.edu.au", "password": "Lyz1234567"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        # edit profile data
        password = {"currentPassword": "Lyz123123", "newPassword": "Lyz123456@"}

        # Add the same user to DB using set preference
        response = client.put("/auth/passwordreset", headers=headers, json=password)

        # Check if the registration is unsuccessful
        assert response.status_code == 400
        assert "Invalid Input" in response.get_json()["error"]

        delete_user(zID="5338660")


def test_weak_password(client):
    """
    Test updating the user's password with a weak new password.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        # Delete if user exist
        delete_user(zID="5338660")

        # Add user to DB
        add_dummy_user_to_db(
            "Evan", "Li", "5338660", "z5338660@ad.unsw.edu.au", "Lyz1234567", 1
        )

        # Define user login data
        login_data = {"email": "z5338660@ad.unsw.edu.au", "password": "Lyz1234567"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        # edit profile data
        password = {"currentPassword": "Lyz1234567", "newPassword": "123"}

        # Add the same user to DB using set preference
        response = client.put("/auth/passwordreset", headers=headers, json=password)

        # Check if the registration is unsuccessful
        assert response.status_code == 400
        assert "Invalid Input" in response.get_json()["error"]

        delete_user(zID="5338660")


def test_successful_password_reset(client):
    """
    Test updating the user's password with a weak new password.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        # Delete if user exist
        delete_user(zID="5338660")

        # Add user to DB
        add_dummy_user_to_db(
            "Evan", "Li", "5338660", "z5338660@ad.unsw.edu.au", "Lyz1234567", 1
        )

        # Define user login data
        login_data = {"email": "z5338660@ad.unsw.edu.au", "password": "Lyz1234567"}

        # Add the same user to DB using register
        response = client.post("/login", json=login_data)

        # Get headers
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        # edit profile data
        password = {"currentPassword": "Lyz1234567", "newPassword": "Lyz13579@"}

        # Add the same user to DB using set preference
        response = client.put("/auth/passwordreset", headers=headers, json=password)

        # Check if the registration is unsuccessful
        assert response.status_code == 200
        assert "Reset successful" in response.get_json()["message"]

        delete_user(zID="5338660")
