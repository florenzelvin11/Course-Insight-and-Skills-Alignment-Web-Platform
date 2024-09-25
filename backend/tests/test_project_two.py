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


def test_returns_correct_recommended_projects_single_project(client):
    """
    Test the retrieval of recommended projects for a single project, based on user skills.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        clear_project()
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

        # Define project data
        project_data = {
            "name": "Test Project",
            "client": "Test Client",
            "skills": {"c++": 100},
            "knowledge": {"java": 100},
            "thumbnail": "Test Thumbnail",
            "scope": "Test Scope",
            "topics": ["Test Topics"],
            "requirements": "Test Requirements",
            "outcomes": "Test Outcomes",
        }

        # Create a project
        response = client.post("/projects", json=project_data, headers=headers)

        # Check that the response is valid
        assert response.status_code == 200
        assert response.get_json() == {"message": "Project created successfully"}

        response = client.get(f"/projects/student", headers=headers)

        content = response.get_json()["projects"]

        assert len(content) == 1
        assert content[0]["client"] == "Test Client"
        assert content[0]["name"] == "Test Project"

        assert response.status_code == 200

        clear_project()
        delete_user(zID="5255998")
        delete_user(zID="1234569")


def test_returns_correct_recommended_projects_no_projects(client):
    """
    Test the retrieval of recommended projects when no projects are available.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        clear_project()
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

        response = client.get(f"/projects/student", headers=headers)

        content = response.get_json()["projects"]

        assert len(content) == 0
        assert response.status_code == 200

        clear_project()
        delete_user(zID="5255998")
        delete_user(zID="1234569")


