import * as React from "react";
import NavBar from "../components/NavBar";
import { useState, useEffect } from "react";
import PageHeading from "../components/PageHeading";
import Alert from "@mui/material/Alert";
import { apiCall, canAdd } from "../helpers/helper";
import { generalErrorMessage } from "../constants/constants";
import { useParams } from "react-router-dom";
import CourseInfoPage from "../components/CourseInfoPage";
import VersionDropDown from "../components/VersionDropDown";
import { useNavigate } from "react-router-dom";
import { useGlobalState } from "../components/GlobalReloadProvider";
import LoadingWidget from "../components/LoadingWidget";

function CoursePage() {
  const navigate = useNavigate();
  const params = useParams();
  const [courseData, setCourseData] = useState("");
  const [noCourseData, setNoCourseData] = useState(false);
  const { globalReload } = useGlobalState();

  function successfulRequest(courseData) {
    setNoCourseData(false);
    setCourseData(courseData);
  }

  function failedRequest() {
    setNoCourseData(true);
    setCourseData("");
  }

  function handleVersionChange(version) {
    navigate(
      `/course/${params.courseCode}/${
        params.yearTerm
          ? params.yearTerm
          : `${courseData.currentYear}-${courseData.currentTerm}`
      }/${version}`
    );
  }

  function handleYearTermChange(yearTerm) {
    navigate(
      `/course/${params.courseCode}/${yearTerm}${
        params.version ? `/${params.version}` : ""
      }`
    );
  }

  useEffect(() => {
    window.scrollTo(0, 0);
    const fetchCourseData = async () => {
      try {
        const courseData = await apiCall(
          "GET",
          `/courses/${params.courseCode}${
            params.yearTerm
              ? `/${params.yearTerm.split("-")[0]}/${
                  params.yearTerm.split("-")[1]
                }`
              : ""
          }${params.version ? `/${params.version}` : ""}`
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

    fetchCourseData();
  }, [params.version, params.courseCode, params.yearTerm, globalReload]);

  function title() {
    return `${params.courseCode} ${noCourseData ? "" : `- ${courseData.name}`}`;
  }

  function underCourseHeader() {
    return (
      <div className="under-course-header">
        <div className="under-course-header-drop-down">
          {canAdd() && (
            <VersionDropDown
              label="Version"
              onSelection={handleVersionChange}
              currentVersion={params.version || courseData.currentVersion}
              versions={courseData.availableVersions}
            />
          )}
          <VersionDropDown
            label="Year Term"
            onSelection={handleYearTermChange}
            currentVersion={
              params.yearTerm
                ? params.yearTerm
                : `${courseData.currentYear}-${courseData.currentTerm}`
            }
            versions={getOptions(courseData.availableYearTerms)}
          />
        </div>
      </div>
    );
  }

  function getOptions(list) {
    if (list) {
      return list.map((item) => item.join("-"));
    }
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

  return (
    <>
      <NavBar />
      <PageHeading title={title()} backButtonName={"Back"} backPath={-1} />
      {noCourseData ? (
        errorBox()
      ) : courseData === "" ? (
        <LoadingWidget />
      ) : (
        <>
          {underCourseHeader()}
          <CourseInfoPage
            editPath={`/course-edit/${params.courseCode}`}
            data={courseData}
          />
        </>
      )}
    </>
  );
}

export default CoursePage;
