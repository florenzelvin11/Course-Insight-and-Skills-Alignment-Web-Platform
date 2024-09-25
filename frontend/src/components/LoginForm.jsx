import * as React from "react";
import SubmitButton from "./SubmitButton";
import AuthTextField from "./AuthTextField";
import { useState } from "react";
import Alert from "@mui/material/Alert";
import { isValidLoginData } from "../helpers/helper";

function LoginForm(props) {
  const [loginData, setloginData] = useState({ email: "", password: "" });
  const [error, setError] = useState({ error: "" });

  const handleSubmit = (event) => {
    event.preventDefault();
    const error = isValidLoginData(loginData);
    if (error) {
      setError({ error });
    } else {
      proccessRequest();
    }
  };

  async function proccessRequest() {
    const response = await props.onSubmit(loginData);
    setError({ error: response.error ? "Incorrect email or passsword" : "" });
  }

  const inputChange = (event) => {
    const { name, value } = event.target;
    setloginData({ ...loginData, [name]: value });
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
            <h1>Login</h1>
          </div>
          <AuthTextField onChange={inputChange} name="email" label="Email" />
          <AuthTextField
            type="password"
            onChange={inputChange}
            name="password"
            label="Password"
          />
          {errorMessageCard()}
          <SubmitButton onClick={handleSubmit} label="Login" />
        </form>
      </div>
    </>
  );
}

export default LoginForm;
