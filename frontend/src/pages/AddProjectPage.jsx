import * as React from "react";
import NavBar from "../components/NavBar";
import { useState, useEffect } from "react";
import PageHeading from "../components/PageHeading";
import { apiCall, arrayToObject, getUserType } from "../helpers/helper";
import ResultModal from "../components/ResultModal";
import { useNavigate } from "react-router-dom";
import { useGlobalState } from "../components/GlobalReloadProvider";
import AddProjectForm from "../components/AddProjectForm";

function AddProjectPage() {
  const navigate = useNavigate();
  const [openModal, setOpenModal] = useState(false);
  const { globalReload } = useGlobalState();

  useEffect(() => {
    const checkUserType = () => {
      if (getUserType() === "student") {
        navigate("/project-dashboard");
      }
    };

    checkUserType();
  }, [globalReload, navigate]);

  async function onSubmit(projectData) {
    const requestData = {
      name: projectData.name,
      client: projectData.client,
      skills: arrayToObject(projectData.skills),
      knowledge: arrayToObject(projectData.knowledge),
      thumbnail: projectData.thumbnail,
      scope: projectData.scope,
      requirements: projectData.requirements,

      topics: projectData.topics,
      outcomes: projectData.outcomes,
    };

    const response = await apiCall("POST", `/projects`, requestData);
    if (!response.error) {
      handleOpen();
    }
    return response;
  }

  const handleOpen = () => {
    setOpenModal(true);
  };

  const handleClose = () => {
    navigate("/project-dashboard");
    setOpenModal(false);
  };

  return (
    <>
      <NavBar />
      <PageHeading
        backButtonName="Project Dashboard"
        backPath="/project-dashboard"
        title="Add Project"
      />
      <ResultModal
        handleClose={handleClose}
        open={openModal}
        heading="Project Added!!"
        buttonText="Contiune to dashboard"
      ></ResultModal>
      <AddProjectForm onSubmit={onSubmit} />
    </>
  );
}

export default AddProjectPage;
