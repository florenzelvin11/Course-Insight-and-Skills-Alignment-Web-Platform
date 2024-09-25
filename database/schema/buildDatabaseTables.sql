CREATE DATABASE uni;
USE uni;

-- Creation of roles and permissions
-- CREATE TABLE tblUserRole(
--   ID INT AUTO_INCREMENT, 
--   userRoleName NVARCHAR(128) UNIQUE,
--   PRIMARY KEY (ID)
-- );

-- CREATE TABLE tblPermissions( 
--   ID INT AUTO_INCREMENT,
--   permissionName NVARCHAR(30) UNIQUE,
--   permissionDescription TEXT,
--   PRIMARY KEY (ID)
-- );

-- CREATE TABLE tblRolePermission(
--   userRole INT, 
--   permission INT,
--   PRIMARY KEY (userRole, permission),
--   FOREIGN KEY (userRole) REFERENCES tblUserRole(ID),
--   FOREIGN KEY (permission) REFERENCES tblPermissions(ID)
-- );
-- -- End of creation of roles and permissions 

-- Creation of schools, degrees and majors
CREATE TABLE tblSchool(
  schoolName VARCHAR(255),
  PRIMARY KEY (schoolName)
);

CREATE TABLE tblProgram(
  ID INT,
  programName VARCHAR(255),
  managingSchool VARCHAR(255),
  PRIMARY KEY (ID),
  FOREIGN KEY (managingSchool) REFERENCES tblSchool(schoolName)
);

CREATE TABLE tblMajor(
  ID VARCHAR(6),
  majorName VARCHAR(255),
  program INT,
  PRIMARY KEY (ID),
  FOREIGN KEY (program) REFERENCES tblProgram(ID)
);
-- End of Creation of schools, degrees and majors

-- Creation of users and different types of users 
-- Admins will be marked as admin userRole type
CREATE TABLE tblUser(
    firstname VARCHAR(100),
    lastname VARCHAR(100),
    zID INT(7),
    email VARCHAR(255),
    dob DATE,
    enPassword VARCHAR(255),
    contactNumber BIGINT(11),
    metadataJson TEXT,
    verified BIT(1), 
    summary NVARCHAR(255),
    headline NVARCHAR(255),
    imageURL TEXT,
    privacy BIT(1),
    PRIMARY KEY (zID)
);

CREATE TABLE tblUserCode(
  code VARCHAR(6),
  user INT(7),
  PRIMARY KEY (code),
  FOREIGN KEY (user) REFERENCES tblUser(zID)
);

-- CREATE TABLE tblAcademic(
--     ID INT AUTO_INCREMENT,
--     zID INT(7),
--     school VARCHAR(255),
--     academicType VARCHAR(30),
--     PRIMARY KEY (ID),
--     FOREIGN KEY (zID) REFERENCES tblUser(zID),
--     FOREIGN KEY (school) REFERENCES tblSchool(schoolName)
-- );

-- CREATE TABLE tblStudent(
--   zID INT(7),
--   transcript VARCHAR(255),
--   program INT,
--   major VARCHAR(7),
--   PRIMARY KEY (zID),
--   FOREIGN KEY (program) REFERENCES tblProgram(ID),
--   FOREIGN KEY (major) REFERENCES tblMajor(ID),
--   FOREIGN KEY (zID) REFERENCES tblUser(zID)
-- );
-- End of creation of users and different types of users 

-- Create courses and projects
CREATE TABLE tblCourse(
  ID INT AUTO_INCREMENT,
  courseCode VARCHAR(8),
  courseName VARCHAR(255),
  courseDescription TEXT,
  courseSkills TEXT,
  courseKnowledge TEXT,
  topics TEXT,
  yearDate INT(4),
  term VARCHAR(25),
  revision DATETIME,
  school VARCHAR(255),
  thumbnail TEXT,
  PRIMARY KEY (ID),
  FOREIGN KEY (school) REFERENCES tblSchool(schoolName),
  CONSTRAINT unique_course_revision UNIQUE (courseCode, yearDate, term)
);

CREATE TABLE tblCourseArchive(
  ID INT AUTO_INCREMENT,
  courseID INT,
  courseCode VARCHAR(8),
  courseName VARCHAR(255),
  courseDescription TEXT,
  courseSkills TEXT,
  courseKnowledge TEXT,
  topics TEXT,
  yearDate INT(4),
  term VARCHAR(25),
  revision DATETIME,
  school VARCHAR(255),
  thumbnail TEXT,
  PRIMARY KEY (ID),
  FOREIGN KEY (courseID) REFERENCES tblCourse(ID),
  FOREIGN KEY (school) REFERENCES tblSchool(schoolName),
  CONSTRAINT unique_course_revision UNIQUE (courseCode, yearDate, term, revision)
);