def test_returns_correct_recommended_projects_multiple_sorted_order(client):
    """
    Test the retrieval of recommended projects for a user with multiple projects in sorted order.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        clear_project()
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

        # Define project data
        project_data = {
            "name": "Test Project",
            "client": "Test Client",
            "skills": {"essay writing": 100},
            "knowledge": {"python": 100},
            "thumbnail": "Test Thumbnail",
            "scope": "Test Scope",
            "topics": ["Test Topics"],
            "requirements": "Test Requirements",
            "outcomes": "Test Outcomes",
        }

        # Create a project
        response = client.post("/projects", json=project_data, headers=headers)

        # Check that the response is valid
        assert response.status_code == 200
        assert response.get_json() == {"message": "Project created successfully"}

        # Define project data
        project_data_two = {
            "name": "Test Project 2",
            "client": "Test Client 2",
            "skills": {"public speaking": 60, "essay writing": 100},
            "knowledge": {"python": 60, "c++": 40},
            "thumbnail": "Test Thumbnail",
            "scope": "Test Scope",
            "topics": ["Test Topics"],
            "requirements": "Test Requirements",
            "outcomes": "Test Outcomes",
        }

        # Create a project
        response = client.post("/projects", json=project_data_two, headers=headers)

        # Check that the response is valid
        assert response.status_code == 200
        assert response.get_json() == {"message": "Project created successfully"}

        # Define project data
        project_data_three = {
            "name": "Test Project 3",
            "client": "Test Client 3",
            "skills": {"public speaking": 60, "essay writing": 100},
            "knowledge": {"graphs": 100},
            "thumbnail": "Test Thumbnail",
            "scope": "Test Scope",
            "topics": ["Test Topics"],
            "requirements": "Test Requirements",
            "outcomes": "Test Outcomes",
        }

        # Create a project
        response = client.post("/projects", json=project_data_three, headers=headers)

        # Check that the response is valid
        assert response.status_code == 200
        assert response.get_json() == {"message": "Project created successfully"}

        response = client.get(f"/projects/student", headers=headers)

        content = response.get_json()["projects"]

        assert len(content) == 3
        assert content[0]["client"] == "Test Client 2"
        assert content[0]["name"] == "Test Project 2"

        assert content[1]["client"] == "Test Client 3"
        assert content[1]["name"] == "Test Project 3"

        assert content[2]["client"] == "Test Client"
        assert content[2]["name"] == "Test Project"

        assert response.status_code == 200

        clear_project()
        delete_user(zID="5255998")
        delete_user(zID="1234569")


def test_returns_correct_projects_information_multiple_projects(client):
    """"
    Test the retrieval of detailed information for many projects.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        clear_project()
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

        # Define project data
        project_data = {
            "name": "Test Project",
            "client": "Test Client",
            "skills": {"essay writing": 100},
            "knowledge": {"python": 100},
            "thumbnail": "Test Thumbnail",
            "scope": "Test Scope",
            "topics": ["Test Topics"],
            "requirements": "Test Requirements",
            "outcomes": "Test Outcomes",
        }

        # Create a project
        response = client.post("/projects", json=project_data, headers=headers)

        # Check that the response is valid
        assert response.status_code == 200
        assert response.get_json() == {"message": "Project created successfully"}

        # Define project data
        project_data_two = {
            "name": "Test Project 2",
            "client": "Test Client 2",
            "skills": {"public speaking": 60, "essay writing": 100},
            "knowledge": {"python": 60, "c++": 40},
            "thumbnail": "Test Thumbnail",
            "scope": "Test Scope",
            "topics": ["Test Topics"],
            "requirements": "Test Requirements",
            "outcomes": "Test Outcomes",
        }

        # Create a project
        response = client.post("/projects", json=project_data_two, headers=headers)

        # Check that the response is valid
        assert response.status_code == 200
        assert response.get_json() == {"message": "Project created successfully"}

        # Define project data
        project_data_three = {
            "name": "Test Project 3",
            "client": "Test Client 3",
            "skills": {"public speaking": 60, "essay writing": 100},
            "knowledge": {"graphs": 100},
            "thumbnail": "Test Thumbnail",
            "scope": "Test Scope",
            "topics": ["Test Topics"],
            "requirements": "Test Requirements",
            "outcomes": "Test Outcomes",
        }

        # Create a project
        response = client.post("/projects", json=project_data_three, headers=headers)

        # Check that the response is valid
        assert response.status_code == 200
        assert response.get_json() == {"message": "Project created successfully"}

        project_id = Project.query.filter_by(
            projectName=project_data_two["name"], client=project_data_two["client"]
        ).first()
        # Get that project
        response = client.get(f"/projects/{project_id.ID}", headers=headers)

        content = response.get_json()
        assert response.status_code == 200

        # Check that the contents of the project is correct
        assert content["client"] == project_data_two["client"]
        assert content["name"] == project_data_two["name"]
        assert content["knowledge"] == project_data_two["knowledge"]
        assert content["skills"] == project_data_two["skills"]
        assert content["outcomes"] == project_data_two["outcomes"]
        assert content["requirements"] == project_data_two["requirements"]
        assert content["thumbnail"] == project_data_two["thumbnail"]
        assert content["topics"] == project_data_two["topics"]
        assert content["missingKnowledge"] == []
        assert content["missingSkills"] == []
        assert content["percentageMatch"] == 100
        assert content["groups"] == []

        clear_project()
        delete_user(zID="5255998")
        delete_user(zID="1234569")


