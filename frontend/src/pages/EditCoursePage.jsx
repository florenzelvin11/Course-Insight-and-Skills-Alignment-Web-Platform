import * as React from "react";
import NavBar from "../components/NavBar";
import { useState, useEffect } from "react";
import PageHeading from "../components/PageHeading";
import { useParams } from "react-router-dom";
import EditCourseForm from "../components/EditCourseForm";
import { apiCall, arrayToObject, getUserType } from "../helpers/helper";
import ResultModal from "../components/ResultModal";
import { useNavigate } from "react-router-dom";
import { useGlobalState } from "../components/GlobalReloadProvider";

function EditCoursePage() {
  const navigate = useNavigate();
  const params = useParams();
  const [courseData, setCourseData] = useState("");
  const [oldCourseData, setOldCourseData] = useState("");
  const [openModal, setOpenModal] = useState(false);
  const { globalReload } = useGlobalState();

  function successfulRequest(courseData) {
    setCourseData(courseData);
    setOldCourseData(courseData);
  }

  function failedRequest() {
    setCourseData("");
  }

  useEffect(() => {
    const fetchCourseData = async () => {
      try {
        const courseData = await apiCall(
          "GET",
          `/courses/${params.courseCode}${
            params.version ? `/${params.version}` : ""
          }`
        );
        if (courseData.error) {
          failedRequest();
        } else {
          successfulRequest(courseData);
        }
      } catch (error) {
        failedRequest();
      }
    };

    const checkUserType = () => {
      if (getUserType() === "student") {
        navigate(`/course/${params.courseCode}`);
      }
    };

    fetchCourseData();
    checkUserType();
  }, [params.courseCode, params.version, globalReload, navigate]);

  async function onSubmit(newCourseData) {
    const requestData = {
      name: newCourseData.name,
      code: newCourseData.code,
      year: parseInt(newCourseData.year),
      term: newCourseData.term,
      thumbnail: newCourseData.thumbnail,
      school: courseData.school,
      topics: newCourseData.topics,
      description: newCourseData.description,
      skills: arrayToObject(newCourseData.skills),
      knowledge: arrayToObject(newCourseData.knowledge),
    };

    const response = await apiCall(
      "PUT",
      `/courses/${oldCourseData.code}/${oldCourseData.currentYear}/${oldCourseData.currentTerm}`,
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
    navigate(`/course/${params.courseCode}`);
    setOpenModal(false);
  };

  return (
    <>
      <NavBar />
      <PageHeading
        title={params.courseCode}
        backButtonName={`${params.courseCode}`}
        backPath={`/course/${params.courseCode}`}
      />
      <ResultModal
        handleClose={handleClose}
        open={openModal}
        heading="Course updated!!"
        buttonText="Contiune"
      ></ResultModal>
      <EditCourseForm courseData={courseData} onSubmit={onSubmit} />
    </>
  );
}

export default EditCoursePage;
