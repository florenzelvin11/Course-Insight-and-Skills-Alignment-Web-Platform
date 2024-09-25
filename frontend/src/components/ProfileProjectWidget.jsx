import React from 'react'
import { Box, Typography, Divider } from "@mui/material";
import FlexBetween from "./FlexBetween";
import WidgetWrapper from "./WidgetWrapper";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiCall } from "../helpers/helper";
import { useGlobalState } from './GlobalReloadProvider';
import LoadingWidget from './LoadingWidget';
import MediaCard from './MediaCard';
import placeHolderCourseThumbnail from "../assets/placeHolderCourseImage.jpg";

const ProfileProjectsWidget = (props) => {
    const navigate = useNavigate()
    const { globalReload } = useGlobalState();
    const [ isLoading, setIsLoading ] = React.useState(false)
    
    const [projectData, setProjectData] = useState([])

    React.useEffect(() => {
        async function getData() {
            try {
                const response = await apiCall('GET', `/student/projects?zID=${JSON.stringify(props.zID)}`)

                if (!response.error) {
                    setProjectData(response.projects)
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

    return (
        <WidgetWrapper maxWidth={'920px'}>
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
                    Projects I&apos;m In
                </Typography>
            </Box>
        </FlexBetween>

        {
            isLoading ?
            <LoadingWidget />
            : 
            <>
            {
                projectData.length > 0
                &&
                <>
                {/* Second Row */}
                <Divider />
                <Box p="1rem 0">
                    <div className="profile-course-container">
                        {projectData.slice(0,6).map((project, index) => (
                            <MediaCard
                                key={index}
                                heading={project.projectName}
                                school={project.client}
                                thumbnail={project.thumbnail || placeHolderCourseThumbnail}
                                path={`/project/${project.id}`}
                                sx={{
                                    backgroundColor: 'white',
                                    maxWidth: '340px',
                                }}
                            />
                        ))
                        }
                    </div>
                </Box>
                </>
            }

            {/* Third Row */}
            {/* TODO */}
            {
                projectData.length > 6
                &&
                <>
                <Box 
                    p="0 0"
                    display={'flex'}
                    justifyContent={'center'}
                    m={'0'}
                    onClick={() => navigate(`/profile/student/${props.zID}/projects`)}
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

export default ProfileProjectsWidget;