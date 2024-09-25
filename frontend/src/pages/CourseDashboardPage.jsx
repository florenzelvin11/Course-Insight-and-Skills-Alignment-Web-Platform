import * as React from "react";
import NavBar from "../components/NavBar";
import { useState, useEffect } from "react";
import CourseCard from "../components/CourseCard";
import PageHeading from "../components/PageHeading";
import Dashboard from "../components/Dashboard";
import Alert from "@mui/material/Alert";
import { apiCall, canAdd } from "../helpers/helper";
import { noCoursesError } from "../constants/constants";
import { useGlobalState } from "../components/GlobalReloadProvider";

function CourseDashboardPage() {
  const [courseData, setCourseData] = useState([]);
  const [noCourses, setNoCourses] = useState(false);
  const { globalReload } = useGlobalState();

  function failedRequest() {
    setNoCourses(true);
    setCourseData([]);
  }

  function successfulRequest(courses) {
    setNoCourses(false);
    setCourseData(courses);
  }

  useEffect(() => {
    const fetchCourseData = async () => {
      try {
        const { courses } = await apiCall(
          "GET",
          `/courses/${canAdd() ? "academic" : "student"}`
        );
        if (courses.length === 0) {
          failedRequest();
        } else {
          successfulRequest(courses);
        }
      } catch (error) {
        failedRequest();
      }
    };

    fetchCourseData();
  }, [globalReload]);

  return (
    <>
      <NavBar />
      <PageHeading
        title="Courses"
        actionPath={canAdd() ? "/add-course-menu" : ""}
        actionName="Add"
      />
      <Dashboard
        content={courseData.map((course, index) => (
          <CourseCard
            key={index}
            name={course.name}
            code={course.code}
            school={course.school}
            thumbnail={course.thumbnail}
            sx={{ width: "370px" }}
          />
        ))}
        error={noCourses && <Alert severity="warning">{noCoursesError}</Alert>}
      />
    </>
  );
}

export default CourseDashboardPage;
