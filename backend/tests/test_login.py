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
from flask_jwt_extended import jwt_required, get_jwt_identity


@pytest.fixture
def client():
    # Create and return a test client for the Flask app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def add_dummy_user_to_db(firstname, lastname, zID, email, password, verified):
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
    Get a user's verification code from the database.

    Args:
    - zID (str): The unique identifier for the user whose verification code is to be deleted.
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


def test_registration_with_existing_email_and_zID(client):
    """
    Test user registration with an existing email and zID.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        # Add user to DB
        add_dummy_user_to_db(
            "Sammi", "Au-Yeung", "1255997", "z1255997@ad.unsw.edu.au", "IamSammi123*", 1
        )

        # Define user registration data
        registration_data = {
            "zId": "z1255997",
            "firstName": "Sammi",
            "lastName": "Au-Yeung",
            "email": "z1255997@ad.unsw.edu.au",
            "password": "IamSammi123*",
        }

        # Add the same user to DB using register
        response = client.post("/register", json=registration_data)

        # Check if the registration is unsuccessful
        assert response.status_code == 400
        response_data = json.loads(response.data.decode("utf-8"))
        print(response_data)
        assert (
            "User already exists. Please use a different zID or login to your existing account."
            in response_data["error"]
        )

        delete_user(zID="1255997")


def test_registration_with_existing_email(client):
    """
    Test user registration with an existing email.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        # Add user to DB
        add_dummy_user_to_db(
            "Sammi", "Au-Yeung", "1255997", "z1255997@ad.unsw.edu.au", "IamSammi123*", 1
        )

        # Define user registration data - different zID, same email
        registration_data = {
            "zId": "z2255997",
            "firstName": "Sammi",
            "lastName": "Au-Yeung",
            "email": "z1255997@ad.unsw.edu.au",
            "password": "IamSammi123*",
        }

        # Add the same user to DB using register
        response = client.post("/register", json=registration_data)

        # Check if the registration is unsuccessful
        assert response.status_code == 400
        response_data = json.loads(response.data.decode("utf-8"))
        assert (
            "Email already exists. Please use a different email"
            in response_data["error"]
        )  # Error message should be present

        delete_user(zID="1255997")


def test_registration_with_missing_fields(client):
    """
    Test user registration with missing fields.

    Args:
    - client: Flask test client.
    """
    # Define user registration data - missing zID and password
    registration_data = {
        "firstName": "Sammi",
        "lastName": "Au-Yeung",
        "email": "z1255997@ad.unsw.edu.au",
    }

    # Add the same user to DB using register
    response = client.post("/register", json=registration_data)

    # Check if the registration is unsuccessful
    assert response.status_code == 400
    response_data = json.loads(response.data.decode("utf-8"))
    assert (
        "Please provide all required fields" in response_data["error"]
    )  # Error message should be present


def test_registration_with_existing_zID(client):
    """
    Test user registration with an existing zID.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        # Add user to DB
        add_dummy_user_to_db(
            "Sammi", "Au-Yeung", "1255997", "z1255997@ad.unsw.edu.au", "IamSammi123*", 1
        )

        # Define user registration data - different email, same zID
        registration_data = {
            "zId": "z1255997",
            "firstName": "Sammi",
            "lastName": "Au-Yeung",
            "email": "z2255997@ad.unsw.edu.au",
            "password": "IamSammi123*",
        }

        # Add the same user to DB using register
        response = client.post("/register", json=registration_data)

        # Check if the registration is unsuccessful
        assert response.status_code == 400
        response_data = json.loads(response.data.decode("utf-8"))
        assert (
            "User already exists. Please use a different zID or login to your existing account."
            in response_data["error"]
        )  # Error message should be present

        delete_user(zID="1255997")


def test_login_successfully(client):
    """
    Test successful user login.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        add_dummy_user_to_db(
            "Sammi", "Au-Yeung", "1255997", "z1255997@ad.unsw.edu.au", "IamSammi123*", 1
        )
        # Test a successful login
        data = {"email": "z1255997@ad.unsw.edu.au", "password": "IamSammi123*"}

        response = client.post("/login", json=data)
        assert response.status_code == 200
        assert "token" in response.get_json()
        assert "userType" in response.get_json()

        delete_user(zID="1255997")


