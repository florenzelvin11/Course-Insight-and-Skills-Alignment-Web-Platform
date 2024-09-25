import React from 'react'
import { Box, Typography, Divider } from "@mui/material";
import FlexBetween from "./FlexBetween";
import WidgetWrapper from "./WidgetWrapper";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiCall } from "../helpers/helper";
import Studentcard from './StudentCard';
import LoadingWidget from './LoadingWidget';
import { useGlobalState } from '../components/GlobalReloadProvider';

const SimilarStudentsWidget = (props) => {
    const { globalReload } = useGlobalState()

    const navigate = useNavigate()

    const [isLoading, setIsLoading] = React.useState(true)
    
    const [studentsData, setStudentsData] = useState([])

    React.useEffect(() => {
        async function getData() {
            try {
                const response = await apiCall('GET', `/user/recommended-users?zID=${props.zID}`)
                // const response = {}
                if (!response.error) {
                    setStudentsData(response.students) 
                    setIsLoading(false)
                } else {
                    console.log(response)
                }
                return response
            } catch(e) {
                //
            }
        }
        getData()
    }, [globalReload])

    return (
        <WidgetWrapper>
            {/* First Row */}
            <FlexBetween
                gap="0.5rem"
                pb="1.1rem"
            >
                <Box>
                    <Typography 
                        variant="2"
                        component="h2"
                        color={"black"}
                        fontWeight="600"
                    >
                        Similar Students
                    </Typography>
                </Box>
            </FlexBetween>

            <Divider />

            {
                isLoading ?
                <LoadingWidget />
                :
                <>
                {/* Second Row */}
                <Box p="1rem 0" maxWidth="1000px">
                    <div className="similar-student-container">
                        {studentsData.slice(0,6).map((student, index) => (
                            <Studentcard 
                            key={index}
                            zID={student.zID}
                            profileData={student}
                            path={`/profile/student/${student.zID}`}
                            sx={{
                                backgroundColor: "white"
                            }}
                        />
                        ))
                        }
                    </div>
                </Box>
                {/* Third Row */}
                {
                    studentsData.length > 6
                    &&
                    <>
                    <Box 
                        p="0 0"
                        display={'flex'}
                        justifyContent={'center'}
                        m={'0'}
                        onClick={() => navigate('/similar-students')}
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

export default SimilarStudentsWidget;