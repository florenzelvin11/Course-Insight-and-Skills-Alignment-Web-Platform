import React from 'react'
import AddIcon from '@mui/icons-material/Add';
import { Box, Typography, Divider, IconButton } from "@mui/material";
import FlexBetween from "./FlexBetween";
import WidgetWrapper from "./WidgetWrapper";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiCall } from "../helpers/helper";
import ProfileCourseCard from './ProfileCourseCard';
import { useGlobalState } from './GlobalReloadProvider';
import LoadingWidget from './LoadingWidget';

const ProfileCourseWidget = (props) => {
    const navigate = useNavigate()
    const { globalReload, setGlobalReload } = useGlobalState();
    const [isLoading, setIsLoading] = React.useState(true)
    
    const [courseData, setCourseData] = useState(null)

    React.useEffect(() => {
        async function getData() {
            try {
                const response = await apiCall('GET', `/${props.userType}/course?zID=${JSON.stringify(props.zID)}`)

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
            zID: props.zID,
            courseCode: course.courseCode,
            yearDate: course.yearDate,
            term: course.term,
        }
        
        const response = await apiCall('DELETE', `/${props.userType}/course/delete`, requestData)
        // const response = {} // Test Successful Post

        if (!response.error) {
            // Make sure courseData is in the right format and then push it into courseCodes.
            const updatedCourses = courseData.filter((_, i) => i !== index);
            setCourseData(updatedCourses);
            setIsLoading(false)
            setGlobalReload(!globalReload);
        } else {
            alert(response.error);
        }
        return response
    }

    const handleRemoveCourse = (e, index, course) => {
        e.preventDefault();
        onDelete(index, course);
        setIsLoading(true)
    };

    return (
        <WidgetWrapper>
        {/* First Row */}
        <FlexBetween
            gap="0.5rem"
            pb="0.5rem"
        >
            <Box>
                <Typography 
                    variant="2"
                    component="h2"
                    color={"black"}
                    fontWeight="600"
                >
                    My Courses
                </Typography>
            </Box>
            {
                !props?.public
                &&
                <IconButton
                    color="primary"
                    aria-label="Add Courses"
                    component="span"
                    onClick={props.handleClickOpen}
                >
                    <AddIcon fontSize='large'/>
                </IconButton>
            }
        </FlexBetween>

        {
            isLoading ?
            <LoadingWidget />
            : 
            <>
            {
                courseData.length > 0
                &&
                <>
                {/* Second Row */}
                <Divider />
                <Box p="1rem 0">
                    <div className="profile-course-container">
                        {courseData.slice(0,6).map((course, index) => (
                            <ProfileCourseCard
                                key={index}
                                courseCode={course.courseCode}
                                courseInfo={course}
                                public={props.public}
                                onDelete={(e) => handleRemoveCourse(e, index, course)}
                                sx={{
                                    backgroundColor: "white",
                                }}
                            />
                        ))
                        }
                    </div>
                </Box>
                </>
            }

            {/* Third Row */}
            {
                courseData.length > 6
                &&
                <>
                <Box 
                    p="0 0"
                    display={'flex'}
                    justifyContent={'center'}
                    m={'0'}
                    onClick={() => navigate(`/profile/${props.userType}/${props.zID}/courses`)}
                >
                    <Typography
                        variant="subtitle1"
                        component="subtitle1"
                        sx={{
                            "&:hover": {
                                color: "#dcdcdc",
                                cursor: "pointer"
                            }
                        }}
                    >
                    See More...
                    </Typography>
                </Box>
                </>
            }
            </>
        }
        </WidgetWrapper>
    )
}

export default ProfileCourseWidget;