def test_login_unverified(client):
    """
    Test login for an unverified user.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        add_dummy_user_to_db(
            "Sammi", "Au-Yeung", "1255997", "z1255997@ad.unsw.edu.au", "IamSammi123*", 0
        )

        data = {"email": "z1255997@ad.unsw.edu.au", "password": "IamSammi123*"}

        response = client.post("/login", json=data)
        assert response.status_code == 401
        print(response.get_json()["error"])
        assert (
            "User unverified, please sign up again with the same details"
            in response.get_json()["error"]
        )

        delete_user(zID="1255997")


def test_login_failed_wrong_password(client):
    """
    Test login with an incorrect password.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        add_dummy_user_to_db(
            "Sammi", "Au-Yeung", "1255997", "z1255997@ad.unsw.edu.au", "IamSammi123*", 1
        )

        # Wrong password
        data = {"email": "z1255997@ad.unsw.edu.au", "password": "IamSammi123"}

        response = client.post("/login", json=data)
        assert response.status_code == 401
        assert "Invalid email or password" in response.get_json()["error"]

        delete_user(zID="1255997")


def test_login_failed_wrong_email(client):
    """
    Test login with an incorrect email.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        add_dummy_user_to_db(
            "Sammi", "Au-Yeung", "1255997", "z1255997@ad.unsw.edu.au", "IamSammi123*", 1
        )

        # Wrong password
        data = {"email": "z2255997@ad.unsw.edu.au", "password": "IamSammi123*"}

        response = client.post("/login", json=data)
        assert response.status_code == 401
        assert "Invalid email or password" in response.get_json()["error"]

        delete_user(zID="1255997")


def test_successful_logout(client):
    """
    Test successful logout.

    Args:
    - client: Flask test client.
    """
    # login
    login_data = {"email": "banana@gmail.com", "password": "banana"}

    response = client.post("/login", json=login_data)
    assert response.status_code == 200

    # Define header for request
    responseData = response.get_json()
    access_token = responseData.get("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    response = client.post("/logout", headers=headers)
    assert response.status_code == 200
    assert "Logout successful" in response.get_json()["message"]


def test_email_verification_with_no_invalid_code(client):
    """
    Test email verification with an invalid verification code.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        # Add a new unverified user
        add_dummy_user_to_db(
            "Sammi", "Au-Yeung", "1255997", "z1255997@ad.unsw.edu.au", "IamSammi123*", 0
        )

        # Send a valid verification code
        verification_data = {"zId": "z1255997", "code": "INVALID"}

        response = client.post("/verifyCode", json=verification_data)
        # Check if the verification fails (status code 400)
        assert response.status_code == 400

        # Clean up by deleting the unverified user
        delete_user(zID="1255997")


def test_registration_with_valid_data(client):
    """
    Test email verification with an invalid verification code.

    Args:
    - client: Flask test client.
    """
    # Define user registration data with unique information
    registration_data = {
        "zId": "z5255135",
        "firstName": "Finbar",
        "lastName": "Kelly",
        "email": "z1255997@ad.unsw.edu.au",
        "password": "SecurePassword123*",
    }

    # Attempt to register with valid data
    response = client.post("/register", json=registration_data)

    # Check if the registration is successful (status code 200)
    assert response.status_code == 200

    # Clean up by deleting the newly registered user
    delete_usercode(zID="5255135")
    delete_user(zID="5255135")


