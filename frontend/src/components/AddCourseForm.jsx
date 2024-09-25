import * as React from 'react';
import { useState } from 'react';
import { generalErrorMessage, schoolOptions, termOptions, } from '../constants/constants'
import SubmitButton from './SubmitButton';
import Alert from '@mui/material/Alert';
import AddSkill from './AddSkill';
import { validateCourseData } from '../helpers/helper';
import EditTextField from './EditTextField';
import AddTopic from './AddTopic';
import DropDownInput from './DropDownInput';

function AddCourseForm (props) {
  const [courseData, setCourseData] = useState({
    name: '',
    code: '',
    year: '',
    term: '',
    school: '',
    thumbnail: '',
    topics: [],
    description: '',
    skills: [],
    knowledge: [], 
  });

  const [topics, setTopics] = useState([]);
  const [skills, setSkills] = useState([{ name: '', weight: '' }]);
  const [knowledge, setKnowledge] = useState([{ name: '', weight: '' }]);
  const [error, setError] = useState({error: ''});

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
  }

  async function proccessRequest() {
      const response = await props.onSubmit({...courseData, skills, knowledge, topics});
      setError({ error: response.error ? generalErrorMessage : '' });
  }
  
  const inputChange = (event) => {
    const { name, value } = event.target;  
    setCourseData({ ...courseData, [name]: value });
  };

  function errorMessageCard() {
    return (
      <div className="error-card">
        {error.error !== '' && <Alert sx={{ width: '100%', mb: 1}} severity="error">{error.error}</Alert>}
      </div>
    );
  }

  return (
  <>
    <div className="central-card">
      <form className="auth-form" onSubmit={handleSubmit}>
        <div className="auth-heading">
          <h1>{'Create your new Course'} </h1>
        </div>
        <EditTextField value={courseData.code} onChange={inputChange} name="code" label="Code" helperText="Enter code in the form COMPXXXX"/>
        <EditTextField value={courseData.name} onChange={inputChange} name="name" label="Name"/>
        <EditTextField value={courseData.year} onChange={inputChange} name="year" label="Year"/>
        <DropDownInput onChange={inputChange} selectedOption={courseData.term} menuItems={termOptions} name="term" label="Term"/>
        <EditTextField value={courseData.thumbnail} onChange={inputChange} name="thumbnail" label="Thumbnail"/>
        <EditTextField value={courseData.description} onChange={inputChange} name="description" label="Description" multiline rows={4}/>
        <DropDownInput onChange={inputChange} selectedOption={courseData.school} menuItems={schoolOptions} name="school" label="School"/>
        <AddTopic label="Topics" name="topics" topics={topics} onTopicChange={handleTopicChange}/>
        <AddSkill label="Skills" name="skills" skills={skills} onSkillChange={handleSkillChange}/>
        <AddSkill label="Knowledge" name="knowledge" skills={knowledge} onSkillChange={handleKnowledgeChange}/>
        {errorMessageCard()}
        <SubmitButton onClick={handleSubmit} label="Add Course"/>
      </form>
    </div>
  </>
  );
}

export default AddCourseForm;