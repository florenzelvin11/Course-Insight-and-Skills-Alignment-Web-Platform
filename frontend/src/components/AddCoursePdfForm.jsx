import * as React from "react";
import { useState } from "react";
import PdfUploader from "./PdfUploader";
import Alert from "@mui/material/Alert";

function AddCoursePdfForm(props) {
  const [error, setError] = useState({ error: "" });

  const onSubmit = async (dataURL) => {
    const response = await props.onSubmit(dataURL);
    setError({ error: response.error ? "Invalid UNSW course outline PDF" : "" });
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
        <form className="auth-form">
          <div className="auth-heading">
            <h1>{"Upload the PDF for your new Course"} </h1>
          </div>
          <PdfUploader onSubmit={onSubmit} />
          {errorMessageCard()}
        </form>
      </div>
    </>
  );
}

export default AddCoursePdfForm;
