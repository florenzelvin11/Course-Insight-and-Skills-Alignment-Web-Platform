import * as React from "react";
import SignUpForm from "../components/SignUpForm";
import AuthNavBar from "../components/AuthNavBar";
import { apiCall, setUserData } from "../helpers/helper";
import { useNavigate } from "react-router-dom";

function SignUpPage() {
  const navigate = useNavigate();

  function navigateToVerifyAccount() {
    navigate("/verify-account");
  }

  async function onSubmit(userData) {
    const requestData = {
      zId: userData.zId,
      firstName: userData.firstName,
      lastName: userData.lastName,
      email: userData.email,
      password: userData.password,
    };

    const response = await apiCall("POST", "/register", requestData);

    if (!response.error) {
      setUserData({ zId: userData.zId });
      navigateToVerifyAccount();
    }

    return response;
  }

  return (
    <>
      <AuthNavBar buttonLabel="Login" />
      <SignUpForm id="sign-up-form" onSubmit={onSubmit} />
    </>
  );
}

export default SignUpPage;
