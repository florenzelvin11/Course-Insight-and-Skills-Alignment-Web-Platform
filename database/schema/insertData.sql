USE uni;

INSERT INTO tblSchool(schoolName) 
VALUES 
('Australian Graduate School of Management'),
('School of Accounting, Auditing and Taxation'),
('School of Banking and Finance'),
('School of Economics'),
('School of Information Systems and Technology Management'),
('School of Management and Governance'),
('School of Marketing'),
('UNSW Business School'),
('School of Risk and Actuarial Studies'),
('Graduate School of Biomedical Engineering'),
('School of Chemical Engineering'),
('School of Civil and Environmental Engineering'),
('School of Computer Science and Engineering'),
('School of Electrical Engineering and Telecommunications'),
('School of Mechanical and Manufacturing Engineering'),
('School of Minerals and Energy Resources Engineering'),
('School of Photovoltaic and Renewable Energy Engineering'),
('School of Art and Design'),
('School of the Arts and Media'),
('School of Built Environment'),
('School of Social Sciences'),
('School of Humanities and Languages'),
('School of Education'),
('School of Law, Society and Criminology'),
('School of Global and Public Law'),
('School of Private and Commercial Law'),
('School of Clinical Medicine'),
('School of Population Health'),
('School of Health Sciences'),
('School of Optometry and Vision Science'),
('School of Biomedical Sciences'),
('School of Aviation'),
('School of Biological, Earth and Environmental Sciences'),
('School of Biotechnology and Biomolecular Sciences'),
('School of Chemistry'),
('School of Materials Science and Engineering'),
('School of Mathematics and Statistics'),
('School of Physics'),
('School of Psychology');

-- INSERT INTO tblProgram(ID, programName, managingSchool) 
-- VALUES (3132,'Materials Science and Engineering (Honours) / Engineering Science','Arts, Design and Architecture'),
-- (3778,'Computer Science','Engineering');

-- INSERT INTO tblMajor(ID, majorName, program) 
-- VALUES ('COMPA1','Default', 3778),
-- ('COMPD1','Database Systems', 3778),
-- ('COMPE1','eCommerce Systems', 3778),
-- ('COMPS1','Embedded Systems', 3778),
-- ('COMPJ1','Programming Langauges', 3778),
-- ('COMPI1','Artificial Intelligence', 3778),
-- ('COMPN1','Computer Networks', 3778),
-- ('COMPY1','Security Engineering', 3778);

-- INSERT INTO tblCourse(courseCode, yearDate, term) 
-- VALUES ('COMP3900', 2021, 'T2'),
-- ('COMP3900', 2020, 'T2');

-- INSERT INTO tblCourseArchive(courseCode, yearDate, term, revision) 
-- VALUES ('COMP3900',2020, 'T2', '2020-01-01 15:10:11');

-- -- INSERT INTO tblPermissions(permissionName, permissionDescription) 
-- -- VALUES ('login','Able to login');

-- INSERT INTO tblUserRole(userRoleName)
-- VALUES ('Admin'),
-- ('Student');

-- -- INSERT INTO tblRolePermission(userRole, permission)
-- -- VALUES (1,1);

INSERT INTO tblUser(firstname, lastname, zID, email, dob, enPassword, contactNumber, metadataJson, verified) 
VALUES ('C', 'D', 5319978, 'banana@gmail.com', '2000-07-13', 'b493d48364afe44d11c0165cf470a4164d1e2609911ef998be868d46ade3de4e', 61123456789,
'{
  "class": {
    "admin": {},
    "academic": {
      "type": "academic",
      "school": "Engineering",
      "skills":{},
      "knowledge":{}
    },
    "student": {
        "major": "null",
        "program": "null",
        "transcript": "null",
        "skills": {},
        "knowledge":{},
        "jobExperience": {}
    }
  }
}', 1);

INSERT INTO tblUser(firstname, lastname, zID, email, dob, enPassword, contactNumber, metadataJson, verified) 
VALUES ('Sammi', 'A', 5255997, 'z5255997@unsw.edu.au', '2000-12-12', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 61495833859,
'{
  "class": {
    "academic": {
      "type": "casual academic",
      "school": "Engineering",
      "skills":{},
      "knowledge":{}
    },
    "student": {
        "skills": {
          "operate": 9,
          "problem solving": 18,
          "communication": 27,
          "adaptability": 18,
          "resilience": 27
      },
        "knowledge": {
          "level high": 6,
          "robotics": 6,
          "general programming": 12,
          "unix": 6,
          "programming language": 6,
          "flow control": 6,
          "compiler c": 6,
          "genome": 6,
          "programming concept": 6,
          "mechanics": 6,
          "programs computer": 6,
          "design program": 6,
          "computer system": 6,
          "list link": 6,
          "arrays": 6
      }
    }
  }
}', 1);


-- INSERT INTO tblProject(projectName, client, creatorZId, skills, knowledge, scope, requirements, topics) 
-- VALUES ("Fitness Tracker", "Jane Doe", 5319978, '{
--           "operate": 9,
--           "problem solving": 18,
--           "communication": 27,
--           "adaptability": 18,
--           "critical thinking": 9,
--           "resilience": 18
--       }', '{
--           "level high": 6,
--           "robotics": 6,
--           "general programming": 6,
--           "translate": 6,
--           "unix": 6,
--           "programming language": 6,
--           "flow control": 6,
--           "compiler c": 6,
--           "genome": 6,
--           "programming concept": 6,
--           "mechanics": 6,
--           "programs computer": 6,
--           "design program": 6,
--           "computer system": 6,
--           "list link": 6,
--           "arrays": 6
--       }', "Completes this within 5 weeks", "Completed comp1511", '["topic 1", "topic 2"]'
--       );

-- INSERT INTO tblAcademic(zID, school, academicType) 
-- VALUES (5319978, 'Engineering', 'banana');

-- -- INSERT INTO tblCourse(ID, courseName, courseDescription)
-- -- VALUES ('COMP3900', 'Computer Science Project', 
-- -- 'A capstone software project. Students work in teams to define, implement 
-- -- and evaluate a real-world software system. Most of the work in this course 
-- -- is team-based project work, although there are some introductory lectures on 
-- -- software project management and teamwork strategies. Project teams meet fortnightly
-- -- with project mentors to report on the progress of the project. Assessment is based on a 
-- -- project proposal, a final project demonstration and report, and on the quality of the 
-- -- software system itself. Students are also required to reflect on their work and to
-- --  provide peer assessment of their team-mates\' contributions to the project.')