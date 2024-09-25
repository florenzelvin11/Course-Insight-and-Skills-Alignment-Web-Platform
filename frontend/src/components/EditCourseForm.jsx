import * as React from "react";
import { useState, useEffect } from "react";
import { generalErrorMessage, termOptions } from "../constants/constants";
import SubmitButton from "./SubmitButton";
import Alert from "@mui/material/Alert";
import { useParams } from "react-router-dom";
import AddSkill from "./AddSkill";
import { objectToArray, validateCourseData } from "../helpers/helper";
import EditTextField from "./EditTextField";
import AddTopic from "./AddTopic";
import DropDownInput from "./DropDownInput";

function EditCourseForm(props) {
  const params = useParams();
  const [courseData, setCourseData] = useState({
    name: "",
    code: "",
    year: "",
    term: "",
    thumbnail: "",
    school: "",
    topics: [],
    description: "",
    skills: [],
    knowledge: [],
    currentVersion: "",
    availableVersions: [],
  });

  const [topics, setTopics] = useState([]);
  const [skills, setSkills] = useState([{ name: "", weight: "" }]);
  const [knowledge, setKnowledge] = useState([{ name: "", weight: "" }]);
  const [error, setError] = useState({ error: "" });

  const handleSkillChange = (updatedSkills) => {
    setCourseData({ ...courseData, [skills]: updatedSkills });
    setSkills(updatedSkills);
  };

  const handleKnowledgeChange = (updatedKnowledge) => {
    setKnowledge(updatedKnowledge);
  };

  const handleTopicChange = (updatedTopics) => {
    setTopics(updatedTopics);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const error = validateCourseData(courseData, skills, knowledge, topics);
    if (error) {
      setError({ error });
    } else {
      proccessRequest();
    }
  };

  async function proccessRequest() {
    const response = await props.onSubmit({
      ...courseData,
      skills,
      knowledge,
      topics,
    });
    setError({ error: response.error ? generalErrorMessage : "" });
  }

  const inputChange = (event) => {
    const { name, value } = event.target;
    setCourseData({ ...courseData, [name]: value });
  };

  useEffect(() => {
    const setupCourseData = async () => {
      if (props.courseData) {
        setCourseData({
          name: props.courseData.name,
          code: props.courseData.code,
          year: props.courseData.currentYear,
          term: props.courseData.currentTerm,
          thumbnail: props.courseData.thumbnail,
          topics: props.courseData.topics,
          description: props.courseData.description,
          skills: objectToArray(props.courseData.skills),
          knowledge: objectToArray(props.courseData.knowledge),
          currentVersion: props.courseData.currentVersion,
          availableVersions: props.courseData.availableVersions,
        });
        if (props.courseData.topics) {
          setTopics(props.courseData.topics);
        }
        if (props.courseData.skills) {
          setSkills(objectToArray(props.courseData.skills));
        }
        if (props.courseData.knowledge) {
          setKnowledge(objectToArray(props.courseData.knowledge));
        }
      }
    };

    setupCourseData();
  }, [props.courseData]);

  function errorMessageCard() {
    return (
      <div className="error-card">
        {error.error !== "" && (
          <Alert sx={{ width: "100%", mb: 1 }} severity="error">
            {error.error}
          </Alert>
        )}
      </div>
    );
  }

  return (
    <>
      <div className="central-card">
        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="auth-heading">
            <h1>{`Edit ${params.courseCode}`} </h1>
          </div>
          <EditTextField
            value={courseData.name}
            onChange={inputChange}
            name="name"
            label="Name"
          />
          <EditTextField
            value={courseData.year}
            onChange={inputChange}
            name="year"
            label="Year"
            type="number"
          />
          <DropDownInput
            onChange={inputChange}
            selectedOption={courseData.term}
            menuItems={termOptions}
            name="term"
            label="Term"
          />
          <EditTextField
            value={courseData.description}
            onChange={inputChange}
            name="description"
            label="Description"
            multiline
            rows={4}
          />
          <EditTextField
            value={courseData.thumbnail}
            onChange={inputChange}
            name="thumbnail"
            label="Thumbnail"
          />
          <AddTopic
            label="Topics"
            name="topics"
            topics={topics}
            onTopicChange={handleTopicChange}
          />
          <AddSkill
            label="Skills"
            name="skills"
            skills={skills}
            onSkillChange={handleSkillChange}
          />
          <AddSkill
            label="Knowledge"
            name="knowledge"
            skills={knowledge}
            onSkillChange={handleKnowledgeChange}
          />
          {errorMessageCard()}
          <SubmitButton onClick={handleSubmit} label="Edit Course" />
        </form>
      </div>
    </>
  );
}

export default EditCourseForm;
