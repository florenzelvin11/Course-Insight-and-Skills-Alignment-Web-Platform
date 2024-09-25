import React from 'react';
import NavBar from '../components/NavBar';
import { useState } from 'react';
import PageHeading from '../components/PageHeading';
import { getUserData, apiCall } from '../helpers/helper';
import Dashboard from '../components/Dashboard';
import ProfileCourseCard from '../components/ProfileCourseCard';
import { useParams } from 'react-router-dom';
import { useGlobalState } from '../components/GlobalReloadProvider';
import LoadingScreen from '../components/LoadingScreen';

export default function ProfileCoursePage() {
    const { globalReload, setGlobalReload } = useGlobalState()
    const params = useParams()
    const isUser = params?.zID == getUserData()?.profileData.zID;
    const [isLoading, setIsLoading] = React.useState(true)
  
    const [courseData, setCourseData] = useState([])

    React.useEffect(() => {
        async function getData() {
            try {
                const response = await apiCall('GET', `/${params.userType}/course?zID=${params.zID}`)
                if (!response.error) {
                    setCourseData(response.courses)
                    setIsLoading(false)
                } else {
                    console.log(response.error)
                }
                return response
            } catch(e) {
                //
            }
        }
        getData()
    }, [globalReload])

    const onDelete = async (index, course) => {
        const requestData = {
            zID: params?.zID,
            courseCode: course.courseCode,
            yearDate: course.yearDate,
            term: course.term,
        }

        const response = await apiCall('DELETE', `/${params.userType}/course/delete`, requestData)
        // const response = {} // Test Successful Post

        if (!response.error) {
            // Make sure courseData is in the right format and then push it into courseCodes.
            const updatedCourses = courseData.filter((_, i) => i !== index);
            setCourseData(updatedCourses);
            setIsLoading(false)
            setGlobalReload(!globalReload);
        } else {
            // alert(response.error);
        }
        return response
    }

    const handleRemoveCourse = (e, index, course) => {
        e.preventDefault();
        onDelete(index, course);
        setIsLoading(true)
    };

  return (
    <>
        <NavBar/>
        {
            isLoading ?
            <LoadingScreen />
            :
            <>
            <PageHeading
                backButtonName="Profile"
                backPath={-1}
                title="Courses"
            />
            <Dashboard 
                content={courseData.map((course, index) => (
                <ProfileCourseCard
                    key={index}
                    courseCode={course.courseCode}
                    courseInfo={course}
                    public={!isUser}
                    onDelete={(e) => handleRemoveCourse(e, index, course)}
                    sx={{
                        backgroundColor: "white",
                    }}
                />
                ))}
            />
            </>
        }
    </>
  );
}