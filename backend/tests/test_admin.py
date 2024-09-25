import ast
import sys
import os
from datetime import datetime

current_directory = os.getcwd()
# Get the parent directory
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)
import hashlib
import json
import pytest
from app.app import app
from app.models import (
    db,
    User,
    Project,
    Group,
    GroupMember,
    Course,
    CourseEnrolment,
    CourseArchive,
)


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
        courseDescription="",
        courseSkills=json.dumps("{ 'c++': 100}"),
        courseKnowledge=json.dumps("{ 'c++': 100}"),
        topics=json.dumps("['topic', 'topic_2']"),
        school=school,
        yearDate=yearDate,
        term=term,
        thumbnail="null",
        revision=datetime.now(),
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


def check_course_count():
    return Course.query.count()


def check_enrolment_count():
    return CourseEnrolment.query.count()


def check_group_count():
    return Group.query.count()


def check_project_count():
    return Project.query.count()


def findCourseID(code, year, term):
    course = Course.query.filter_by(courseCode=code, yearDate=year, term=term).first()
    return course.ID


def findProjectID(name):
    project = Project.query.filter_by(projectName=name).first()
    return project.ID


def findGroupID(groupName, project):
    group = Group.query.filter_by(groupName=groupName, project=project).first()
    return group.ID


