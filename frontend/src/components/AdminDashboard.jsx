import React from 'react';
import PageHeading from './PageHeading';
import WidgetWrapper from './WidgetWrapper';
import { Box, Divider, Typography } from '@mui/material';
import { PieChart } from "@mui/x-charts/PieChart";
import { useGlobalState } from './GlobalReloadProvider';
import { apiCall } from '../helpers/helper';
import LoadingWidget from './LoadingWidget';

export default function AdminDashboard() {
    const colours = [
        "#BD94E0",
        "#E094BD",
        "#94E094",
        "#E094E0",
        "#94BDE0",
        "#E0BD94",
        "#5A6B04",
        "#E06B5A",
        "#1F2B0E",
        "#E02B1F",
        "#FFA500",
        "#7C1C1C",
        "#1C7C3E",
        "#1C3E7C",
        "#3E1C7C",
        "#7C3E1C",
        "#4D4D4D",
        "#7C1C5B",
        "#5B7C1C",
        "#1C5B7C",
        "#7C5B1C",
        "#5B1C7C",
        "#FF5733",
        "#33FF57",
        "#5733FF",
        "#FF33E9",
        "#E9FF33",
        "#33E9FF",
        "#FF33A8",
        "#A8FF33"
    ];


    const { globalReload } = useGlobalState()
    const [ isLoading, setIsLoading ] = React.useState(true);

    const [ data, setData ] = React.useState(null);
    
    React.useEffect(() => {
        async function getProjects() {
            try {
                const response = await apiCall('GET', '/admin/dashboard');

                if (!response.error) {
                    setData(response.dashboard)
                    setIsLoading(false);
                }
                return response
            } catch(e) {
                //
                console.log(e.message)
            }
        }
        getProjects()
    }, [globalReload])


    return (
        <>
        <PageHeading
            title="Admin Dashboard"
        />
        {
        isLoading
        ?
        <LoadingWidget />
        :
        <Box className="container" >
            <Box display={'grid'} gridTemplateColumns={'repeat(3, 1fr)'} gap={'5rem'} width={"90%"}>
                <WidgetWrapper>
                    <h2 className="page-heading--title">Active Users</h2>
                    <Divider />
                    <Box mt={'10px'}>
                        <PieChart
                            series={[
                                {
                                    data: [
                                        {
                                            id: 1,
                                            value: data.userCount.student,
                                            label: 'Student',
                                            color: colours[4],
                                        },
                                        {
                                            id: 2,
                                            value: data.userCount.casualAcademic,
                                            label: 'Casual Academic',
                                            color: colours[7],
                                        },
                                        {
                                            id: 2,
                                            value: data.userCount.academic,
                                            label: 'Academic',
                                            color: colours[2],
                                        },
                                        {
                                            id: 2,
                                            value: data.userCount.courseAdmin,
                                            label: 'courseAdmin',
                                            color: colours[10],
                                        },
                                        
                                        {
                                            id: 3,
                                            value: data.userCount.admin,
                                            label: 'Admin',
                                            color: colours[16],
                                        },
                                    ]
                                }
                            ]}
                            width={460}
                            height={200}
                        />
                    </Box>
                </WidgetWrapper>
                <WidgetWrapper>
                    <h2 className="page-heading--title">Active Courses</h2>
                    <Divider />
                    <Box sx={{ 
                            display: 'flex', 
                            justifyContent: 'center', 
                            alignContent: 'center',
                            alignItems: 'center'
                        }}>
                        <Typography variant="body1" fontSize={'10rem'}>{data.courseCount}</Typography>
                    </Box>
                </WidgetWrapper>
                <WidgetWrapper>
                    <h2 className="page-heading--title">Active Projects</h2>
                    <Divider />
                    <Box sx={{ 
                            display: 'flex', 
                            justifyContent: 'center', 
                            alignContent: 'center',
                            alignItems: 'center'
                        }}>
                        <Typography variant="body1" fontSize={'10rem'}>{data.projectCount}</Typography>
                    </Box>
                </WidgetWrapper>
            </Box>
        </Box>
        }
        </>
    )
}