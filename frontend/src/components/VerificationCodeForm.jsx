import * as React from "react";
import Alert from "@mui/material/Alert";

function VerificationCodeForm(props) {
  function errorMessageCard() {
    return (
      <div className="error-card">
        {props.error !== "" && (
          <Alert sx={{ width: "100%", mb: 1 }} severity="error">
            {props.error}
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
            <h1>Verifying your account</h1>
            <h4>Please check your email</h4>
          </div>
          {errorMessageCard()}
        </form>
      </div>
    </>
  );
}

export default VerificationCodeForm;
