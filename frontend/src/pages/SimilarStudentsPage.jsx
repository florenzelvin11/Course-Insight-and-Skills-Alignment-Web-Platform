import React from 'react';
import NavBar from '../components/NavBar';
import { useState } from 'react';
import PageHeading from '../components/PageHeading';
import { Box } from '@mui/material';
import Studentcard from '../components/StudentCard';
import LoadingWidget from '../components/LoadingWidget';
import { useGlobalState } from '../components/GlobalReloadProvider';
import { apiCall, getUserData, getUserType } from '../helpers/helper';
import { useNavigate } from 'react-router-dom';

export default function SimilarStudentsPage() {

  const navigate = useNavigate()

  if (getUserType() !== 'student') {
    navigate('/profile')
  }

  const { globalReload } = useGlobalState()

  const [isLoading, setIsLoading] = React.useState(true)
  
  const [studentsData, setStudentsData] = useState([])

  React.useEffect(() => {
    async function getData() {
        try {
            const response = await apiCall('GET', `/user/recommended-users?zID=${getUserData().profileData.zID}`)
            // const response = {}
            if (!response.error) {
                setStudentsData(response.students)
                setIsLoading(false)
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
      <PageHeading 
          backButtonName="Profile"
          backPath="/profile"
          title="Similar Students"
      />
      {
        isLoading ?
        <LoadingWidget />
        :
        <Box
          mb="100px"
          width="100%"
          display="flex"
          justifyContent="center"
        >
          <div className="similar-student-container">
            {studentsData.map((student, index) => (
                <Studentcard 
                key={index}
                zID={student.zID}
                profileData={student}
                path={`/profile/student/${student.zID}`}
                sx={{
                  width: '600px'
                }}
              />
            ))
            }
          </div>
        </Box>
      }
    </>
  );
}