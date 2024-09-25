import React from 'react';
import NavBar from '../components/NavBar';
import { useState } from 'react';
import PageHeading from '../components/PageHeading';
import { apiCall } from '../helpers/helper';
import Dashboard from '../components/Dashboard';
import { useParams } from 'react-router-dom';
import { useGlobalState } from '../components/GlobalReloadProvider';
import LoadingScreen from '../components/LoadingScreen';
import MediaCard from '../components/MediaCard';
import placeHolderCourseThumbnail from "../assets/placeHolderCourseImage.jpg";


export default function ProfileProjectPage() {
    const { globalReload } = useGlobalState()
    const params = useParams()
    const [isLoading, setIsLoading] = React.useState(true)
  
    const [projectData, setProjectData] = useState([])

    React.useEffect(() => {
        async function getData() {
            try {
                const response = await apiCall('GET', `/student/projects?zID=${JSON.stringify(params.zID)}`)
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
                title="Projects"
            />
            <Dashboard 
                content={projectData.map((project, index) => (
                    <MediaCard
                        key={index}
                        heading={project.projectName}
                        school={project.client}
                        thumbnail={project.thumbnail || placeHolderCourseThumbnail}
                        path={`/project/${project.id}`}
                        sx={{
                            backgroundColor: 'white',
                            maxWidth: '340px'
                        }}
                    />
                ))}
            />
            </>
        }
    </>
  );
}