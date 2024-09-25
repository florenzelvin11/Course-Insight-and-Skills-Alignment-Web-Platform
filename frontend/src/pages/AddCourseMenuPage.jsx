import * as React from "react";
import NavBar from "../components/NavBar";
import { useEffect } from "react";
import PageHeading from "../components/PageHeading";
import { getUserType } from "../helpers/helper";
import { useNavigate } from "react-router-dom";
import { useGlobalState } from "../components/GlobalReloadProvider";
import SubmitButton from "../components/SubmitButton";

function AddCourseMenuPage() {
  const navigate = useNavigate();
  const { globalReload } = useGlobalState();

  useEffect(() => {
    const checkUserType = () => {
      if (getUserType() === "student") {
        navigate("/course-dashboard");
      }
    };

    checkUserType();
  }, [globalReload, navigate]);

  function navigateToAddUrl() {
    navigate("/add-course-url");
  }

  function navigateToAddManual() {
    navigate("/add-course");
  }

  function navigateToAddPdf() {
    navigate("/add-course-pdf");
  }

  return (
    <>
      <NavBar />
      <PageHeading
        backButtonName="Courses"
        backPath="/course-dashboard"
        title="Add Your Course"
      />
      <div className="add-button-container">
        <div className="add-button">
          <SubmitButton
            sx={{ width: "312px" }}
            onClick={navigateToAddUrl}
            label="Add Course with URL"
          />
        </div>
        <div className="add-button">
          <SubmitButton
            sx={{ width: "312px" }}
            onClick={navigateToAddManual}
            label="Manually add a Course"
          />
        </div>
        <div className="add-button">
          <SubmitButton
            sx={{ width: "312px" }}
            onClick={navigateToAddPdf}
            label="Add Course with a PDF"
          />
        </div>
      </div>
    </>
  );
}

export default AddCourseMenuPage;
