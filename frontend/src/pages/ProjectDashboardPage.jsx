import * as React from "react";
import NavBar from "../components/NavBar";
import { useState, useEffect } from "react";
import ProjectCard from "../components/ProjectCard";
import PageHeading from "../components/PageHeading";
import Dashboard from "../components/Dashboard";
import Alert from "@mui/material/Alert";
import { apiCall, canAdd, transformProjectList } from "../helpers/helper";
import { useGlobalState } from "../components/GlobalReloadProvider";

function ProjectDashboardPage() {
  const [projectData, setProjectData] = useState([]);
  const [noProjects, setNoProjects] = useState(false);
  const { globalReload } = useGlobalState();

  function failedRequest() {
    setNoProjects(true);
    setProjectData([]);
  }

  function successfulRequest(projects) {
    setNoProjects(false);
    projects = transformProjectList(projects);
    setProjectData(projects);
  }

  useEffect(() => {
    const fetchProjectData = async () => {
      try {
        const { projects } = await apiCall(
          "GET",
          `/projects/${canAdd() ? "academic" : "student"}`
        );

        const allProjectsIsEmpty = projects.every(obj => Object.keys(obj).length === 0);

        if (allProjectsIsEmpty) {
          failedRequest();
        } else {
          successfulRequest(projects);
        }
      } catch (error) {
        failedRequest();
      }
    };

    fetchProjectData();
  }, [globalReload]);

  return (
    <>
      <NavBar />
      <PageHeading
        title="Projects"
        actionPath={canAdd() ? "/add-project" : ""}
        actionName="Add"
      />
      <Dashboard
        content={projectData.map((project, index) => (
          <ProjectCard
            key={index}
            name={project.name}
            knowledge={project.knowledge}
            client={project.client}
            id={project.id}
            thumbnail={project.thumbnail}
          />
        ))}
        error={
          noProjects && (
            <Alert severity="warning">
              No projects can be found at this time
            </Alert>
          )
        }
      />
    </>
  );
}

export default ProjectDashboardPage;
