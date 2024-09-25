'''
This file contains the APIs related to the project dashboard and projects
page. It also contains the functions that those APIs used.

'''
import json
import sys
import os
from flask import Blueprint, jsonify, request
from recommendations.recommended_projects import get_project_recommendations, \
                    get_missing_skills_and_knowledge, get_percentage_match

from flask_jwt_extended import jwt_required, get_jwt_identity

try:
    from models import db, User, Project, Group, GroupMember
except ImportError:
    from .models import db, User, Project, Group, GroupMember

# # Get the current and parent directory
current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

projects = Blueprint("projects", __name__)

def get_recommended_projects(zID):
    """
    Given the user's zID, this function will return projects that
    utilises the skills a user has.
    """
    user = User.query.filter_by(zID=zID).first()
    user_metaData = json.loads(user.metadataJson)
    user_knowledge = user_metaData["class"]["student"]["knowledge"]
    user_skills = user_metaData["class"]["student"]["skills"]

    all_projects = []
    projects = Project.query.all()
    for project in projects:
        project_ID = project.ID
        project_skills = json.loads(project.skills)
        project_knowledge = json.loads(project.skills)
        all_projects.append(
            {
                "name": project_ID,
                "Project required knowledge": project_knowledge,
                "Project required skills": project_skills,
            }
        )
    recommended_projects = get_project_recommendations(
        all_projects, user_skills, user_knowledge
    )
    if len(recommended_projects) == 0:
        return {"projects": []}, 200

    project_Id_recommended = [item[0] for item in recommended_projects]
    top_recommended_projects = project_Id_recommended[:10]

    recommended_projects_info = []

    for project in top_recommended_projects:
        project_all_info = Project.query.filter_by(ID=project).first()
        project_required_info = {
            "id": project_all_info.ID,
            "name": project_all_info.projectName,
            "client": project_all_info.client,
            "skills": json.loads(project_all_info.skills),
            "knowledge": json.loads(project_all_info.knowledge),
            "thumbnail": project_all_info.thumbnail,
        }
        recommended_projects_info.append(project_required_info)
    return {"projects": recommended_projects_info}, 200


def get_certain_project(zID, projectId):
    """
    Given the project ID and the zID of a student, this function
    will return the information about that project.
    """
    user = User.query.filter_by(zID=zID).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    user_metaData = json.loads(user.metadataJson)
    student_knowledge = user_metaData["class"]["student"]["knowledge"]
    student_skills = user_metaData["class"]["student"]["skills"]
    project_info = Project.query.filter_by(ID=projectId).first()
    if not project_info:
        return jsonify({"error": "Project not found"}), 404

    project_skills = json.loads(project_info.skills)
    project_knowledge = json.loads(project_info.knowledge)

    project_data = [
        {
            "name": project_info.projectName,
            "Project required knowledge": project_knowledge,
            "Project required skills": project_skills,
        }
    ]

    missing_skills, missing_knowledge = get_missing_skills_and_knowledge(
        project_data, student_skills, student_knowledge
    )

    skills_knowledge_size = len(project_skills) + len(project_knowledge)
    missing_size = len(missing_skills) + len(missing_knowledge)

    full_project_info = {
        "id": project_info.ID,
        "name": project_info.projectName,
        "client": project_info.client,
        "skills": json.loads(project_info.skills),
        "knowledge": json.loads(project_info.knowledge),
        "missingKnowledge": list(missing_knowledge),
        "missingSkills": list(missing_skills),
        "thumbnail": project_info.thumbnail,
        "scope": project_info.scope,
        "requirements": project_info.requirements,
        "topics": json.loads(project_info.topics),
        "outcomes": project_info.outcomes,
        "percentageMatch": get_percentage_match(skills_knowledge_size, missing_size),
        "groups": get_groups_of_certain_project(projectId),
    }
    return jsonify(full_project_info), 200


def get_groups_of_certain_project(projectId):
    """
    This function will get all the groups relating to a certain project.
    """
    groups = Group.query.filter_by(project=projectId).all()

    groups_info = []

    for group in groups:
        group_details = {
            "id": group.ID,
            "groupName": group.groupName,
            "members": get_members_of_group(group.ID),
        }
        groups_info.append(group_details)
    return groups_info


def get_members_of_group(groupId):
    '''
    Retrieve the members (students) of a group based on the group ID.

    Parameters:
    - groupId (int): The groupId of the group.

    Returns:
    - list: A list of zID of the members in the group.
    '''
    group_members = GroupMember.query.filter_by(groupID=groupId).all()
    members_zID = []
    for group_member in group_members:
        members_zID.append(group_member.student)
    return members_zID


@projects.route("/projects/student", methods=["GET"])
@jwt_required()
def get_recommended_projects_students():
    '''
    Endpoint to retrieve recommended projects for the currently authenticated student.

    Requires a valid JWT token with the student's zID.

    Returns:
    JSON: A JSON response containing the recommended projects for the student and a
    status code.
    '''
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(zID=current_user_id).first()
    # identify user role
    if not user:
        return jsonify({"error": "Invalid token."}), 401

    response = get_recommended_projects(user.zID)
    return response