def test_registration_with_valid_usercode(client):
    """
    Test user registration with a valid user code.

    Args:
    - client: Flask test client.
    """
    # Define user registration data with unique information
    registration_data = {
        "zId": "z5255135",
        "firstName": "Finbar",
        "lastName": "Kelly",
        "email": "z1255997@ad.unsw.edu.au",
        "password": "SecurePassword123*",
    }

    # Attempt to register with valid data
    response = client.post("/register", json=registration_data)

    # Define header for request
    responseData = response.get_json()
    access_token = responseData.get("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    # Check if the registration is successful (status code 200)
    assert response.status_code == 200

    print(response)

    usercode = get_usercode(zID="5255135")
    usercode_data = {"zId": "z5255135", "code": usercode}
    response = client.post("/verifyCode", json=usercode_data)
    assert response.status_code == 200
    # Clean up by deleting the newly registered user
    delete_usercode(zID="5255135")
    delete_user(zID="5255135")


def test_registration_with_invalid_usercode(client):
    """
    Test user registration with invalid user code.

    Args:
    - client: Flask test client.
    """
    registration_data = {
        "zId": "z5255135",
        "firstName": "Finbar",
        "lastName": "Kelly",
        "email": "z1255997@ad.unsw.edu.au",
        "password": "SecurePassword123*",
    }

    # Attempt to register with valid data
    response = client.post("/register", json=registration_data)

    # Define header for request
    responseData = response.get_json()
    access_token = responseData.get("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    # Define header for request
    responseData = response.get_json()
    access_token = responseData.get("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    # Check if the registration is successful (status code 200)
    assert response.status_code == 200

    print(response)

    usercode = get_usercode(zID="5255135")
    usercode_data = {"zId": "z5255135", "code": "ABCDE"}
    response = client.post("/verifyCode", json=usercode_data)
    assert response.status_code == 400
    # Clean up by deleting the newly registered user
    delete_usercode(zID="5255135")
    delete_user(zID="5255135")


def test_giving_non_existent_user_roles(client):
    """
    Test attempting to assign roles to a non-existent user.

    Args:
    - client: Flask test client.
    """
    # login
    login_data = {"email": "banana@gmail.com", "password": "banana"}

    response = client.post("/login", json=login_data)
    assert response.status_code == 200

    # Define header for request
    responseData = response.get_json()
    access_token = responseData.get("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    # Define user registration data with unique information
    given_role_data = {"zId": "z5255135", "userType": "academic"}

    # Attempt to register with valid data
    response = client.put(
        "admin/user/edit/usertype", headers=headers, json=given_role_data
    )

    # Check if the registration is successful (status code 200)
    assert response.status_code == 200

    # Clean up by deleting the newly registered user
    delete_user(zID="5255135")

    response = client.post("/logout", headers=headers)
    assert response.status_code == 200
    assert "Logout successful" in response.get_json()["message"]


def test_giving_existent_duplicate_user_roles(client):
    """
    Test attempting to assign duplicate roles to an existing user.

    Args:
    - client: Flask test client.
    """
    # login
    login_data = {"email": "banana@gmail.com", "password": "banana"}

    response = client.post("/login", json=login_data)
    assert response.status_code == 200

    # Define header for request
    responseData = response.get_json()
    access_token = responseData.get("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    # Define user registration data with unique information
    given_role_data = {"zId": "z5255135", "userType": "academic"}

    # Attempt to register with valid data
    response = client.put(
        "admin/user/edit/usertype", headers=headers, json=given_role_data
    )
    assert response.status_code == 200

    # Attempt to duplicate role
    given_role_data = {"zId": "z5255135", "userType": "academic"}

    response = client.put(
        "admin/user/edit/usertype", headers=headers, json=given_role_data
    )

    # Check if the registration is failed due to duplicate assignment (status code 400)
    assert response.status_code == 400
    # Clean up by deleting the newly registered user
    delete_user(zID="5255135")

    response = client.post("/logout", headers=headers)
    assert response.status_code == 200
    assert "Logout successful" in response.get_json()["message"]


def test_giving_existent_user_more_roles(client):
    """
    Test attempting to assign additional roles to an existing user.

    Args:
    - client: Flask test client.
    """
    # login
    login_data = {"email": "banana@gmail.com", "password": "banana"}

    response = client.post("/login", json=login_data)
    assert response.status_code == 200

    # Define header for request
    responseData = response.get_json()
    access_token = responseData.get("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    # Define user registration data with unique information
    given_role_data = {"zId": "z5255135", "userType": "academic"}

    # Attempt to register with valid data
    response = client.put(
        "admin/user/edit/usertype", headers=headers, json=given_role_data
    )

    assert response.status_code == 200

    # Attempt to duplicate role
    given_role_data = {"zId": "z5255135", "userType": "casual academic"}

    response = client.put(
        "admin/user/edit/usertype", headers=headers, json=given_role_data
    )

    # Check if the registration is failed due to duplicate assignment (status code 400)
    assert response.status_code == 200
    # Clean up by deleting the newly registered user
    delete_user(zID="5255135")

    response = client.post("/logout", headers=headers)
    assert response.status_code == 200
    assert "Logout successful" in response.get_json()["message"]