CREATE TABLE tblProject(
  ID INT AUTO_INCREMENT,
  course INT,
  projectName TEXT,
  client TEXT,
  creatorZId INT(7),
  skills TEXT,
  knowledge TEXT,
  thumbnail TEXT,
  scope TEXT,
  requirements TEXT,
  topics TEXT,
  outcomes TEXT,
  FOREIGN KEY (course) REFERENCES tblCourse(ID),
  PRIMARY KEY (ID)
);

-- CREATE TABLE tblProjectArchive(
--   ID INT AUTO_INCREMENT,
--   revision INT,
--   course VARCHAR(8),
--   projectName VARCHAR(255),
--   projectScope TEXT,
--   learningOutcomes TEXT,
--   FOREIGN KEY (projectID) REFERENCES tblProject(ID),
--   FOREIGN KEY (course) REFERENCES tblCourse(ID),
--   PRIMARY KEY (ID, revision)
-- );
-- -- End of courses and projects

-- -- Creation of skills and knowledge 
-- CREATE TABLE tblSkills(
--   ID INT AUTO_INCREMENT,
--   skillName VARCHAR(128),
--   PRIMARY KEY (ID)
-- );

-- CREATE TABLE tblKnowledge(
--   ID INT AUTO_INCREMENT,
--   knowledgeName VARCHAR(128),
--   PRIMARY KEY (ID)
-- );
-- -- End of creation of skills and knowledge 

CREATE TABLE tblCourseRole(
  ID INT AUTO_INCREMENT,
  courseRoleName VARCHAR(255),
  courseRoleDescription TEXT,
  coursePermissions INT,
  PRIMARY KEY (ID)
);

-- Creation of the relation between course/projects to user
CREATE TABLE tblCourseEnrolment(
  ID INT AUTO_INCREMENT,
  course INT,
  user INT(7),
  courseRole VARCHAR(255),
  PRIMARY KEY (ID),
  FOREIGN KEY (course) REFERENCES tblCourse(ID),
  FOREIGN KEY (user) REFERENCES tblUser(zID)
);

-- CREATE TABLE tblUserProject(
--   ID INT AUTO_INCREMENT,
--   project INT,
--   user INT(7),
--   PRIMARY KEY (ID), 
--   FOREIGN KEY (project) REFERENCES tblProject(ID),
--   FOREIGN KEY (user) REFERENCES tblUser(zID)
-- );
-- -- End of creation of the relation between course/projects to user

-- Creation of groups 
CREATE TABLE tblGroup(
  ID INT AUTO_INCREMENT,
  groupName VARCHAR(255),
  project INT,
  PRIMARY KEY (ID),
  FOREIGN KEY (project) REFERENCES tblProject(ID)
);
-- End of creation of groups

-- Creation of relations groups and users
CREATE TABLE tblGroupMember(
  ID INT AUTO_INCREMENT,
  groupID INT,
  student INT(7),
  PRIMARY KEY (ID),
  FOREIGN KEY (groupID) REFERENCES tblGroup(ID),
  FOREIGN KEY (student) REFERENCES tblUser(zID)
);
-- End of creation of groups and users

-- -- Creation of courses' gained skills and knowledge
-- CREATE TABLE tblCourseSkill(
--   ID INT AUTO_INCREMENT,
--   skill INT, 
--   course VARCHAR(8),
--   PRIMARY KEY (ID), 
--   FOREIGN KEY (skill) REFERENCES tblSkills(ID),
--   FOREIGN KEY (course) REFERENCES tblCourse(ID)
-- );

-- CREATE TABLE tblCourseKnowledge(
--   ID INT AUTO_INCREMENT,
--   knowledge INT, 
--   course VARCHAR(8),
--   PRIMARY KEY (ID), 
--   FOREIGN KEY (knowledge) REFERENCES tblKnowledge(ID),
--   FOREIGN KEY (course) REFERENCES tblCourse(ID)
-- );
-- -- End of creation of courses' gained skills and knowledge

-- -- Creation of projects' required skills, knowledge and courses
-- CREATE TABLE tblProjectSkill(
--   ID INT AUTO_INCREMENT,
--   skill INT, 
--   project INT,
--   PRIMARY KEY (ID), 
--   FOREIGN KEY (skill) REFERENCES tblSkills(ID),
--   FOREIGN KEY (project) REFERENCES tblProject(ID)
-- );

-- CREATE TABLE tblProjectKnowledge(
--   ID INT AUTO_INCREMENT,
--   knowledge INT, 
--   project INT,
--   PRIMARY KEY (ID), 
--   FOREIGN KEY (knowledge) REFERENCES tblKnowledge(ID),
--   FOREIGN KEY (project) REFERENCES tblProject(ID)
-- );

-- CREATE TABLE tblProjectCourseRequired(
--   ID INT AUTO_INCREMENT,
--   course VARCHAR(8), 
--   project INT,
--   PRIMARY KEY (ID), 
--   FOREIGN KEY (course) REFERENCES tblCourse(ID),
--   FOREIGN KEY (project) REFERENCES tblProject(ID)
-- );
-- -- End of creation of projects' required skills, knowledge and courses