@projects.route("/projects/<projectId>", methods=["GET"])
@jwt_required()
def get_certain_projects_students(projectId):

    '''
    Endpoint to retrieve details of a specific project for the currently authenticated student.

    Requires a valid JWT token with the student's zID.

    Parameters:
    - projectId (int): The project ID of the project to retrieve details for.

    Returns:
    JSON: A JSON response containing the details of the specified project for the student.

    Example:
    GET /projects/83262

    Response:
        {
        id: 83262,
        name: "Fitness Tracker",
        client: "Jane Doe",
        skills: { "writing": 60, "speaking": 40 },
        knowledge: { "c++": 60, "JavaScript": 40 },
        missingKnowledge: ["c++", "JavaScript"],
        missingSkills: ["problem solving", "communication"],
        thumbnail: "https://cdn.dribbble.com...",
        scope: "string",
        requirements: "Completed COMP1511"
        topics: ["topic 1", "topic 2"],
        outcomes: "string",
        percentageMatch: 50,
        groups: [
            {
            id: 15,
            groupName: "best group",
            members: ["z5255135", "z5288212"]
            },
            {
            id: 72,
            groupName: "another group",
            members: ["z5455335", "z5282674"]
            }
        ],
        }

    '''
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(zID=current_user_id).first()
    # identify user role
    if not user:
        return jsonify({"error": "Invalid token."}), 401

    response = get_certain_project(user.zID, projectId)
    return response


@projects.route("/projects/academic", methods=["GET"])
@jwt_required()
def get_created_projects():
    """
    Gets all academic projects which the user has created

    Requires a valid JWT token with the user's unique identifier.

    Returns:
    JSON: A JSON response containing details of academic projects created by the user.

    Example:
    GET /projects/academic

    Response:
    {
    projects: [
        {
        id: 83262,
        name: "Fitness Tracker",
        client: "Jane Doe",
        skills: { "writing": 60, "speaking": 40 },
        knowledge: { "c++": 60, "JavaScript": 40 },
        thumbnail: "https://cdn.dribbble.com...",
        }, ...
    ]
    }
    """

    user_id = get_jwt_identity()

    projects = Project.query.filter_by(creatorZId=user_id).all()
    result = {"projects": []}

    for project in projects:
        result["projects"].append(
            {
                "id": project.ID,
                "name": project.projectName,
                "client": project.client,
                "skills": json.loads(project.skills),
                "knowledge": json.loads(project.knowledge),
                "thumbnail": project.thumbnail,
            }
        )
    return jsonify(result), 200


@projects.route("/projects", methods=["POST"])
@jwt_required()
def create_project():
    """
    Creates a new project

    Requires a valid JWT token with the user's unique identifier.

    Request:
    - Method: POST
    - Content-Type: application/json
    - Body:
        {
        name: "Fitness Tracker",
        client: "Jane Doe",
        skills: { "writing": 60, "speaking": 40 },
        knowledge: { "c++": 60, "JavaScript": 40 },
        thumbnail: "https://cdn.dribbble.com...",
        scope: "string",
        topics: ["topic 1", "topic 2"],
        requirements: "Completed COMP1511"
        outcomes: "string",
        }

    Returns:
    JSON: A JSON response indicating the success of the project creation.

    """

    user_id = get_jwt_identity()
    # user_id=1234567

    data = request.get_json()
    project = Project(
        projectName=data["name"],
        client=data["client"],
        # skills = json.loads(data["skills"]),
        skills=json.dumps(data["skills"]),
        knowledge=json.dumps(data["knowledge"]),
        thumbnail=data["thumbnail"],
        scope=data["scope"],
        topics=json.dumps(data["topics"]),
        requirements=data["requirements"],
        outcomes=data["outcomes"],
        creatorZId=user_id,
    )
    db.session.add(project)
    db.session.commit()
    return jsonify({"message": "Project created successfully"}), 200


@projects.route("/projects/groupCreate/<projectId>", methods=["POST"])
@jwt_required()
def create_group_project(projectId):
    """
    Creates a group for the project with id of projectId and adds the user to as a member
    of the created group

    Request:
    - Method: POST
    - Content-Type: application/json
    - Body:
        {
        groupName: "Group number one"
        }

    Returns:
    JSON: A JSON response indicating the success of the group creation.
    """

    user_id = get_jwt_identity()
    data = request.get_json()

    all_members = get_all_members_for_project(projectId)

    if user_id in all_members:
        return jsonify({"error": "User already in a group"}), 400

    # create new group
    group = Group(groupName=data["groupName"], project=projectId)

    # Add the group to the db first before getting groupID
    db.session.add(group)
    db.session.commit()

    # add user to current group as a group member
    group_member = GroupMember(groupID=group.ID, student=user_id)

    # save to db
    db.session.add(group_member)
    db.session.commit()

    return jsonify({"message": "Group created"}), 200


def get_all_members_for_project(project_id):
    """
    Gets the zID of all students in the current project
    """
    members = GroupMember.query.join(Group).filter(Group.project == project_id).all()
    member_ids = [member.student for member in members]

    return member_ids


@projects.route("/projects/join/<projectId>/<groupId>", methods=["PUT"])
@jwt_required()
def join_group_project(projectId, groupId):
    """
    Adds the current user to the group with id groupId for the project with id projectId
    """

    # check if the project has the group
    project = Project.query.filter_by(ID=projectId).first()
    if project is None:
        return jsonify({"error": "Project does not exist"}), 400

    # check if the group exists
    group = Group.query.filter_by(ID=groupId, project=projectId).first()
    if group is None:
        return jsonify({"error": "Group does not exist"}), 400

    user_id = get_jwt_identity()
    # check if user already in group
    group_member = GroupMember.query.filter_by(groupID=groupId, student=user_id).first()

    if group_member is not None:
        return jsonify({"error": "User already in group"}), 400

    all_members = get_all_members_for_project(projectId)

    if user_id in all_members:
        return jsonify({"error": "User already in a group"}), 400

    # create new member
    group_member = GroupMember(groupID=groupId, student=user_id)
    db.session.add(group_member)
    db.session.commit()
    return jsonify({"message": "User added to group"}), 200
