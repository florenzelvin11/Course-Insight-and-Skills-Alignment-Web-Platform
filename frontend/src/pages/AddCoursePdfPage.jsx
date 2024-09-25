import * as React from "react";
import NavBar from "../components/NavBar";
import { useState, useEffect } from "react";
import PageHeading from "../components/PageHeading";
import { apiCall, getUserType } from "../helpers/helper";
import ResultModal from "../components/ResultModal";
import { useNavigate } from "react-router-dom";
import { useGlobalState } from "../components/GlobalReloadProvider";
import AddCoursePdfForm from "../components/AddCoursePdfForm";

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

  async function onSubmit(data) {
    console.log(data);
    const requestData = {
      pdf: data,
    };

    const response = await apiCall("PUT", `/courses/pdf`, requestData);
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
        heading="PDF received! Please note that this process can take up to 1 minute"
        buttonText="Contiune to dashboard"
      ></ResultModal>
      <AddCoursePdfForm onSubmit={onSubmit} />
    </>
  );
}

export default AddCourseUrlPage;
