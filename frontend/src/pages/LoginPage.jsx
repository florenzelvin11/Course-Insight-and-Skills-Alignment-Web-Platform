import * as React from "react";
import LoginForm from "../components/LoginForm";
import AuthNavBar from "../components/AuthNavBar";
import { apiCall, setUserData } from "../helpers/helper";
import { useNavigate } from "react-router-dom";

function LoginPage() {
  const navigate = useNavigate();

  function navigateToCourseDashboard() {
    navigate("/course-dashboard");
  }

  async function onSubmit(userData) {
    const requestData = {
      email: userData.email,
      password: userData.password,
    };

    const response = await apiCall("POST", "/login", requestData);

    if (!response.error) {
      setUserData({
        highestUserType: response.userType,
        userType: response.userType,
        token: response.token,
      });
      navigateToCourseDashboard();
    }

    return response;
  }

  return (
    <>
      <AuthNavBar buttonLabel="sign up" />
      <LoginForm id="login-form" onSubmit={onSubmit} />
    </>
  );
}

export default LoginPage;