def test_returns_correct_projects_information(client):
    """
    Test the retrieval of detailed information for a specific project.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        clear_project()
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

        # Define project data
        project_data = {
            "name": "Test Project",
            "client": "Test Client",
            "skills": {"essay writing": 100},
            "knowledge": {"python": 100},
            "thumbnail": "Test Thumbnail",
            "scope": "Test Scope",
            "topics": ["Test Topics"],
            "requirements": "Test Requirements",
            "outcomes": "Test Outcomes",
        }

        # Create a project
        response = client.post("/projects", json=project_data, headers=headers)

        # Check that the response is valid
        assert response.status_code == 200
        assert response.get_json() == {"message": "Project created successfully"}

        # Define project data
        project_data_two = {
            "name": "Test Project 2",
            "client": "Test Client 2",
            "skills": {"public speaking": 60, "essay writing": 100},
            "knowledge": {"python": 60, "c++": 40},
            "thumbnail": "Test Thumbnail",
            "scope": "Test Scope",
            "topics": ["Test Topics"],
            "requirements": "Test Requirements",
            "outcomes": "Test Outcomes",
        }

        # Create a project
        response = client.post("/projects", json=project_data_two, headers=headers)

        # Check that the response is valid
        assert response.status_code == 200
        assert response.get_json() == {"message": "Project created successfully"}

        project_id = Project.query.filter_by(
            projectName=project_data["name"], client=project_data["client"]
        ).first()
        # Get that project
        response = client.get(f"/projects/{project_id.ID}", headers=headers)

        content = response.get_json()
        assert response.status_code == 200

        # Check that the contents of the project is correct
        assert content["client"] == project_data["client"]
        assert content["name"] == project_data["name"]
        assert content["knowledge"] == project_data["knowledge"]
        assert content["skills"] == project_data["skills"]
        assert content["outcomes"] == project_data["outcomes"]
        assert content["requirements"] == project_data["requirements"]
        assert content["thumbnail"] == project_data["thumbnail"]
        assert content["topics"] == project_data["topics"]
        assert content["missingKnowledge"] == []
        assert content["missingSkills"] == []
        assert content["percentageMatch"] == 100
        assert content["groups"] == []

        clear_project()
        delete_user(zID="5255998")
        delete_user(zID="1234569")


def test_returns_correct_projects_information_multiple_projects_with_groups(client):
    """
    Test the retrieval of detailed information for many specific project with associated groups.

    Args:
    - client: Flask test client.
    """
    with app.app_context():
        clear_project()
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

        # Define project data
        project_data = {
            "name": "Test Project",
            "client": "Test Client",
            "skills": {"essay writing": 100},
            "knowledge": {"python": 100},
            "thumbnail": "Test Thumbnail",
            "scope": "Test Scope",
            "topics": ["Test Topics"],
            "requirements": "Test Requirements",
            "outcomes": "Test Outcomes",
        }

        # Create a project
        response = client.post("/projects", json=project_data, headers=headers)

        # Check that the response is valid
        assert response.status_code == 200
        assert response.get_json() == {"message": "Project created successfully"}

        # Define project data
        project_data_two = {
            "name": "Test Project 2",
            "client": "Test Client 2",
            "skills": {"public speaking": 60, "essay writing": 100},
            "knowledge": {"python": 60, "c++": 40},
            "thumbnail": "Test Thumbnail",
            "scope": "Test Scope",
            "topics": ["Test Topics"],
            "requirements": "Test Requirements",
            "outcomes": "Test Outcomes",
        }

        # Create a project
        response = client.post("/projects", json=project_data_two, headers=headers)

        # Check that the response is valid
        assert response.status_code == 200
        assert response.get_json() == {"message": "Project created successfully"}

        # Define project data
        project_data_three = {
            "name": "Test Project 3",
            "client": "Test Client 3",
            "skills": {"public speaking": 60, "essay writing": 100},
            "knowledge": {"graphs": 100},
            "thumbnail": "Test Thumbnail",
            "scope": "Test Scope",
            "topics": ["Test Topics"],
            "requirements": "Test Requirements",
            "outcomes": "Test Outcomes",
        }

        # Create a project
        response = client.post("/projects", json=project_data_three, headers=headers)

        # Check that the response is valid
        assert response.status_code == 200
        assert response.get_json() == {"message": "Project created successfully"}

        project_id = Project.query.filter_by(
            projectName=project_data_two["name"], client=project_data_two["client"]
        ).first()

        group = Group(groupName="Test Group", project=project_id.ID)

        db.session.add(group)
        db.session.commit()

        # Join a group
        response = client.put(
            f"/projects/join/{project_id.ID}/{group.ID}", headers=headers
        )
        print(response.get_json())

        assert response.status_code == 200
        assert response.get_json() == {"message": "User added to group"}

        # Get that project
        response = client.get(f"/projects/{project_id.ID}", headers=headers)

        content = response.get_json()
        assert response.status_code == 200

        # Check that the contents of the project is correct
        assert content["client"] == project_data_two["client"]
        assert content["name"] == project_data_two["name"]
        assert content["knowledge"] == project_data_two["knowledge"]
        assert content["skills"] == project_data_two["skills"]
        assert content["outcomes"] == project_data_two["outcomes"]
        assert content["requirements"] == project_data_two["requirements"]
        assert content["thumbnail"] == project_data_two["thumbnail"]
        assert content["topics"] == project_data_two["topics"]
        assert content["missingKnowledge"] == []
        assert content["missingSkills"] == []
        assert content["percentageMatch"] == 100
        assert content["groups"] == [
            {"id": group.ID, "groupName": group.groupName, "members": [5255998]}
        ]

        clear_project()
        delete_user(zID="5255998")
        delete_user(zID="1234569")
