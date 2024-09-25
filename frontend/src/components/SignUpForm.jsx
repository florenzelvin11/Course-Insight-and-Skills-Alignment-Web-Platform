import * as React from "react";
import { useState } from "react";
import { generalErrorMessage } from "../constants/constants";
import SubmitButton from "./SubmitButton";
import AuthTextField from "./AuthTextField";
import { isValidSignUpData } from "../helpers/helper";
import Alert from "@mui/material/Alert";

function SignUpForm(props) {
  const [signUpData, setSignUpData] = useState({
    zId: "",
    firstName: "",
    lastName: "",
    email: "",
    password: "",
  });
  const [error, setError] = useState({ error: "" });

  const handleSubmit = (event) => {
    event.preventDefault();
    const error = isValidSignUpData(signUpData);
    if (error) {
      setError({ error });
    } else {
      proccessRequest();
    }
  };

  async function proccessRequest() {
    const response = await props.onSubmit(signUpData);
    setError({ error: response.error ? generalErrorMessage : "" });
  }

  const inputChange = (event) => {
    const { name, value } = event.target;
    setSignUpData({ ...signUpData, [name]: value });
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
            <h1>Sign up</h1>
          </div>
          <AuthTextField onChange={inputChange} name="zId" label="zID" />
          <AuthTextField
            onChange={inputChange}
            name="firstName"
            label="First Name"
          />
          <AuthTextField
            onChange={inputChange}
            name="lastName"
            label="Last Name"
          />
          <AuthTextField onChange={inputChange} name="email" label="Email" />
          <AuthTextField
            type="password"
            onChange={inputChange}
            name="password"
            label="Password"
          />
          <AuthTextField
            type="password"
            onChange={inputChange}
            name="confirmedPassword"
            label="Confirm Password"
          />
          {errorMessageCard()}
          <SubmitButton onClick={handleSubmit} label="Sign up" />
        </form>
      </div>
    </>
  );
}

export default SignUpForm;
