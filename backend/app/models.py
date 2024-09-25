from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# School
class School(db.Model):
    __tablename__ = "tblSchool"

    schoolName = db.Column(db.String(255), primary_key=True)


# Program
class Program(db.Model):
    __tablename__ = "tblProgram"

    ID = db.Column(db.Integer, primary_key=True)
    programName = db.Column(db.String(255))
    managingSchool = db.Column(db.String(255), db.ForeignKey("tblSchool.schoolName"))


# Major
class Major(db.Model):
    __tablename__ = "tblMajor"

    ID = db.Column(db.String(6), primary_key=True)
    majorName = db.Column(db.String(255))
    program = db.Column(db.Integer, db.ForeignKey("tblProgram.ID"))


# User
class User(db.Model):
    __tablename__ = "tblUser"

    zID = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(255))
    dob = db.Column(db.Date)
    enPassword = db.Column(db.String(255))
    contactNumber = db.Column(db.BigInteger)
    metadataJson = db.Column(db.Text)
    verified = db.Column(db.Integer)
    summary = db.Column(db.String(255))
    headline = db.Column(db.String(255))
    imageURL = db.Column(db.Text)
    privacy = db.Column(db.Integer)


# User Codes
class UserCode(db.Model):
    __tablename__ = "tblUserCode"

    code = db.Column(db.String(6))
    user = db.Column(db.Integer, primary_key=True)


# Course
class Course(db.Model):
    __tablename__ = "tblCourse"

    ID = db.Column(db.Integer, primary_key=True)
    courseCode = db.Column(db.String(8))
    courseName = db.Column(db.String(255))
    courseDescription = db.Column(db.Text)
    courseSkills = db.Column(db.Text)
    courseKnowledge = db.Column(db.Text)
    topics = db.Column(db.Text)
    yearDate = db.Column(db.Integer)
    term = db.Column(db.String(255))
    revision = db.Column(db.DateTime)
    thumbnail = db.Column(db.Text)
    school = db.Column(db.String(255), db.ForeignKey("tblSchool.schoolName"))


class CourseArchive(db.Model):
    __tablename__ = "tblCourseArchive"

    ID = db.Column(db.Integer, primary_key=True)
    courseID = db.Column(db.Integer, db.ForeignKey("tblCourse.ID"))
    courseCode = db.Column(db.String(8))
    courseName = db.Column(db.String(255))
    courseDescription = db.Column(db.Text)
    courseSkills = db.Column(db.Text)
    courseKnowledge = db.Column(db.Text)
    topics = db.Column(db.Text)
    yearDate = db.Column(db.Integer)
    term = db.Column(db.String(255))
    revision = db.Column(db.DateTime)
    thumbnail = db.Column(db.Text)
    school = db.Column(db.String(255), db.ForeignKey("tblSchool.schoolName"))


# Course Role
class CourseRole(db.Model):
    __tablename__ = "tblCourseRole"

    ID = db.Column(db.Integer, primary_key=True)
    courseRoleDescription = db.Column(db.Text)
    coursePermissions = db.Column(db.Integer)


# # Course Enrolment
class CourseEnrolment(db.Model):
    __tablename__ = "tblCourseEnrolment"
    ID = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.Integer, db.ForeignKey("tblCourse.ID"))
    user = db.Column(db.Integer, db.ForeignKey("tblUser.zID"))
    courseRole = db.Column(db.String(255))


class Project(db.Model):
    __tablename__ = "tblProject"
    ID = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.Integer, db.ForeignKey("tblCourse.ID"))
    projectName = db.Column(db.String(255))
    client = db.Column(db.Text)
    creatorZId = db.Column(db.Integer, db.ForeignKey("tblUser.zID"))
    skills = db.Column(db.Text)
    knowledge = db.Column(db.Text)
    thumbnail = db.Column(db.Text)
    scope = db.Column(db.Text)
    requirements = db.Column(db.Text)
    topics = db.Column(db.Text)
    outcomes = db.Column(db.Text)


# Group
class Group(db.Model):
    __tablename__ = "tblGroup"

    ID = db.Column(db.Integer, primary_key=True)
    groupName = db.Column(db.String(255))
    project = db.Column(db.Integer, db.ForeignKey("tblProject.ID"))


# Group Member
class GroupMember(db.Model):
    __tablename__ = "tblGroupMember"

    ID = db.Column(db.Integer, primary_key=True)
    groupID = db.Column(db.Integer, db.ForeignKey("tblGroup.ID"))
    student = db.Column(db.Integer, db.ForeignKey("tblUser.zID"))
