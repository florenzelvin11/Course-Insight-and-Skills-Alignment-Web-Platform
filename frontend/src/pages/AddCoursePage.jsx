import * as React from "react";
import NavBar from "../components/NavBar";
import { useState, useEffect } from "react";
import PageHeading from "../components/PageHeading";
import { apiCall, arrayToObject, getUserType } from "../helpers/helper";
import ResultModal from "../components/ResultModal";
import { useNavigate } from "react-router-dom";
import AddCourseForm from "../components/AddCourseForm";
import { useGlobalState } from "../components/GlobalReloadProvider";

function AddCoursePage() {
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
      name: courseData.name,
      code: courseData.code,
      year: parseInt(courseData.year),
      term: courseData.term,
      topics: courseData.topics,
      description: courseData.description,
      thumbnail: courseData.thumbnail,
      school: courseData.school,
      skills: arrayToObject(courseData.skills),
      knowledge: arrayToObject(courseData.knowledge),
    };

    const response = await apiCall(
      "PUT",
      `/courses/${courseData.code}/${requestData.year}/${requestData.term}`,
      requestData
    );
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
        heading="Course Added!!"
        buttonText="Contiune to dashboard"
      ></ResultModal>
      <AddCourseForm onSubmit={onSubmit} />
    </>
  );
}

export default AddCoursePage;