#####################
#       Tests       #
#####################
def test_successful_user_list(client):
    """
    Test the successful retrieval of a list of users with admin privileges.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        data = {"email": "banana@gmail.com", "password": "banana"}

        response = client.post("/login", json=data)

        assert response.status_code == 200
        assert "token" in response.get_json()
        assert "userType" in response.get_json()
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        response = client.get("/admin/all-users", headers=headers)

        assert response.status_code == 200
        data = response.get_json()
        assert len(data["users"]) == 2


def test_successful_course_list(client):
    """
    Test the successful retrieval of a list of courses with admin privileges.

    Args:
    - client: Flask test client.

    """
    with app.app_context():  # Create an application context
        data = {"email": "banana@gmail.com", "password": "banana"}

        response = client.post("/login", json=data)

        assert response.status_code == 200
        assert "token" in response.get_json()
        assert "userType" in response.get_json()
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        response = client.get("/admin/all-courses", headers=headers)

        assert response.status_code == 200
        data = response.get_json()
        assert len(data["courses"]) == 0


def test_successful_project_list(client):
    """
    Test the successful retrieval of a list of projects with admin privileges.

    Args:
    - client: Flask test client.

    Steps:
    1. Perform a successful login to obtain an access token.
    2. Create two sample projects using the access token.
    3. Use the access token to make a request to retrieve a list of all projects.
    4. Check that the response status code is 200.
    5. Check that the response contains the expected keys: "projects".
    6. Check that the number of projects in the response is as expected.
    7. Clean up by clearing the projects from the database.

    """
    with app.app_context():  # Create an application context
        data = {"email": "banana@gmail.com", "password": "banana"}

        response = client.post("/login", json=data)

        assert response.status_code == 200
        assert "token" in response.get_json()
        assert "userType" in response.get_json()
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        # Define project data
        project_data = {
            "name": "Test Project1",
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
        project_data = {
            "name": "Test Project 2",
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

        response = client.get("/admin/all-projects", headers=headers)

        assert response.status_code == 200
        data = response.get_json()
        assert len(data["projects"]) == 2

        clear_project()


def test_successful_admin_dashboard(client):
    """
    Test the successful retrieval of the admin dashboard information.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        clear_project()
        data = {"email": "banana@gmail.com", "password": "banana"}

        response = client.post("/login", json=data)

        assert response.status_code == 200
        assert "token" in response.get_json()
        assert "userType" in response.get_json()
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        # Define project data
        project_data = {
            "name": "Test Project1",
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
        project_data = {
            "name": "Test Project 2",
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

        response = client.get("/admin/all-projects", headers=headers)

        assert response.status_code == 200
        data = response.get_json()
        assert len(data["projects"]) == 2

        response = client.get("/admin/dashboard", headers=headers)

        assert response.status_code == 200
        data = response.get_json()
        assert data["dashboard"]["userCount"]["student"] == 2
        assert data["dashboard"]["userCount"]["casualAcademic"] == 1
        assert data["dashboard"]["userCount"]["academic"] == 1
        assert data["dashboard"]["userCount"]["courseAdmin"] == 0
        assert data["dashboard"]["userCount"]["admin"] == 1
        assert data["dashboard"]["courseCount"] == 0
        assert data["dashboard"]["projectCount"] == 2

        clear_project()


def test_course_delete(client):
    """
    Test the deletion of a course by an admin.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        clear_project()
        data = {"email": "banana@gmail.com", "password": "banana"}

        response = client.post("/login", json=data)

        assert response.status_code == 200
        assert "token" in response.get_json()
        assert "userType" in response.get_json()
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
            "code": "COMP9900",
            "year": "2022",
            "term": "T2",
            "description": "cs",
            "skills": {"c++": 100},
            "knowledge": {"c++": 100},
            "topics": ["topic", "topic_2"],
            "thumbnail": "null",
            "school": "School of Computer Science and Engineering",
        }

        # Add the course to DB using set preference
        response = client.put(
            f"/courses/{course.courseCode}/{course.yearDate}/{course.term}",
            headers=headers,
            json=courses,
        )

        # Check if the registration is unsuccessful

        assert response.status_code == 200
        assert "Course updated successfully." in response.get_json()["message"]

        response = client.get("/admin/all-courses", headers=headers)

        assert response.status_code == 200
        data = response.get_json()
        assert len(data["courses"]) == 1
        course = {"courseCode": "COMP9900", "yearDate": "2022", "term": "T2"}
        response = client.delete("/admin/course/delete", headers=headers, json=course)
        response = client.get("/admin/all-courses", headers=headers)

        assert response.status_code == 200
        data = response.get_json()
        assert len(data["courses"]) == 0

        clear_project()


def test_project_delete(client):
    """
    Test the deletion of a project by an admin.

    Args:
    - client: Flask test client.
    """
    with app.app_context():  # Create an application context
        clear_project()
        data = {"email": "banana@gmail.com", "password": "banana"}

        response = client.post("/login", json=data)

        assert response.status_code == 200
        assert "token" in response.get_json()
        assert "userType" in response.get_json()
        responseData = response.get_json()
        access_token = responseData.get("token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        project_data = {
            "name": "Test Project1",
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

        # Check if the registration is unsuccessful
        assert response.status_code == 200

        response = client.get("/admin/all-projects", headers=headers)

        assert response.status_code == 200
        data = response.get_json()
        assert len(data["projects"]) == 1
        project = {"ID": findProjectID(project_data["name"])}
        response = client.delete("/admin/project/delete", headers=headers, json=project)
        response = client.get("/admin/all-projects", headers=headers)

        assert response.status_code == 200
        data = response.get_json()
        assert len(data["projects"]) == 0


def test_group_delete(client):
    """
    Test the deletion of a group by an admin.

    Args:
    - client: Flask test client.

    """
    with app.app_context():
        clear_project()

        data = {"email": "banana@gmail.com", "password": "banana"}

        response = client.post("/login", json=data)

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

        project_id = response.get_json()["projects"][0]["id"]

        # Create a group
        response = client.post(
            f"/projects/groupCreate/{project_id}", json=group_data, headers=headers
        )

        assert response.status_code == 200
        assert response.get_json() == {"message": "Group created"}

        assert check_group_count() == 1

        group = {
            "groupID": findGroupID("Test Group", findProjectID(project_data["name"]))
        }

        response = client.delete("/admin/group/delete", headers=headers, json=group)
        response = client.get("/admin/all-projects", headers=headers)

        assert response.status_code == 200
        assert check_group_count() == 0
        # Delete the user from the database
        clear_project()


def test_student_project_list(client):
    """
    Test the retrieval of project list for a student.

    Args:
    - client: Flask test client.

    """
    with app.app_context():
        clear_project()

        data = {"email": "banana@gmail.com", "password": "banana"}

        response = client.post("/login", json=data)

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
            zid="5319978",
        )

        group = Group(groupName="Test Group", project=project.ID)

        db.session.add(group)
        db.session.commit()

        # Join a group
        response = client.put(
            f"/projects/join/{project.ID}/{group.ID}", headers=headers
        )

        assert response.status_code == 200
        assert response.get_json() == {"message": "User added to group"}

        userData = {"zID": "5319978"}

        response = client.get(
            f"/student/projects?zID={userData['zID']}", headers=headers, json=userData
        )
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["projects"]) == 1
        print(len(data))

        # Delete the user from the database
        clear_project()
