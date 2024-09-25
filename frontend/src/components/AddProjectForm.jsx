import * as React from "react";
import { useState } from "react";
import { generalErrorMessage } from "../constants/constants";
import SubmitButton from "./SubmitButton";
import Alert from "@mui/material/Alert";
import AddSkill from "./AddSkill";
import EditTextField from "./EditTextField";
import AddTopic from "./AddTopic";
import { validateProjectData } from "../helpers/helper";

function AddProjectForm(props) {
  const [projectData, setProjectData] = useState({
    name: "",
    client: "",
    skills: "",
    knowledge: "",
    thumbnail: "",
    requirements: "",
    scope: "",
    topics: [],
    outcomes: "",
  });
  const [topics, setTopics] = useState([]);
  const [skills, setSkills] = useState([{ name: "", weight: "" }]);
  const [knowledge, setKnowledge] = useState([{ name: "", weight: "" }]);
  const [error, setError] = useState({ error: "" });

  const handleSkillChange = (updatedSkills) => {
    setProjectData({ ...projectData, [skills]: updatedSkills });
    setSkills(updatedSkills);
  };

  const handleKnowledgeChange = (updatedKnowledge) => {
    setProjectData({ ...projectData, [knowledge]: updatedKnowledge });
    setKnowledge(updatedKnowledge);
  };

  const handleTopicChange = (updatedTopics) => {
    setTopics(updatedTopics);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const error = validateProjectData(
      { ...projectData, skills, knowledge, topics },
      skills,
      knowledge,
      topics
    );
    if (error) {
      setError({ error });
    } else {
      proccessRequest();
    }
  };

  async function proccessRequest() {
    const response = await props.onSubmit({
      ...projectData,
      skills,
      knowledge,
      topics,
    });
    setError({ error: response.error ? generalErrorMessage : "" });
  }

  const inputChange = (event) => {
    const { name, value } = event.target;
    setProjectData({ ...projectData, [name]: value });
  };

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
            <h1>{"Create your new project"} </h1>
          </div>
          <EditTextField
            value={projectData.name}
            onChange={inputChange}
            name="name"
            label="Name"
          />
          <EditTextField
            value={projectData.client}
            onChange={inputChange}
            name="client"
            label="Client Name"
          />
          <EditTextField
            value={projectData.thumbnail}
            onChange={inputChange}
            name="thumbnail"
            label="Thumbnail"
          />
          <EditTextField
            value={projectData.scope}
            onChange={inputChange}
            name="scope"
            label="Scope"
            multiline
            rows={4}
          />
          <EditTextField
            value={projectData.requirements}
            onChange={inputChange}
            name="requirements"
            label="Requirements"
            multiline
            rows={4}
          />
          <EditTextField
            value={projectData.outcomes}
            onChange={inputChange}
            name="outcomes"
            label="Outcomes"
            multiline
            rows={4}
          />
          <AddTopic
            label="Topics"
            name="topics"
            topics={topics}
            onTopicChange={handleTopicChange}
          />
          <AddSkill
            label="Skills Required"
            name="skills"
            skills={skills}
            onSkillChange={handleSkillChange}
          />
          <AddSkill
            label="Knowledge Required"
            name="knowledge"
            skills={knowledge}
            onSkillChange={handleKnowledgeChange}
          />
          {errorMessageCard()}
          <SubmitButton onClick={handleSubmit} label="Add Project" />
        </form>
      </div>
    </>
  );
}

export default AddProjectForm;
