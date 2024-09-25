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
from app.models import db, User, Project, Group, GroupMember


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


def add_dummy_project_to_db(name, client, skills, thumbnail, scope, topics, zid):
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
    new_project = Project(
        projectName=name,
        client=client,
        skills=skills,
        thumbnail=thumbnail,
        scope=scope,
        topics=topics,
        creatorZId=zid,
    )
    db.session.add(new_project)
    db.session.commit()

    return new_project


def delete_project(id):
    """
    Delete a project from the database.

    Parameters:
    - id (int): The ID of the project to be deleted.
    """
    # Find the project by its ID
    project = Project.query.filter_by(ID=id).first()
    if project:
        # Delete the project from the database session
        db.session.delete(project)
        # Commit the changes to the database
        db.session.commit()


def clear_project():
    """
    Clear all projects, groups, and group members from the database.
    """
    db.session.query(GroupMember).delete()
    db.session.query(Group).delete()
    db.session.query(Project).delete()
    db.session.commit()


#####################
#       Tests       #
#####################
def test_successful_project_create(client):
    """
    Test the successful creation of a project.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        clear_project()

        # Add a dummy user to the database
        add_dummy_user_to_db(
            firstname="John",
            lastname="Smith",
            zID="1234569",
            email="z1234569@ad.unsw.edu.au",
            password="Lyz1234569",
            verified=1,
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

        # Define project data
        project_data = {
            "name": "Test Project",
            "client": "Test Client",
            "skills": json.dumps({"c++": 60}),
            "knowledge": json.dumps({"java": 60}),
            "thumbnail": "Test Thumbnail",
            "scope": "Test Scope",
            "topics": json.dumps(["Test Topics"]),
            "requirements": "Test Requirements",
            "outcomes": "Test Outcomes",
        }

        # Create a project
        response = client.post("/projects", json=project_data, headers=headers)

        # Check that the response is valid
        assert response.status_code == 200
        assert response.get_json() == {"message": "Project created successfully"}

        # Delete the user from the database
        clear_project()
        delete_user(zID="1234569")


def test_academic_results(client):
    """
    Test the retrieval of academic projects for a specific user.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        clear_project()

        # Add a dummy user to the database
        add_dummy_user_to_db(
            firstname="John",
            lastname="Smith",
            zID="1234569",
            email="z1234569@ad.unsw.edu.au",
            password="Lyz1234569",
            verified=1,
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

        # Define project data
        project_data = {
            "name": "Test Project",
            "client": "Test Client",
            "skills": json.dumps({"c++": 60}),
            "knowledge": json.dumps({"java": 60}),
            "thumbnail": "Test Thumbnail",
            "scope": "Test Scope",
            "topics": json.dumps(["Test Topics"]),
            "requirements": "Test Requirements",
            "outcomes": "Test Outcomes",
        }

        # Create a project
        response = client.post("/projects", json=project_data, headers=headers)

        # Check that the response is valid
        assert response.status_code == 200
        assert response.get_json() == {"message": "Project created successfully"}

        # Get the created projects
        response = client.get("/projects/academic", headers=headers)
        assert response.status_code == 200
        assert response.get_json()["projects"].__len__() == 1

        # Delete the user from the database
        clear_project()
        delete_user(zID="1234569")


def test_group_create(client):
    """
    Test the creation of a group within a specific academic project.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        clear_project()

        # Add a dummy user to the database
        add_dummy_user_to_db(
            firstname="John",
            lastname="Smith",
            zID="1234569",
            email="z1234569@ad.unsw.edu.au",
            password="Lyz1234569",
            verified=1,
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

        # Define project data
        project_data = {
            "name": "Test Project",
            "client": "Test Client",
            "skills": json.dumps({"c++": 60}),
            "knowledge": json.dumps({"java": 60}),
            "thumbnail": "Test Thumbnail",
            "scope": "Test Scope",
            "topics": json.dumps(["Test Topics"]),
            "requirements": "Test Requirements",
            "outcomes": "Test Outcomes",
        }

        # Create a project
        response = client.post("/projects", json=project_data, headers=headers)

        # Check that the response is valid
        assert response.status_code == 200
        assert response.get_json() == {"message": "Project created successfully"}

        # Get the created projects
        response = client.get("/projects/academic", headers=headers)

        assert response.status_code == 200
        assert response.get_json()["projects"].__len__() == 1

        # Define group data
        group_data = {"groupName": "Test Group"}

        project_id = (response.get_json()["projects"][0]["id"],)

        # Create a group
        response = client.post(
            f"/projects/groupCreate/{project_id[0]}", json=group_data, headers=headers
        )
        print(response.get_json())

        assert response.status_code == 200
        assert response.get_json() == {"message": "Group created"}

        # Delete the user from the database
        clear_project()
        delete_user(zID="1234569")


def test_group_join(client):
    """
    Test the successful joining of a group

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        clear_project()

        # Add a dummy user to the database
        add_dummy_user_to_db(
            firstname="John",
            lastname="Smith",
            zID="1234569",
            email="z1234569@ad.unsw.edu.au",
            password="Lyz1234569",
            verified=1,
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

        project = add_dummy_project_to_db(
            name="Test Project",
            client="Test Client",
            skills="Test Skills",
            thumbnail="Test Thumbnail",
            scope="Test Scope",
            topics="Test Topics",
            zid="1234569",
        )

        group = Group(groupName="Test Group", project=project.ID)

        db.session.add(group)
        db.session.commit()

        # Join a group
        response = client.put(
            f"/projects/join/{project.ID}/{group.ID}", headers=headers
        )
        print(response.get_json())

        assert response.status_code == 200
        assert response.get_json() == {"message": "User added to group"}

        # Delete the user from the database
        clear_project()
        delete_user(zID="1234569")


def test_group_join_project_not_exsist(client):
    """
    Test the failed joining of a group within a non-existing academic project.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        clear_project()

        # Add a dummy user to the database
        add_dummy_user_to_db(
            firstname="John",
            lastname="Smith",
            zID="1234569",
            email="z1234569@ad.unsw.edu.au",
            password="Lyz1234569",
            verified=1,
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

        project = add_dummy_project_to_db(
            name="Test Project",
            client="Test Client",
            skills="Test Skills",
            thumbnail="Test Thumbnail",
            scope="Test Scope",
            topics="Test Topics",
            zid="1234569",
        )

        group = Group(groupName="Test Group", project=project.ID)

        db.session.add(group)
        db.session.commit()

        # Join a group
        response = client.put(f"/projects/join/123/{group.ID}", headers=headers)
        print(response.get_json())

        assert response.status_code == 400
        assert response.get_json() == {"error": "Project does not exist"}

        # Delete the user from the database
        clear_project()
        delete_user(zID="1234569")


def test_group_join_group_not_exsist(client):
    """
    Test the failed joining of a non-existent group.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        clear_project()

        # Add a dummy user to the database
        add_dummy_user_to_db(
            firstname="John",
            lastname="Smith",
            zID="1234569",
            email="z1234569@ad.unsw.edu.au",
            password="Lyz1234569",
            verified=1,
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

        project = add_dummy_project_to_db(
            name="Test Project",
            client="Test Client",
            skills="Test Skills",
            thumbnail="Test Thumbnail",
            scope="Test Scope",
            topics="Test Topics",
            zid="1234569",
        )

        group = Group(groupName="Test Group", project=project.ID)

        db.session.add(group)
        db.session.commit()

        # Join a group
        response = client.put(f"/projects/join/{project.ID}/123", headers=headers)
        print(response.get_json())

        assert response.status_code == 400
        assert response.get_json() == {"error": "Group does not exist"}

        # Delete the user from the database
        clear_project()
        delete_user(zID="1234569")


def test_group_join_user_already_exsist(client):
    """
    Test the failed joining of a group due to user already in group.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        clear_project()

        # Add a dummy user to the database
        add_dummy_user_to_db(
            firstname="John",
            lastname="Smith",
            zID="1234569",
            email="z1234569@ad.unsw.edu.au",
            password="Lyz1234569",
            verified=1,
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

        project = add_dummy_project_to_db(
            name="Test Project",
            client="Test Client",
            skills="Test Skills",
            thumbnail="Test Thumbnail",
            scope="Test Scope",
            topics="Test Topics",
            zid="1234569",
        )

        group = Group(groupName="Test Group", project=project.ID)

        db.session.add(group)
        db.session.commit()

        # Join a group
        response = client.put(
            f"/projects/join/{project.ID}/{group.ID}", headers=headers
        )
        response = client.put(
            f"/projects/join/{project.ID}/{group.ID}", headers=headers
        )
        print(response.get_json())

        assert response.status_code == 400
        assert response.get_json() == {"error": "User already in group"}

        # Delete the user from the database
        clear_project()
        delete_user(zID="1234569")
