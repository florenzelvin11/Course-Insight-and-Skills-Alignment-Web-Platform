import * as React from "react";
import NavBar from "../components/NavBar";
import { useState, useEffect } from "react";
import PageHeading from "../components/PageHeading";
import Alert from "@mui/material/Alert";
import { apiCall } from "../helpers/helper";
import { generalErrorMessage } from "../constants/constants";
import { useParams } from "react-router-dom";
import { useGlobalState } from "../components/GlobalReloadProvider";
import ProjectInfoPage from "../components/ProjectInfoPage";
import ResultModal from "../components/ResultModal";
import FormModal from "../components/FormModal";
import LoadingWidget from "../components/LoadingWidget";

function ProjectPage() {
  const params = useParams();
  const [projectData, setProjectData] = useState("");
  const [noProjectData, setNoProjectData] = useState(false);
  const [openModal, setOpenModal] = useState(false);
  const [openCreateGroupModal, setOpenCreateGroupModal] = useState(false);
  const { globalReload, setGlobalReload } = useGlobalState();
  const [userInGroup, setUserInGroup] = useState(false);

  async function successfulRequest(projectData) {
    setNoProjectData(false);
    const resultUserInAGroup = await isUserInAGroup(projectData);
    setUserInGroup(resultUserInAGroup);
    setProjectData(projectData);
  }

  async function isUserInAGroup(projectData) {
    const { zID } = await apiCall("GET", "/user/profile");
    return projectData.groups.some((group) => group.members.includes(zID));
  }

  function failedRequest() {
    setNoProjectData(true);
    setProjectData("");
  }

  async function joinGroup(groupID) {
    const response = await apiCall(
      "PUT",
      `/projects/join/${params.projectId}/${groupID}`
    );
    if (!response.error) {
      setGlobalReload(!globalReload);
      handleOpen();
    }
  }

  async function createGroupClick() {
    setOpenCreateGroupModal(true);
  }

  async function createGroup(name) {
    const requestBody = {
      groupName: name,
    };
    const response = await apiCall(
      "POST",
      `/projects/groupCreate/${params.projectId}`,
      requestBody
    );
    if (!response.error) {
      setGlobalReload(!globalReload);
      setOpenCreateGroupModal(false);
    }
  }

  useEffect(() => {
    window.scrollTo(0, 0);
    const fetchProjectData = async () => {
      try {
        const projectData = await apiCall(
          "GET",
          `/projects/${params.projectId}`
        );
        if (projectData.error) {
          failedRequest();
        } else {
          successfulRequest(projectData);
        }
      } catch (error) {
        failedRequest();
      }
    };

    fetchProjectData();
  }, [params.projectId, globalReload]);

  function title() {
    return projectData.name ?? "Project";
  }

  function errorBox() {
    return (
      <div className="error-container">
        <Alert sx={{ width: "50%" }} severity="warning">
          {generalErrorMessage}
        </Alert>
      </div>
    );
  }

  const handleOpen = () => {
    setOpenModal(true);
  };

  const handleClose = () => {
    setOpenModal(false);
  };

  return (
    <>
      <NavBar />
      <PageHeading
        title={title()}
        backButtonName="Projects"
        backPath="/project-dashboard"
      />
      {noProjectData ? (
        errorBox()
      ) : projectData === "" ? (
        <LoadingWidget />
      ) : (
        <>
          <ProjectInfoPage
            data={projectData}
            joinGroup={joinGroup}
            createGroup={createGroupClick}
            userInGroup={userInGroup}
          />
          <FormModal
            handleClose={createGroup}
            open={openCreateGroupModal}
            heading="Create a new group!!"
            buttonText="Create Group"
          />
          <ResultModal
            handleClose={handleClose}
            open={openModal}
            heading="Success, Group Joined"
            buttonText="Contiune"
          />
        </>
      )}
    </>
  );
}

export default ProjectPage;
