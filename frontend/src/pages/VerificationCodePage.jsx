import * as React from "react";
import AuthNavBar from "../components/AuthNavBar";
import { apiCall, setUserData } from "../helpers/helper";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useParams } from "react-router-dom";
import VerificationCodeForm from "../components/VerificationCodeForm";

function VerificationCodePage() {
  const params = useParams();
  const navigate = useNavigate();
  const [error, setError] = useState({ error: "" });

  function navigateToManageProfile() {
    navigate("/profile");
  }

  useEffect(() => {
    const verifyCode = async () => {
      if (params.zId && params.code) {
        const requestData = {
          zId: params.zId,
          code: params.code,
        };

        const response = await apiCall("POST", "/verifyCode", requestData);
        console.log("response here", response);
        if (!response.error) {
          setUserData({
            highestUserType: response.userType,
            userType: response.userType,
            token: response.token,
          });
          navigateToManageProfile();
          return;
        } else {
          setError({ error: "We could not verify your account at this time" });
        }
      }
    };

    verifyCode();
  }, [params.zId, params.code]);

  return (
    <>
      <AuthNavBar buttonLabel="Login" />
      <VerificationCodeForm error={error.error} />
    </>
  );
}

export default VerificationCodePage;
