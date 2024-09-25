import * as React from "react";
import { useState } from "react";
import SubmitButton from "./SubmitButton";
import Alert from "@mui/material/Alert";
import { hasEmptyValue } from "../helpers/helper";
import EditTextField from "./EditTextField";

function AddCourseUrlForm(props) {
  const [courseData, setCourseData] = useState({ url: "" });
  const [error, setError] = useState({ error: "" });

  const handleSubmit = (event) => {
    event.preventDefault();
    const error = hasEmptyValue(courseData);
    if (error) {
      setError({ error });
    } else {
      proccessRequest();
    }
  };

  async function proccessRequest() {
    const response = await props.onSubmit(courseData);
    setError({ error: response.error ? "Invalid UNSW course outline URL" : "" });
  }

  const inputChange = (event) => {
    const { name, value } = event.target;
    setCourseData({ ...courseData, [name]: value });
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
            <h1>{"Create your new Course"} </h1>
          </div>
          <EditTextField
            value={courseData.code}
            onChange={inputChange}
            name="url"
            label="Course URL"
            helperText="Enter the url of your course's details"
          />
          {errorMessageCard()}
          <SubmitButton onClick={handleSubmit} label="Add Course" />
        </form>
      </div>
    </>
  );
}

export default AddCourseUrlForm;
