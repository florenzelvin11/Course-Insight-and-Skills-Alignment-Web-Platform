import * as React from "react";
import NavBar from "../components/NavBar";
import { useState, useEffect } from "react";
import PageHeading from "../components/PageHeading";
import { apiCall, getUserType } from "../helpers/helper";
import ResultModal from "../components/ResultModal";
import { useNavigate } from "react-router-dom";
import { useGlobalState } from "../components/GlobalReloadProvider";
import AddCourseUrlForm from "../components/AddCourseUrlForm";

function AddCourseUrlPage() {
  const navigate = useNavigate();
  const [openModal, setOpenModal] = useState(false);
  const { globalReload } = useGlobalState();

  useEffect(() => {
    const checkUserType = () => {
      if (getUserType() === "student") {
        navigate("/course-dashboard");
      }
    };

    checkUserType();
  }, [globalReload, navigate]);

  async function onSubmit(courseData) {
    const requestData = {
      url: courseData.url,
    };

    const response = await apiCall("PUT", `/courses/url`, requestData);
    if (!response.error) {
      handleOpen();
    }
    return response;
  }

  const handleOpen = () => {
    setOpenModal(true);
  };

  const handleClose = () => {
    navigate("/course-dashboard");
    setOpenModal(false);
  };

  return (
    <>
      <NavBar />
      <PageHeading
        backButtonName="Add Course Menu"
        backPath="/add-course-menu"
        title="Add Course"
      />
      <ResultModal
        handleClose={handleClose}
        open={openModal}
        heading="URL received! Please note that ths process can take up to 5 minutes"
        buttonText="Contiune to dashboard"
      ></ResultModal>
      <AddCourseUrlForm onSubmit={onSubmit} />
    </>
  );
}

export default AddCourseUrlPage;
